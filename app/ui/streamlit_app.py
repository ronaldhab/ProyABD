import streamlit as st
import pandas as pd
import math
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

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
# Capa de Optimización con Caché (Evita latencia por múltiples reconexiones)
# ==============================================================================

@st.cache_data(ttl=600)
def cached_get_tablas_y_indices(params):
    return get_tablas_y_indices(params)

@st.cache_data(ttl=600)
def cached_get_conteo_tablas_indices(params):
    return get_conteo_tablas_indices(params)

@st.cache_data(ttl=600)
def cached_get_restricciones(params):
    return get_restricciones(params)

@st.cache_data(ttl=600)
def cached_get_detalle_indices(params):
    return get_detalle_indices(params)

@st.cache_data(ttl=600)
def cached_get_triggers(params):
    return get_triggers(params)

@st.cache_data(ttl=600)
def cached_get_tamano_tablas(params):
    return get_tamano_tablas(params)

@st.cache_data(ttl=600)
def cached_get_tamano_registro_por_tabla(params):
    return get_tamano_registro_por_tabla(params)

@st.cache_data(ttl=600)
def cached_get_tamano_columnas(params):
    return get_tamano_columnas(params)

@st.cache_data(ttl=600)
def cached_get_factor_bloqueo(params):
    return get_factor_bloqueo(params)

@st.cache_data(ttl=600)
def cached_get_tables_and_columns(params):
    return get_tables_and_columns(params)

@st.cache_data(ttl=600)
def cached_estimate_query_cost(table, col, params):
    return estimate_query_cost(table, col, params)
