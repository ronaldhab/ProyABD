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
                SUM(
                    CASE
                        WHEN tp.name = 'int' THEN 4
                        WHEN tp.name IN ('decimal', 'numeric') THEN (c.precision / 2) + 2
                        WHEN tp.name = 'float' THEN c.max_length
                        WHEN tp.name = 'real' THEN 4
                        WHEN tp.name IN ('datetime', 'datetime2') THEN
                            CASE WHEN c.scale > 2 THEN 8 ELSE 6 + (c.scale + 1) / 2 END
                        WHEN tp.name = 'date' THEN 3
                        WHEN tp.name = 'time' THEN 3 + (c.scale + 1) / 2
                        ELSE COALESCE(c.max_length, 0)
                    END
                ) AS [Tamano de Registro (Bytes)]
            FROM sys.columns c
            JOIN sys.tables t ON c.object_id = t.object_id
            JOIN sys.schemas s ON t.schema_id = s.schema_id
            JOIN sys.types tp ON c.user_type_id = tp.user_type_id
            WHERE s.name = 'streaming'
            GROUP BY t.name
            ORDER BY t.name;
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
