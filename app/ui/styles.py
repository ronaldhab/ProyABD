import streamlit as st

def inject_styles():
    """Inyecta los estilos CSS personalizados y fuentes de Google en la aplicación Streamlit."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap');

        :root {
            --navy-primary: #092C74;
            --blue-accent: #3A73C4;
            --bg-dark: #0A0E1A;
            --card-bg: #111827;
            --card-border: #1F2937;
            --text-primary: #E5E7EB;
            --text-secondary: #9CA3AF;
        }

        /* Tipografía global */
        html, body, .stMarkdown, p, label, table, tr, td, th {
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
        }

        /* Títulos de página con tipografía Montserrat y degradado */
        .page-title {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            font-size: 2.1rem;
            background: linear-gradient(135deg, #E5E7EB, var(--blue-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--navy-primary);
        }

        .page-subtitle {
            font-family: 'Inter', sans-serif;
            font-weight: 400;
            font-size: 1rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }

        /* Estilo para tarjetas métricas personalizadas */
        .metric-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid var(--card-border);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1rem;
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
            font-weight: 500;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--blue-accent);
            font-family: 'Montserrat', sans-serif;
        }

        /* Botón de retorno premium */
        .back-btn-container {
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid var(--card-border);
        }

        /* Banners y cajas informativas */
        .info-banner {
            background-color: rgba(9, 44, 116, 0.2);
            border-left: 4px solid var(--navy-primary);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1.5rem;
        }

        .info-banner-text {
            font-size: 0.95rem;
            color: var(--text-primary);
            line-height: 1.5;
            margin: 0;
        }

        /* Estilización de tablas y DataFrame de Streamlit */
        .stDataFrame {
            border: 1px solid var(--card-border) !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }

        /* Estilización de Botones en General (hacerlos más legibles y estilizados) */
        div.stButton > button {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            border-radius: 8px !important;
            border: 1px solid var(--navy-primary) !important;
            background-color: var(--card-bg) !important;
            color: var(--text-primary) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            padding: 0.4rem 0.8rem !important;
        }

        div.stButton > button:hover {
            border-color: var(--blue-accent) !important;
            color: #FFFFFF !important;
            background-color: var(--navy-primary) !important;
            box-shadow: 0 0 10px rgba(58, 115, 196, 0.3) !important;
            transform: translateY(-1.5px) !important;
        }
        
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Estilización de las Opciones en la Barra Lateral (Menú de Navegación) */
        [data-testid="stSidebarNav"] a * {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.92rem !important;
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] *,
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            color: var(--blue-accent) !important;
            font-weight: 600 !important;
        }

        /* Títulos de las secciones de la barra lateral (Inicio, Consultas) */
        [data-testid="stSidebarNavHeader"] {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.82rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: var(--blue-accent) !important;
        }

        /* Estilos para encabezados de expanders (Conexión SQL) sin interferir en iconos */
        [data-testid="stExpander"] details summary p {
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 0.92rem;
        }
    </style>
    """, unsafe_allow_html=True)
