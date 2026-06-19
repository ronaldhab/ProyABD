import pandas as pd
from app.connection import get_connection

def get_tamano_registro_por_tabla(conn_params=None):
    """
    R7: Calcular o estimar el tamaño de cada registro en bytes.
    Retorna un DataFrame con Tabla, Cantidad de Columnas y Tamaño de Registro en bytes.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT 
            t.name AS [Tabla],
            COUNT(c.column_id) AS [Cantidad de Columnas],
            SUM(c.max_length) AS [Tamaño de Registro (Bytes)]
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
        GROUP BY t.name
        ORDER BY t.name;
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
