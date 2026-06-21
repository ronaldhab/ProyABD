import math
import pandas as pd
from app.connection import get_connection
from app import config

def get_tables_and_columns(conn_params=None):
    """
    Retorna un diccionario {tabla: [columnas]} de todas las tablas en el esquema streaming.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT t.name AS [Tabla], c.name AS [Columna]
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
        ORDER BY t.name, c.column_id;
        """
        df = pd.read_sql(query, conn)
        result = {}
        for _, row in df.iterrows():
            table = row["Tabla"]
            col = row["Columna"]
            if table not in result:
                result[table] = []
            result[table].append(col)
        return result
    finally:
        conn.close()

def estimate_query_cost(table_name, column_name, conn_params=None):
    """
    R10: Dada una consulta de igualdad sobre un campo de una tabla,
    indica si existe un índice que pueda ser utilizado y estima el costo
    en cantidad de accesos a disco y en tiempo.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        # 1. Obtener estadísticas físicas de la tabla (filas y páginas)
        query_stats = """
        SELECT 
            SUM(CASE WHEN ps.index_id IN (0, 1) THEN ps.row_count ELSE 0 END) AS [Filas],
            SUM(CASE WHEN ps.index_id IN (0, 1) THEN ps.used_page_count ELSE 0 END) AS [PaginasUsadas]
        FROM sys.tables t
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        JOIN sys.dm_db_partition_stats ps ON t.object_id = ps.object_id
        WHERE s.name = 'streaming' AND t.name = ?
        GROUP BY t.name;
        """
        cursor = conn.cursor()
        cursor.execute(query_stats, table_name)
        stats_row = cursor.fetchone()
        
        if not stats_row:
            return {"error": f"No se encontraron estadísticas para la tabla {table_name}"}
        
        total_rows = stats_row[0]
        total_pages = stats_row[1]
        
        # Si la tabla tiene 0 páginas (por ejemplo, vacía), asumimos al menos 1 para los cálculos
        if total_pages == 0:
            total_pages = 1
            
        # 2. Calcular tamaño del registro y factor de bloqueo
        query_row_size = """
        SELECT SUM(c.max_length) AS [TamanoRegistro]
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming' AND t.name = ?;
        """
        cursor.execute(query_row_size, table_name)
        row_size = cursor.fetchone()[0] or 1
        blocking_factor = max(1, math.floor(config.PAGE_SIZE_BYTES / row_size))
        
        # 3. Buscar si existe un índice utilizable (donde la columna sea la principal o primera del índice)
        query_index = """
        SELECT 
            i.name AS [IndiceNombre],
            i.type_desc AS [IndiceTipo],
            i.is_unique AS [IndiceUnico],
            i.is_primary_key AS [IndicePK]
        FROM sys.indexes i
        JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        JOIN sys.tables t ON i.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
          AND t.name = ?
          AND c.name = ?
          AND ic.key_ordinal = 1
          AND i.name IS NOT NULL;
        """
        cursor.execute(query_index, (table_name, column_name))
        index_row = cursor.fetchone()
        
        index_exists = index_row is not None
        index_details = {}
        
        # 4. Estimación del Costo
        # Tasa de transferencia en bytes por segundo: 17 MB/s = 17 * 1024 * 1024 bytes/s
        transfer_rate_bps = config.TRANSFER_RATE_MB_S * 1024 * 1024
        # Tiempo por acceso de una página:
        time_per_page = config.PAGE_SIZE_BYTES / transfer_rate_bps
        
        # --- Caso 1: Búsqueda secuencial (Full Table Scan) sin usar índices
        scan_accesses = total_pages
        scan_time_sec = scan_accesses * time_per_page
        
        # --- Caso 2: Búsqueda indexada
        seek_accesses = None
        seek_time_sec = None
        
        if index_exists:
            index_details = {
                "nombre": index_row[0],
                "tipo": index_row[1],
                "unico": "Sí" if index_row[2] == 1 else "No",
                "pk": "Sí" if index_row[3] == 1 else "No"
            }
            
            # Estimación del costo de una Búsqueda Indexada (B-Tree traversal)
            # Para SQL Server, la altura estimada de un B-Tree se puede modelar como logaritmo
            # de las páginas de datos en base al factor de bloqueo del índice.
            # - Altura del árbol B-Tree del índice: ceil(log(P, 100)) + 1 (asumiendo fan-out promedio de 100)
            # - Si es un Clustered Index (tipo 'CLUSTERED'):
            #   Leemos los niveles del B-Tree y llegamos directo al dato.
            # - Si es un Non-Clustered Index (tipo 'NONCLUSTERED'):
            #   Leemos los niveles del B-Tree del índice y hacemos 1 Lookup a la página de datos.
            
            btree_fanout = 100 # Fan-out estándar típico
            btree_height = max(1, math.ceil(math.log(total_pages, btree_fanout))) if total_pages > 1 else 1
            
            if index_details["tipo"] == "CLUSTERED":
                seek_accesses = btree_height + 1
            else:
                # B-Tree del índice + 1 lookup a la tabla
                seek_accesses = btree_height + 1 + 1
                
            # Asegurar que el costo con índice no sea mayor que el scan en tablas pequeñas
            if seek_accesses > scan_accesses:
                seek_accesses = scan_accesses
                
            seek_time_sec = seek_accesses * time_per_page
            
        return {
            "tabla": table_name,
            "columna": column_name,
            "total_filas": total_rows,
            "total_paginas": total_pages,
            "tamano_registro": row_size,
            "factor_bloqueo": blocking_factor,
            "indice_existe": index_exists,
            "indice_detalles": index_details,
            "costo_scan": {
                "accesos": scan_accesses,
                "tiempo_segundos": scan_time_sec
            },
            "costo_seek": {
                "accesos": seek_accesses,
                "tiempo_segundos": seek_time_sec
            } if index_exists else None
        }
    finally:
        conn.close()
