import pandas as pd
from app.connection import get_connection

def get_tablas_y_indices(conn_params=None):
    """
    R1: Listar el nombre de las tablas e índices existentes en el esquema streaming.
    Retorna (df_tablas, df_indices).
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query_tablas = """
        SELECT t.name AS [Tabla],
               s.name AS [Esquema],
               t.create_date AS [Fecha de Creación]
        FROM sys.tables t
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
        ORDER BY t.name;
        """
        
        query_indices = """
        SELECT t.name AS [Tabla],
               i.name AS [Índice],
               i.type_desc AS [Tipo de Índice],
               CASE WHEN i.is_unique = 1 THEN 'Sí' ELSE 'No' END AS [Único],
               CASE WHEN i.is_primary_key = 1 THEN 'Sí' ELSE 'No' END AS [Clave Primaria]
        FROM sys.indexes i
        JOIN sys.tables t ON i.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming' AND i.name IS NOT NULL
        ORDER BY t.name, i.name;
        """
        
        df_tablas = pd.read_sql(query_tablas, conn)
        df_indices = pd.read_sql(query_indices, conn)
        return df_tablas, df_indices
    finally:
        conn.close()
