import pandas as pd
from app.connection import get_connection

def get_detalle_indices(conn_params=None):
    """
    R4: Para cada índice creado en el esquema, listar las columnas que lo conforman, 
    indicar si es único o no, y mostrar información relevante del índice disponible.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        # Consulta principal agrupada con STRING_AGG para mostrar columnas
        query = """
        SELECT 
            t.name AS [Tabla],
            i.name AS [Índice],
            i.type_desc AS [Tipo de Índice],
            CASE WHEN i.is_unique = 1 THEN 'Sí' ELSE 'No' END AS [Único],
            CASE WHEN i.is_primary_key = 1 THEN 'Sí' ELSE 'No' END AS [Clave Primaria],
            i.fill_factor AS [Factor de Relleno (Fill Factor)],
            STRING_AGG(
                c.name + CASE WHEN ic.is_descending_key = 1 THEN ' DESC' ELSE ' ASC' END, 
                ', '
            ) WITHIN GROUP (ORDER BY ic.key_ordinal) AS [Columnas que lo Conforman]
        FROM sys.indexes i
        JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
        JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        JOIN sys.tables t ON i.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming' AND i.name IS NOT NULL
        GROUP BY t.name, i.name, i.type_desc, i.is_unique, i.is_primary_key, i.fill_factor
        ORDER BY [Tabla], [Índice];
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
