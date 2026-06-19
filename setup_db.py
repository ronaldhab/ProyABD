import re
import os
import pyodbc
from app import config
from app.connection import get_connection

def split_sql_statements(content):
    """Divide un script SQL en bloques individuales usando el separador GO en su propia línea."""
    # Expresión regular para encontrar GO al inicio de línea, opcionalmente rodeado de espacios
    pattern = re.compile(r'^\s*GO\s*$', re.IGNORECASE | re.MULTILINE)
    statements = pattern.split(content)
    return [stmt.strip() for stmt in statements if stmt.strip()]

def execute_statements(conn, statements, file_name):
    """Ejecuta una lista de declaraciones SQL en una conexión activa."""
    cursor = conn.cursor()
    for i, stmt in enumerate(statements):
        # Limpiar comentarios iniciales vacíos
        clean_stmt = re.sub(r'^--.*$', '', stmt, flags=re.MULTILINE).strip()
        if not clean_stmt:
            continue
            
        try:
            cursor.execute(clean_stmt)
        except Exception as e:
            # Mostrar contexto del error
            preview = clean_stmt[:120].replace('\n', ' ')
            print(f"[ERROR] Error en {file_name} (Bloque {i+1}): {e}")
            print(f"   Sentencia: {preview}...")
            raise e

def setup_database():
    """Ejecuta los scripts SQL del repositorio en orden para configurar y poblar la base de datos."""
    print("[START] Iniciando configuracion de la base de datos StreamUCV...")
    
    server = config.SERVER
    # Si detectamos que no tiene la instancia SQLEXPRESS, sugerimos cambiarla
    # Pero usaremos los valores de config de forma predeterminada.
    driver = config.DRIVER
    usr = config.USERNAME
    pwd = config.PASSWORD
    
    print(f"[CONNECT] Conectando a {server} (Driver: {driver})...")
    
    # 1. Conectar a master para crear la base de datos
    master_conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE=master;"
    if usr and pwd:
        master_conn_str += f"UID={usr};PWD={pwd};"
    else:
        master_conn_str += "Trusted_Connection=yes;"
        
    if "18" in driver:
        master_conn_str += "Encrypt=yes;TrustServerCertificate=yes;"
        
    try:
        conn = pyodbc.connect(master_conn_str)
        conn.autocommit = True
        print("[OK] Conexion exitosa a la base de datos master.")
    except Exception as e:
        print(f"[ERROR] Al conectar a master: {e}")
        print("Sugerencia: Si usas SQL Server Express local, asegurate de configurar SERVER = 'localhost\\\\SQLEXPRESS' en app/config.py.")
        return False
        
    try:
        repo_path = os.path.join("scripts", "create_repositorio_sqlserver.sql")
        if not os.path.exists(repo_path):
            repo_path = os.path.join("Fase-1", repo_path)
            
        print(f"[FILE] Leyendo {repo_path}...")
        with open(repo_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        statements = split_sql_statements(content)
        print(f"[RUN] Ejecutando {len(statements)} bloques en master...")
        execute_statements(conn, statements, "create_repositorio")
        print("[OK] Base de datos StreamUCV y esquema streaming creados.")
    except Exception as e:
        print(f"[ERROR] Al ejecutar create_repositorio: {e}")
        return False
    finally:
        conn.close()
        
    # 2. Conectar a la base de datos StreamUCV creada para crear tablas e insertar datos
    stream_conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE=StreamUCV;"
    if usr and pwd:
        stream_conn_str += f"UID={usr};PWD={pwd};"
    else:
        stream_conn_str += "Trusted_Connection=yes;"
        
    if "18" in driver:
        stream_conn_str += "Encrypt=yes;TrustServerCertificate=yes;"
        
    try:
        conn = pyodbc.connect(stream_conn_str)
        conn.autocommit = True
        print("[OK] Conectado a la nueva base de datos StreamUCV.")
    except Exception as e:
        print(f"[ERROR] Al conectar a la base de datos StreamUCV recien creada: {e}")
        return False
        
    try:
        tables_path = os.path.join("scripts", "create_tables_sqlserver.sql")
        if not os.path.exists(tables_path):
            tables_path = os.path.join("Fase-1", tables_path)
            
        print(f"[FILE] Leyendo {tables_path}...")
        with open(tables_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        statements = split_sql_statements(content)
        print(f"[RUN] Ejecutando {len(statements)} bloques de creacion de tablas...")
        execute_statements(conn, statements, "create_tables")
        print("[OK] Tablas, restricciones e indices creados con exito.")
        
        inserts_path = os.path.join("scripts", "insert_tables_sqlserver.sql")
        if not os.path.exists(inserts_path):
            inserts_path = os.path.join("Fase-1", inserts_path)
            
        print(f"[FILE] Leyendo {inserts_path}...")
        with open(inserts_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        statements = split_sql_statements(content)
        print(f"[RUN] Ejecutando {len(statements)} bloques de insercion de datos (esto puede demorar unos segundos)...")
        execute_statements(conn, statements, "insert_tables")
        print("[OK] Datos de prueba cargados con exito.")
        
        print("\n*** Configuracion de base de datos finalizada con exito! ***")
        return True
        
    except Exception as e:
        print(f"[ERROR] Fallo la configuracion de las tablas/datos: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database()
