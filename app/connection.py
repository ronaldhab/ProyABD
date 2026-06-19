import pyodbc
from app import config

def get_installed_drivers():
    """Retorna la lista de drivers ODBC de SQL Server instalados en el sistema."""
    try:
        all_drivers = pyodbc.drivers()
        # Filtrar solo los que contengan SQL Server
        sql_drivers = [d for d in all_drivers if "sql server" in d.lower()]
        return sql_drivers if sql_drivers else all_drivers
    except Exception:
        return []

def test_connection(server, database, username, password, driver):
    """Prueba la conexión con los parámetros dados y retorna (success, message)."""
    try:
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
        if username and password:
            conn_str += f"UID={username};PWD={password};"
        else:
            conn_str += "Trusted_Connection=yes;"
        
        # Compatibilidad con ODBC Driver 18 y políticas de cifrado por defecto
        if "18" in driver:
            conn_str += "Encrypt=yes;TrustServerCertificate=yes;"
            
        conn = pyodbc.connect(conn_str, timeout=5)
        conn.close()
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)

def get_connection(server=None, database=None, username=None, password=None, driver=None):
    """Establece la conexión utilizando los parámetros provistos o los valores por defecto en config.py."""
    srv = server if server is not None else config.SERVER
    db = database if database is not None else config.DATABASE
    usr = username if username is not None else config.USERNAME
    pwd = password if password is not None else config.PASSWORD
    drv = driver if driver is not None else config.DRIVER
    
    conn_str = f"DRIVER={{{drv}}};SERVER={srv};DATABASE={db};"
    
    if usr and pwd:
        conn_str += f"UID={usr};PWD={pwd};"
    else:
        conn_str += "Trusted_Connection=yes;"
        
    if "18" in drv:
        conn_str += "Encrypt=yes;TrustServerCertificate=yes;"
        
    return pyodbc.connect(conn_str, timeout=10)
