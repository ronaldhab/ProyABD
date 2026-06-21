import streamlit as st
from app.ui.styles import inject_styles
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_factor_bloqueo

# Inyectar estilos y sidebar
inject_styles()
inject_sidebar()

st.markdown('<h2 class="page-title">Factor de Bloqueo (Tablas e Índices)</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Determina la cantidad máxima de registros que pueden almacenarse físicamente en una página de datos o bloque de 8 KB (8192 bytes).</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_t_fb, df_i_fb = cached_get_factor_bloqueo(params)
    
    col_fb1, col_fb2 = st.columns(2)
    with col_fb1:
        st.subheader("Factor de Bloqueo por Tabla")
        st.dataframe(df_t_fb, use_container_width=True, hide_index=True)
    with col_fb2:
        st.subheader("Factor de Bloqueo por Índice")
        st.dataframe(df_i_fb, use_container_width=True, hide_index=True)
        
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
