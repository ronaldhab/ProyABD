import pandas as pd
from app.connection import get_connection

def get_tamano_columnas(conn_params=None):
    """
    R8: Indicar el tamaño de cada columna en bytes, según su tipo de dato.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT 
            t.name AS [Tabla],
            c.name AS [Columna],
            tp.name AS [Tipo de Dato],
            CASE 
                WHEN tp.name IN ('varchar', 'char') THEN tp.name + '(' + CAST(c.max_length AS VARCHAR) + ')'
                WHEN tp.name IN ('nvarchar', 'nchar') THEN tp.name + '(' + CAST(c.max_length/2 AS VARCHAR) + ')'
                WHEN tp.name IN ('decimal', 'numeric') THEN tp.name + '(' + CAST(c.precision AS VARCHAR) + ',' + CAST(c.scale AS VARCHAR) + ')'
                ELSE tp.name
            END AS [Definición SQL],
            c.max_length AS [Tamaño Máximo (Bytes)],
            CASE WHEN c.is_nullable = 1 THEN 'Sí' ELSE 'No' END AS [Acepta Nulos]
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        JOIN sys.types tp ON c.user_type_id = tp.user_type_id
        WHERE s.name = 'streaming'
        ORDER BY t.name, c.column_id;
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
