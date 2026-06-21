import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_triggers

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Triggers Activos en el Esquema</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Lista los disparadores (triggers) asociados a las tablas del esquema streaming.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_trig = cached_get_triggers(params)
    if df_trig.empty:
        st.markdown("""
        <div class="info-banner">
            <p class="info-banner-text">No se encontraron triggers definidos en el esquema streaming de la base de datos.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.dataframe(df_trig, use_container_width=True, hide_index=True)
        
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
