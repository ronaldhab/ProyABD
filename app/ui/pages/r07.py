import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_tamano_registro_por_tabla

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Estimación del Tamaño de Registro Por Tabla</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Calcula el tamaño máximo estimado de una fila o registro para cada tabla sumando los límites de tamaño físico de cada tipo de dato de sus columnas.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_reg = cached_get_tamano_registro_por_tabla(params)
    st.dataframe(df_reg, use_container_width=True, hide_index=True)
    
    st.markdown("""
    <div class="info-banner">
        <p class="info-banner-text">
            <strong>Criterio de cálculo:</strong> Un tamaño de registro menor permite un factor de bloqueo más alto 
            y, por lo tanto, reduce el número de accesos físicos de entrada/salida (I/O) a disco para las consultas secuenciales.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
