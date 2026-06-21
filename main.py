import streamlit as st

# Configuración de página centralizada (requerido al usar st.navigation)
st.set_page_config(
    page_title="StreamUCV — Data Dictionary Explorer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definición de las páginas del sistema
menu = st.Page("app/ui/pages/menu.py", title="Menú Principal", default=True)
r01  = st.Page("app/ui/pages/r01.py",  title="Listar Tablas e Índices")
r02  = st.Page("app/ui/pages/r02.py",  title="Conteo de Tablas e Índices")
r03  = st.Page("app/ui/pages/r03.py",  title="Consultar Restricciones del Esquema")
r04  = st.Page("app/ui/pages/r04.py",  title="Consultar Detalles de Índices")
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
