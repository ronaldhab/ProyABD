import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_detalle_indices

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Detalles de Estructura de Índices Existentes</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Visualiza la estructura interna de los índices: columnas que los conforman, unicidad y su factor de relleno (fill factor).</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_det = cached_get_detalle_indices(params)
    
    # Filtro interactivo opcional por tabla para mejorar la visualización
    tablas_disponibles = ["TODAS"] + list(df_det["Tabla"].unique())
    tabla_select = st.selectbox("Filtrar por Tabla", options=tablas_disponibles)
    
    if tabla_select != "TODAS":
        df_mostrar = df_det[df_det["Tabla"] == tabla_select]
    else:
        df_mostrar = df_det
        
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
    
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