# Configuración de página
st.set_page_config(
    page_title="StreamUCV — Data Dictionary Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados para diseño premium
st.markdown("""
<style>
    .main-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B, #8500FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #888888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #1E1E24;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2D2D34;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF4B4B;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión para conexión
if "conn_server" not in st.session_state:
    st.session_state.conn_server = config.SERVER
if "conn_database" not in st.session_state:
    st.session_state.conn_database = config.DATABASE
if "conn_user" not in st.session_state:
    st.session_state.conn_user = config.USERNAME
if "conn_password" not in st.session_state:
    st.session_state.conn_password = config.PASSWORD
if "conn_driver" not in st.session_state:
    # Elegir driver por defecto o el primero instalado
    installed = get_installed_drivers()
    if config.DRIVER in installed:
        st.session_state.conn_driver = config.DRIVER
    elif installed:
        st.session_state.conn_driver = installed[0]
    else:
        st.session_state.conn_driver = config.DRIVER

# Sidebar - Configuración de Conexión
with st.sidebar:
    st.image("https://img.icons8.com/nolan/128/sql.png", width=70)
    st.markdown("### 🔌 Conexión SQL Server")
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
            st.success("¡Conexión establecida correctamente!")
            # Actualizar estado de sesión
            st.session_state.conn_server = server_input
            st.session_state.conn_database = db_input
            st.session_state.conn_user = user_input
            st.session_state.conn_password = pass_input
            st.session_state.conn_driver = driver_input
        else:
            st.error(f"Error de conexión:\n\n{msg}")

    if st.button("🔄 Refrescar Caché", use_container_width=True):
        st.cache_data.clear()
        st.success("¡Caché limpiada! Los datos se recargarán al instante.")

    st.markdown("---")
    st.markdown("🎓 **Administración de Bases de Datos**")
    st.markdown("Proyecto 1 — StreamUCV")
    st.caption("Fase 1 - Consulta del Diccionario de Datos")

# Parámetros activos de conexión
active_conn_params = {
    "server": st.session_state.conn_server,
    "database": st.session_state.conn_database,
    "username": st.session_state.conn_user,
    "password": st.session_state.conn_password,
    "driver": st.session_state.conn_driver
}

# Cabecera Principal
st.markdown('<h1 class="main-title">🎬 StreamUCV</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Módulo de Exploración Técnica del Diccionario de Datos de SQL Server</p>', unsafe_allow_html=True)

# Pestañas para cada requerimiento
tab_home, tab_r1, tab_r2, tab_r3, tab_r4, tab_r5, tab_r6, tab_r7, tab_r8, tab_r9, tab_r10 = st.tabs([
    "🏠 Inicio", 
    "R1: Tablas e Índices", 
    "R2: Conteos", 
    "R3: Restricciones", 
    "R4: Detalle Índices", 
    "R5: Triggers", 
    "R6: Tamaños Tablas", 
    "R7: Registros", 
    "R8: Columnas", 
    "R9: Bloqueos", 
    "R10: Costos"
])

# --- PESTAÑA INICIO ---
with tab_home:
    st.markdown("### Bienvenido al Sistema de Exploración")
    st.write(
        "Esta aplicación permite automatizar la auditoría de metadatos y análisis físicos "
        "de almacenamiento para la base de datos **StreamUCV** y el esquema **streaming** "
        "mediante consultas al Diccionario de Datos del motor Microsoft SQL Server."
    )
    
    st.markdown("#### Estado de la Conexión Activa")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        st.info(f"**Servidor:** `{active_conn_params['server']}`")
    with col_c2:
        st.info(f"**Base de Datos:** `{active_conn_params['database']}`")
    with col_c3:
        st.info(f"**Esquema de trabajo:** `{config.SCHEMA}`")
        
    st.markdown("#### Estructura General del Proyecto")
    st.markdown(
        """
        - **Capa Física de Datos:** 13 tablas relacionales pobladas con datos sintéticos realistas.
        - **Motor de Consultas D/D:** Queries modulares escritas en Python que consultan directamente vistas del sistema como `sys.tables`, `sys.indexes`, `sys.columns`, `sys.objects`, entre otras.
        - **Fórmulas de Bloqueo y Almacenamiento:** Basadas en páginas de datos de **8 KB** y velocidades de lectura promedio de **17 MB/s**.
        """
    )
    
    st.markdown("> **Nota Académica:** Puede alternar las credenciales en el menú lateral izquierdo si desea probar la portabilidad de la solución en otra instancia local de SQL Server.")

# --- PESTAÑA R1 ---
with tab_r1:
    st.markdown("### R1: Tablas e Índices Existentes")
    st.caption("Muestra las tablas registradas y todos los índices activos en el esquema streaming.")
    
    try:
        df_tablas, df_indices = cached_get_tablas_y_indices(active_conn_params)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader(f"Tablas Registradas ({len(df_tablas)})")
            st.dataframe(df_tablas, use_container_width=True)
            
        with col_t2:
            st.subheader(f"Índices Activos ({len(df_indices)})")
            st.dataframe(df_indices, use_container_width=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R1: {e}")

# --- PESTAÑA R2 ---
with tab_r2:
    st.markdown("### R2: Cantidad de Tablas y Conteo de Índices por Tabla")
    
    try:
        total_tablas, df_conteo = cached_get_conteo_tablas_indices(active_conn_params)
        
        # Tarjeta métrica
        st.markdown(
            f"""
            <div class="metric-card" style="margin-bottom: 20px;">
                <div class="metric-label">Cantidad Total de Tablas</div>
                <div class="metric-value">{total_tablas}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        col_r2_1, col_r2_2 = st.columns([2, 3])
        with col_r2_1:
            st.subheader("Índices por Tabla")
            st.dataframe(df_conteo, use_container_width=True, hide_index=True)
        with col_r2_2:
            st.subheader("Gráfico de Distribución de Índices")
            # Configurar tabla para gráfico streamlit
            chart_data = df_conteo.set_index("Tabla")
            st.bar_chart(chart_data)
            
    except Exception as e:
        st.error(f"Error al ejecutar consulta R2: {e}")

# --- PESTAÑA R3 ---
with tab_r3:
    st.markdown("### R3: Restricciones en el Esquema")
    st.caption("Detalle de restricciones (claves primarias, foráneas, checks y defaults) encontradas en el esquema.")
    
    try:
        df_rest = cached_get_restricciones(active_conn_params)
        
        # Filtros interactivos
        tipos_disponibles = ["TODAS"] + list(df_rest["Tipo de Restricción"].unique())
        filtro_tipo = st.selectbox("Filtrar por Tipo de Restricción", options=tipos_disponibles)
        
        if filtro_tipo != "TODAS":
            df_mostrar = df_rest[df_rest["Tipo de Restricción"] == filtro_tipo]
        else:
            df_mostrar = df_rest
            
        st.markdown(f"**Total encontradas:** {len(df_mostrar)}")
        st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R3: {e}")

# --- PESTAÑA R4 ---
with tab_r4:
    st.markdown("### R4: Detalles de Estructura de Índices")
    st.caption("Muestra las columnas que conforman cada índice, si es único o clave primaria, y el factor de relleno.")
    
    try:
        df_det = cached_get_detalle_indices(active_conn_params)
        st.dataframe(df_det, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R4: {e}")

# --- PESTAÑA R5 ---
with tab_r5:
    st.markdown("### R5: Triggers Activos en el Esquema")
    
    try:
        df_trig = cached_get_triggers(active_conn_params)
        if df_trig.empty:
            st.info("ℹ️ No se encontraron triggers definidos en el esquema streaming de la base de datos.")
        else:
            st.dataframe(df_trig, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R5: {e}")

# --- PESTAÑA R6 ---
with tab_r6:
    st.markdown("### R6: Tamaño Ocupado por las Tablas en Disco")
    st.caption("Espacio físico consumido en páginas de datos y almacenamiento en disco.")
    
    try:
        df_tam = cached_get_tamano_tablas(active_conn_params)
        st.dataframe(df_tam, use_container_width=True, hide_index=True)
        
        # Gráfico comparativo de tamaño
        st.subheader("Comparativa de Tamaño Total Usado (KB)")
        chart_tam = df_tam.set_index("Tabla")[["Total Usado (KB)"]]
        st.bar_chart(chart_tam)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R6: {e}")

# --- PESTAÑA R7 ---
with tab_r7:
    st.markdown("### R7: Estimación del Tamaño de Registro en Bytes")
    st.caption("Tamaño calculado sumando los límites máximos definidos para cada tipo de dato de las columnas.")
    
    try:
        df_reg = cached_get_tamano_registro_por_tabla(active_conn_params)
        st.dataframe(df_reg, use_container_width=True, hide_index=True)
        
        st.info("💡 Fórmulas físicas de diseño de bases de datos: Un tamaño de registro menor permite un factor de bloqueo más alto y, por ende, menos accesos físicos de entrada/salida (I/O) a disco.")
    except Exception as e:
        st.error(f"Error al ejecutar consulta R7: {e}")

# --- PESTAÑA R8 ---
with tab_r8:
    st.markdown("### R8: Tamaño de Columnas por Tipo de Dato")
    st.caption("Desglose detallado del tamaño en bytes para cada columna de acuerdo a su definición física de almacenamiento.")
    
    try:
        df_cols = cached_get_tamano_columnas(active_conn_params)
        
        tablas_disponibles = ["TODAS"] + list(df_cols["Tabla"].unique())
        tabla_select = st.selectbox("Filtrar por Tabla", options=tablas_disponibles)
        
        if tabla_select != "TODAS":
            df_cols_mostrar = df_cols[df_cols["Tabla"] == tabla_select]
        else:
            df_cols_mostrar = df_cols
            
        st.dataframe(df_cols_mostrar, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R8: {e}")

# --- PESTAÑA R9 ---
with tab_r9:
    st.markdown("### R9: Factor de Bloqueo (Tablas e Índices)")
    st.caption("Determina la cantidad de registros que pueden almacenarse físicamente dentro de una página de datos de 8 KB.")
    
    try:
        df_t_fb, df_i_fb = cached_get_factor_bloqueo(active_conn_params)
        
        col_fb1, col_fb2 = st.columns(2)
        with col_fb1:
            st.subheader("Factor de Bloqueo por Tabla")
            st.dataframe(df_t_fb, use_container_width=True, hide_index=True)
        with col_fb2:
            st.subheader("Factor de Bloqueo por Índice")
            st.dataframe(df_i_fb, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al ejecutar consulta R9: {e}")

# --- PESTAÑA R10 ---
with tab_r10:
    st.markdown("### R10: Estimador de Costos e Índices Utilizables")
    st.caption("Simulador para consultas de igualdad. Evalúa si hay índices en la columna y estima el costo de I/O y tiempo de ejecución.")
    
    try:
        # Obtener mapa de tablas y columnas para los selectores
        mapa_estructuras = cached_get_tables_and_columns(active_conn_params)
        
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            tabla_select = st.selectbox("Selecciona la Tabla", options=list(mapa_estructuras.keys()))
        with col_sel2:
            columnas_select = mapa_estructuras.get(tabla_select, [])
            columna_select = st.selectbox("Selecciona la Columna de búsqueda", options=columnas_select)
            
        st.markdown("---")
        st.subheader("Resultado de la Estimación")
        
        # Calcular costos
        costos = cached_estimate_query_cost(tabla_select, columna_select, active_conn_params)
        
        if "error" in costos:
            st.error(costos["error"])
        else:
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Total Filas", f"{costos['total_filas']:,}")
            with col_m2:
                st.metric("Páginas de la Tabla", f"{costos['total_paginas']:,}")
            with col_m3:
                st.metric("Tamaño Registro", f"{costos['tamano_registro']} Bytes")
            with col_m4:
                st.metric("Factor de Bloqueo", f"{costos['factor_bloqueo']} reg/pág")
                
            # Tarjeta de Índice
            if costos["indice_existe"]:
                detalles = costos["indice_detalles"]
                st.success(
                    f"🎯 **Índice Utilizable Encontrado:** `{detalles['nombre']}`\n\n"
                    f"- **Tipo:** {detalles['tipo']}\n"
                    f"- **Único:** {detalles['unico']}\n"
                    f"- **Clave Primaria:** {detalles['pk']}"
                )
            else:
                st.warning("⚠️ **No existe ningún índice** en esta columna que permita una búsqueda directa (Index Seek). Se requerirá un escaneo secuencial completo (Full Table Scan).")
                
            # Tabla de comparación de costos
            st.subheader("Comparación de Rendimiento Físico")
            
            c_scan = costos["costo_scan"]
            c_seek = costos["costo_seek"]
            
            comparacion = {
                "Métrica": ["Accesos a Disco (Páginas)", "Tiempo Estimado (Segundos)"],
                "Búsqueda Secuencial (FTS)": [f"{c_scan['accesos']:,}", f"{c_scan['tiempo_segundos']:.6f} s"]
            }
            
            if costos["indice_existe"]:
                comparacion["Búsqueda Indexada (Seek)"] = [f"{c_seek['accesos']:,}", f"{c_seek['tiempo_segundos']:.6f} s"]
                # Calcular mejora
                dif_accesos = c_scan['accesos'] - c_seek['accesos']
                dif_porc = (dif_accesos / max(1, c_scan['accesos'])) * 100
                st.info(f"🚀 **Mejora estimada:** Reducción del **{dif_porc:.2f}%** en accesos a disco e impacto temporal.")
            else:
                comparacion["Búsqueda Indexada (Seek)"] = ["N/A", "N/A"]
                
            df_comp = pd.DataFrame(comparacion)
            st.table(df_comp)
            
    except Exception as e:
        st.error(f"Error al inicializar el comparador R10: {e}")
