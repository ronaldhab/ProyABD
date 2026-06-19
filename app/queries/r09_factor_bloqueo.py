import pandas as pd
from app.connection import get_connection

def get_factor_bloqueo(conn_params=None):
    """
    R9: Calcular el factor de bloqueo de las tablas e índices.
    Retorna (df_tablas_fb, df_indices_fb).
    """
    conn = get_connection(**(conn_params or {}))
    try:
        # 1. Factor de bloqueo de tablas
        query_tablas = """
        SELECT 
            t.name AS [Tabla],
            SUM(c.max_length) AS [Tamaño Registro (Bytes)],
            8192 AS [Tamaño Página (Bytes)],
            FLOOR(8192.0 / SUM(c.max_length)) AS [Factor de Bloqueo]
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
        GROUP BY t.name
        ORDER BY t.name;
        """
        
        # 2. Factor de bloqueo de índices
        # Se calcula sumando el tamaño de las columnas que componen la clave del índice.
        query_indices = """
        SELECT 
            t.name AS [Tabla],
            i.name AS [Índice],
            i.type_desc AS [Tipo de Índice],
            SUM(c.max_length) AS [Tamaño Fila de Índice (Bytes)],
            8192 AS [Tamaño Página (Bytes)],
            FLOOR(8192.0 / SUM(c.max_length)) AS [Factor de Bloqueo de Índice]
        FROM sys.indexes i
        JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        JOIN sys.tables t ON i.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming' AND i.name IS NOT NULL
        GROUP BY t.name, i.name, i.type_desc
        ORDER BY t.name, i.name;
        """
        
        df_tablas_fb = pd.read_sql(query_tablas, conn)
        df_indices_fb = pd.read_sql(query_indices, conn)
        
        return df_tablas_fb, df_indices_fb
    finally:
        conn.close()
