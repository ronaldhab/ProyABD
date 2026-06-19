import pandas as pd
from app.connection import get_connection

def get_restricciones(conn_params=None):
    """
    R3: Indicar las restricciones existentes en el esquema, señalando su nombre, tabla asociada y tipo de restricción.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT 
            c.name AS [Nombre de Restricción],
            t.name AS [Tabla Asociada],
            CASE c.type 
                WHEN 'PK' THEN 'Clave Primaria (Primary Key)'
                WHEN 'F'  THEN 'Clave Foránea (Foreign Key)'
                WHEN 'C'  THEN 'Verificación (Check Constraint)'
                WHEN 'UQ' THEN 'Unicidad (Unique)'
                WHEN 'D'  THEN 'Valor por Defecto (Default)'
                ELSE c.type_desc 
            END AS [Tipo de Restricción]
        FROM sys.objects c
        JOIN sys.tables t ON c.parent_object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
          AND c.type IN ('PK', 'UQ', 'F', 'C', 'D')
        ORDER BY [Tabla Asociada], [Tipo de Restricción], [Nombre de Restricción];
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
