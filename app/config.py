# ==============================================================================
# StreamUCV - Variables de Configuración de Conexión (Requerido por Enunciado)
# ==============================================================================

# Servidor o instancia de SQL Server. Puede ser localhost, una IP o instancia (ej. localhost\SQLEXPRESS)
SERVER = "localhost\\SQLEXPRESS"

# Base de datos del proyecto
DATABASE = "StreamUCV"

# Usuario para la autenticación SQL Server
USERNAME = ""

# Contraseña del usuario sa o el que corresponda
PASSWORD = ""

# Driver de conexión instalado en el sistema
# Opciones comunes: 
# - "ODBC Driver 17 for SQL Server"
# - "ODBC Driver 18 for SQL Server"
# - "SQL Server" (Driver antiguo de Windows, no recomendado para tipos nuevos)
DRIVER = "ODBC Driver 17 for SQL Server"

# ==============================================================================
# Parámetros y Constantes de Cómputo (Esquema streaming y Supuestos Físicos)
# ==============================================================================

# Esquema de trabajo
SCHEMA = "streaming"

# Bloque (Página) en SQL Server en bytes
PAGE_SIZE_BYTES = 8192

# Velocidad de transferencia de disco asumida (en MB/seg)
TRANSFER_RATE_MB_S = 17.0
