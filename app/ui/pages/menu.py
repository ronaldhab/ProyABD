import streamlit as st
from app.ui.styles import inject_styles
from app.ui.pages._shared import inject_sidebar, get_conn_params
from app import config

# Inyectar estilos globales y sidebar
inject_styles()
inject_sidebar()

st.markdown('<h1 class="page-title">🎬 StreamUCV</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Módulo de Exploración Técnica del Diccionario de Datos de SQL Server</p>', unsafe_allow_html=True)

# Sección de Estado de Conexión
params = get_conn_params()

st.markdown("### Estado de la Conexión Activa")
col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Servidor / Instancia</div>
        <div class="metric-value" style="font-size: 1.2rem; color: #E5E7EB; word-break: break-all;">{params['server']}</div>
    </div>
    """, unsafe_allow_html=True)
with col_c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Base de Datos</div>
        <div class="metric-value" style="font-size: 1.2rem; color: #E5E7EB;">{params['database']}</div>
    </div>
    """, unsafe_allow_html=True)
with col_c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Activo</div>
        <div class="metric-value" style="font-size: 1.2rem; color: #3A73C4;">{config.SCHEMA}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Navegación por Requerimientos")
st.markdown("Selecciona una opción a continuación para auditar y consultar metadatos del diccionario de datos:")

# Cuadrícula de opciones de navegación a las páginas R1 - R10
col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Listado de Tablas e Índices", use_container_width=True):
        st.switch_page("app/ui/pages/r01.py")
    if st.button("📊 Conteo de Tablas e Índices por Tabla", use_container_width=True):
        st.switch_page("app/ui/pages/r02.py")
    if st.button("🔑 Restricciones del Esquema", use_container_width=True):
        st.switch_page("app/ui/pages/r03.py")
    if st.button("🔍 Detalle de Columnas por Índice", use_container_width=True):
        st.switch_page("app/ui/pages/r04.py")
    if st.button("⚡ Triggers del Esquema", use_container_width=True):
        st.switch_page("app/ui/pages/r05.py")

with col2:
    if st.button("💾 Espacio Ocupado en Disco por Tabla", use_container_width=True):
        st.switch_page("app/ui/pages/r06.py")
    if st.button("📏 Estimación de Tamaño de Registro", use_container_width=True):
        st.switch_page("app/ui/pages/r07.py")
    if st.button("📐 Tamaño de Columnas por Tipo", use_container_width=True):
        st.switch_page("app/ui/pages/r08.py")
    if st.button("🔒 Factor de Bloqueo de Tablas e Índices", use_container_width=True):
        st.switch_page("app/ui/pages/r09.py")
    if st.button("🎯 Estimador de Costos e Índices Utilizables", use_container_width=True):
        st.switch_page("app/ui/pages/r10.py")

st.markdown("---")
st.markdown("### Acerca de la Aplicación")
st.write(
    "Esta herramienta automatiza el proceso de auditoría y optimización física para el "
    "esquema de base de datos **streaming**. Utiliza metadatos del Diccionario de Datos de SQL Server "
    "para calcular factores de bloqueo, estimar consumos de disco y evaluar la viabilidad "
    "de índices para optimizar consultas de búsqueda de igualdad."
)
