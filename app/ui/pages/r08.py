import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_tamano_columnas

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Tamaño de Columnas por Tipo de Dato</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Desglose del tamaño en bytes para cada columna de acuerdo a su tipo de dato e información física del diccionario de datos.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_cols = cached_get_tamano_columnas(params)
    
    tablas_disponibles = ["TODAS"] + list(df_cols["Tabla"].unique())
    tabla_select = st.selectbox("Filtrar por Tabla", options=tablas_disponibles)
    
    if tabla_select != "TODAS":
        df_cols_mostrar = df_cols[df_cols["Tabla"] == tabla_select]
    else:
        df_cols_mostrar = df_cols
        
    st.dataframe(df_cols_mostrar, use_container_width=True, hide_index=True)
    
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
