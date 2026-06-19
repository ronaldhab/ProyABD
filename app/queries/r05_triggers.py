import pandas as pd
from app.connection import get_connection

def get_triggers(conn_params=None):
    """
    R5: Por cada trigger existente en el esquema, indicar su nombre, tipo, 
    estado y tabla que lo activa.
    """
    conn = get_connection(**(conn_params or {}))
    try:
        query = """
        SELECT 
            tr.name AS [Nombre de Trigger],
            t.name AS [Tabla Asociada],
            CASE WHEN tr.is_disabled = 1 THEN 'Deshabilitado' ELSE 'Habilitado' END AS [Estado],
            CASE 
                WHEN tr.is_instead_of_trigger = 1 THEN 'INSTEAD OF'
                ELSE 'AFTER' 
            END AS [Tipo de Activación],
            STRING_AGG(te.type_desc, ', ') AS [Eventos de Activación]
        FROM sys.triggers tr
        JOIN sys.trigger_events te ON tr.object_id = te.object_id
        JOIN sys.tables t ON tr.parent_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        WHERE s.name = 'streaming'
        GROUP BY tr.name, t.name, tr.is_disabled, tr.is_instead_of_trigger
        ORDER BY [Tabla Asociada], [Nombre de Trigger];
        """
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()
