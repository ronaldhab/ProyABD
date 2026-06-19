import pandas as pd
from app.connection import get_connection

def get_conteo_tablas_indices(conn_params=None):
    """
    R2: Indicar la cantidad total de tablas y la cantidad de índices definidos por cada tabla.
    Retorna (total_tablas, df_conteo_indices_por_tabla).
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query_total = """
        SELECT COUNT(*) AS total
        FROM sys.tables t
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming';
        """
        cursor = conn.cursor()
        cursor.execute(query_total)
        total_tablas = cursor.fetchone()[0]
        
        query_indices_por_tabla = """
        SELECT t.name AS [Tabla],
               COUNT(i.index_id) AS [Cantidad de Índices]
        FROM sys.tables t
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        LEFT JOIN sys.indexes i ON t.object_id = i.object_id AND i.name IS NOT NULL
        WHERE s.name = 'streaming'
        GROUP BY t.name
        ORDER BY t.name;
        """
        df_conteo = pd.read_sql(query_indices_por_tabla, conn)
        return total_tablas, df_conteo
    finally:
        conn.close()
