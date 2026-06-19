import pandas as pd
from app.connection import get_connection

def get_tamano_tablas(conn_params=None):
    """
    R6: Indicar el tamaño ocupado por cada tabla.
    Retorna un DataFrame con el desglose de filas, tamaño de datos, tamaño de índices y total en KB/MB.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT 
            t.name AS [Tabla],
            SUM(CASE WHEN ps.index_id IN (0, 1) THEN ps.row_count ELSE 0 END) AS [Filas],
            SUM(CASE WHEN ps.index_id IN (0, 1) THEN ps.used_page_count ELSE 0 END) * 8 AS [Datos (KB)],
            SUM(CASE WHEN ps.index_id > 1 THEN ps.used_page_count ELSE 0 END) * 8 AS [Índices (KB)],
            SUM(ps.used_page_count) * 8 AS [Total Usado (KB)],
            CAST((SUM(ps.used_page_count) * 8.0) / 1024.0 AS DECIMAL(10, 2)) AS [Total Usado (MB)]
        FROM sys.tables t
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        JOIN sys.dm_db_partition_stats ps ON t.object_id = ps.object_id
        WHERE s.name = 'streaming'
        GROUP BY t.name
        ORDER BY [Total Usado (KB)] DESC;
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
