import streamlit as st
import os
from app import config
from app.connection import get_installed_drivers, test_connection

# Importar funciones de consulta
from app.queries.r01_tablas_indices import get_tablas_y_indices
from app.queries.r02_conteo import get_conteo_tablas_indices
from app.queries.r03_restricciones import get_restricciones
from app.queries.r04_detalle_indices import get_detalle_indices
from app.queries.r05_triggers import get_triggers
from app.queries.r06_tamano_tablas import get_tamano_tablas
from app.queries.r07_tamano_registro import get_tamano_registro_por_tabla
from app.queries.r08_tamano_columnas import get_tamano_columnas
from app.queries.r09_factor_bloqueo import get_factor_bloqueo
from app.queries.r10_costo_consulta import get_tables_and_columns, estimate_query_cost

# ==============================================================================
# Capa de Optimización con Caché
# ==============================================================================

# Funciones internas optimizadas para caché (reciben argumentos hashables nativos)
@st.cache_data(ttl=600)
def _cached_get_tablas_y_indices(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_tablas_y_indices(params)

@st.cache_data(ttl=600)
def _cached_get_conteo_tablas_indices(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_conteo_tablas_indices(params)

@st.cache_data(ttl=600)
def _cached_get_restricciones(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_restricciones(params)

@st.cache_data(ttl=600)
def _cached_get_detalle_indices(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_detalle_indices(params)

@st.cache_data(ttl=600)
def _cached_get_triggers(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_triggers(params)

@st.cache_data(ttl=600)
def _cached_get_tamano_tablas(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_tamano_tablas(params)

@st.cache_data(ttl=600)
def _cached_get_tamano_registro_por_tabla(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_tamano_registro_por_tabla(params)

@st.cache_data(ttl=600)
def _cached_get_tamano_columnas(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_tamano_columnas(params)

@st.cache_data(ttl=600)
def _cached_get_factor_bloqueo(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_factor_bloqueo(params)

@st.cache_data(ttl=600)
def _cached_get_tables_and_columns(server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return get_tables_and_columns(params)

@st.cache_data(ttl=600)
def _cached_estimate_query_cost(table, col, server, database, username, password, driver):
    params = {"server": server, "database": database, "username": username, "password": password, "driver": driver}
    return estimate_query_cost(table, col, params)

# Wrappers públicos transparentes (mantienen la firma que toma un dict params)
def cached_get_tablas_y_indices(params):
    return _cached_get_tablas_y_indices(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_conteo_tablas_indices(params):
    return _cached_get_conteo_tablas_indices(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_restricciones(params):
    return _cached_get_restricciones(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_detalle_indices(params):
    return _cached_get_detalle_indices(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_triggers(params):
    return _cached_get_triggers(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_tamano_tablas(params):
    return _cached_get_tamano_tablas(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_tamano_registro_por_tabla(params):
    return _cached_get_tamano_registro_por_tabla(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_tamano_columnas(params):
    return _cached_get_tamano_columnas(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_factor_bloqueo(params):
    return _cached_get_factor_bloqueo(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_get_tables_and_columns(params):
    return _cached_get_tables_and_columns(params["server"], params["database"], params["username"], params["password"], params["driver"])

def cached_estimate_query_cost(table, col, params):
    return _cached_estimate_query_cost(table, col, params["server"], params["database"], params["username"], params["password"], params["driver"])

# ==============================================================================
# Helpers Compartidos
# ==============================================================================

def init_session_state():
    """Inicializa las variables de estado de sesión si no existen."""
    if "conn_server" not in st.session_state:
        st.session_state.conn_server = config.SERVER
    if "conn_database" not in st.session_state:
        st.session_state.conn_database = config.DATABASE
    if "conn_user" not in st.session_state:
        st.session_state.conn_user = config.USERNAME
    if "conn_password" not in st.session_state:
        st.session_state.conn_password = config.PASSWORD
    if "conn_driver" not in st.session_state:
        installed = get_installed_drivers()
        if config.DRIVER in installed:
            st.session_state.conn_driver = config.DRIVER
        elif installed:
            st.session_state.conn_driver = installed[0]
        else:
            st.session_state.conn_driver = config.DRIVER

def get_conn_params():
    """Retorna los parámetros de conexión activos en formato dict."""
    init_session_state()
    return {
        "server": st.session_state.conn_server,
        "database": st.session_state.conn_database,
        "username": st.session_state.conn_user,
        "password": st.session_state.conn_password,
        "driver": st.session_state.conn_driver
    }

def inject_sidebar():
    """Dibuja el sidebar común en la aplicación."""
    init_session_state()
    
    with st.sidebar:
        
        # Parámetros de conexión agrupados en un desplegable (expander)
        with st.expander("🔌 Conexión SQL Server", expanded=False):
            st.markdown("Ajusta los parámetros para conectarte a tu instancia local de SQL Server.")
            
            server_input = st.text_input("Servidor / Instancia", value=st.session_state.conn_server)
            db_input = st.text_input("Base de Datos", value=st.session_state.conn_database)
        
            auth_mode = st.radio("Modo de Autenticación", ["SQL Server Auth", "Windows Auth (Integrated)"])
            if auth_mode == "SQL Server Auth":
                user_input = st.text_input("Usuario", value=st.session_state.conn_user)
                pass_input = st.text_input("Contraseña", type="password", value=st.session_state.conn_password)
            else:
                user_input = ""
                pass_input = ""
            
            drivers = get_installed_drivers()
            if not drivers:
                drivers = [st.session_state.conn_driver]
        
            driver_input = st.selectbox(
                "Driver ODBC", 
                options=drivers,
                index=drivers.index(st.session_state.conn_driver) if st.session_state.conn_driver in drivers else 0
            )
        
            if st.button("🧪 Probar Conexión", use_container_width=True):
                success, msg = test_connection(server_input, db_input, user_input, pass_input, driver_input)
                if success:
                    st.success("Conexión establecida correctamente")
                    st.session_state.conn_server = server_input
                    st.session_state.conn_database = db_input
                    st.session_state.conn_user = user_input
                    st.session_state.conn_password = pass_input
                    st.session_state.conn_driver = driver_input
                    st.rerun()
                else:
                    st.error(f"Error de conexión:\n\n{msg}")

        st.markdown("---")
        st.markdown("🎓 **Administración de Bases de Datos**")
        st.markdown("Proyecto 1 — StreamUCV")
        st.caption("Fase 1 - Consulta del Diccionario de Datos")

def render_back_button():
    """Dibuja el botón para regresar al menú principal."""
    st.markdown('<div class="back-btn-container"></div>', unsafe_allow_html=True)
    if st.button("⬅️ Volver al Menú Principal"):
        st.switch_page("app/ui/pages/menu.py")
