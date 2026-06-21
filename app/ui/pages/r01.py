import streamlit as st
from app.ui.styles import inject_styles
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_tablas_y_indices

# Inyectar estilos y sidebar
inject_styles()
inject_sidebar()

st.markdown('<h2 class="page-title">Listado de Tablas e Índices del Esquema</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Muestra las tablas registradas y todos los índices activos en el esquema streaming.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_tablas, df_indices = cached_get_tablas_y_indices(params)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader(f"Tablas Registradas ({len(df_tablas)})")
        st.dataframe(df_tablas, use_container_width=True, hide_index=True)
    
    with col_t2:
        st.subheader(f"Índices Activos ({len(df_indices)})")
        st.dataframe(df_indices, use_container_width=True, hide_index=True)
        
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
