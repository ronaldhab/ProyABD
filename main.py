import os
import sys

# Asegurar que el directorio raíz está en el path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    try:
        import streamlit.web.cli as stcli
        sys.argv = ["streamlit", "run", os.path.join(os.path.dirname(__file__), "app", "ui", "streamlit_app.py")]
        sys.exit(stcli.main())
    except ImportError:
        print("Streamlit no está instalado o no se puede importar directamente.")
        print("Por favor ejecute la aplicación usando: streamlit run app/ui/streamlit_app.py")
