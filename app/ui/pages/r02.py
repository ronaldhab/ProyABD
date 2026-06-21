import streamlit as st
from app.ui.styles import inject_styles
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_conteo_tablas_indices

# Inyectar estilos y sidebar
inject_styles()
inject_sidebar()

st.markdown('<h2 class="page-title">Cantidad de Tablas y Conteo de Índices por Tabla</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Indica la cantidad total de tablas y el conteo de índices asociados a cada una de ellas.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    total_tablas, df_conteo = cached_get_conteo_tablas_indices(params)
    
    # Tarjeta métrica de cantidad de tablas
    st.markdown(
        f"""
        <div class="metric-card" style="margin-bottom: 20px; max-width: 300px;">
            <div class="metric-label">Cantidad Total de Tablas</div>
            <div class="metric-value">{total_tablas}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col_r2_1, col_r2_2 = st.columns([2, 3])
    with col_r2_1:
        st.subheader("Conteo por Tabla")
        st.dataframe(df_conteo, use_container_width=True, hide_index=True)
    with col_r2_2:
        st.subheader("Distribución de Índices")
        chart_data = df_conteo.set_index("Tabla")
        st.bar_chart(chart_data)
        
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
