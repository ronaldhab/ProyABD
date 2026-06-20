# main.py - Versión simplificada
import streamlit as st

# Tu código de la aplicación aquí
st.set_page_config(page_title="StreamUCV", layout="wide")
st.title("StreamUCV - Aplicación")

# Importa y ejecuta tu app principal
from app.ui.streamlit_app import main
main()