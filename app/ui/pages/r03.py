import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_restricciones

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Restricciones del Esquema</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Detalle de restricciones (claves primarias, foráneas, de verificación y predeterminadas) en el esquema streaming.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_rest = cached_get_restricciones(params)
    
    # Filtro de tipo de restricción
    tipos_disponibles = ["TODAS"] + list(df_rest["Tipo de Restricción"].unique())
    filtro_tipo = st.selectbox("Filtrar por Tipo de Restricción", options=tipos_disponibles)
    
    if filtro_tipo != "TODAS":
        df_mostrar = df_rest[df_rest["Tipo de Restricción"] == filtro_tipo]
    else:
        df_mostrar = df_rest
        
    st.markdown(f"**Total encontradas:** {len(df_mostrar)}")
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
    
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
