import streamlit as st
from app.ui.styles import inject_styles

# Configuración de página centralizada (requerido al usar st.navigation)
st.set_page_config(
    page_title="StreamUCV — Data Dictionary Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyectar fuentes Google a nivel global una sola vez para evitar parpadeos en transiciones (FOUT)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Inyectar estilos CSS personalizados a nivel global
inject_styles()

# Definición de las páginas del sistema
menu = st.Page("app/ui/pages/menu.py", title="Menú Principal", default=True)
r01  = st.Page("app/ui/pages/r01.py",  title="Listar Tablas e Índices")
r02  = st.Page("app/ui/pages/r02.py",  title="Contabilizar Tablas e Índices")
r03  = st.Page("app/ui/pages/r03.py",  title="Examinar Restricciones del Esquema")
r04  = st.Page("app/ui/pages/r04.py",  title="Inspeccionar Detalles de Índices")
r05  = st.Page("app/ui/pages/r05.py",  title="Verificar Triggers del Esquema")
r06  = st.Page("app/ui/pages/r06.py",  title="Consultar Tamaño de Tablas")
r07  = st.Page("app/ui/pages/r07.py",  title="Estimar Tamaño de Registro por Tabla")
r08  = st.Page("app/ui/pages/r08.py",  title="Consultar Tamaño de Columnas")
r09  = st.Page("app/ui/pages/r09.py",  title="Verificar el Factor de Bloqueo de Tablas e Índices")
r10  = st.Page("app/ui/pages/r10.py",  title="Calcular Costo de Consulta")

# Agrupación y ejecución de la navegación
pg = st.navigation({
    "Inicio": [menu],
    "Consultas": [r01, r02, r03, r04, r05, r06, r07, r08, r09, r10]
})
pg.run()
