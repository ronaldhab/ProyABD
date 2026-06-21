import streamlit as st
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_tamano_tablas

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Espacio Ocupado por cada Tabla en Disco</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Muestra el espacio en disco consumido por cada tabla en el esquema streaming, medido en cantidad de páginas y kilobytes.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    df_tam = cached_get_tamano_tablas(params)
    st.dataframe(df_tam, use_container_width=True, hide_index=True)
    
    st.subheader("Comparativa de Tamaño Usado (KB)")
    chart_data = df_tam.set_index("Tabla")[["Total Usado (KB)"]]
    st.bar_chart(chart_data)
    
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
