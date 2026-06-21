import streamlit as st
import pandas as pd
from app.ui.pages._shared import inject_sidebar, get_conn_params, render_back_button, cached_get_tables_and_columns, cached_estimate_query_cost

# Inyectar sidebar
inject_sidebar()

st.markdown('<h2 class="page-title">Estimador de Costo de Consulta</h2>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Dada una consulta de igualdad sobre un campo, evalúa la presencia de índices utilizables y calcula el costo en accesos a disco (páginas) y tiempo estimado de ejecución.</p>', unsafe_allow_html=True)

params = get_conn_params()

try:
    mapa_estructuras = cached_get_tables_and_columns(params)
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        tabla_select = st.selectbox("Selecciona la Tabla", options=list(mapa_estructuras.keys()))
    with col_sel2:
        columnas_select = mapa_estructuras.get(tabla_select, [])
        columna_select = st.selectbox("Selecciona la Columna de búsqueda", options=columnas_select)
        
    st.markdown("---")
    st.subheader("Resultado de la Estimación")
    
    costos = cached_estimate_query_cost(tabla_select, columna_select, params)
    
    if "error" in costos:
        st.error(costos["error"])
    else:
        # Fila de métricas usando tarjetas personalizadas
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Filas</div>
                <div class="metric-value">{costos['total_filas']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Páginas de la Tabla</div>
                <div class="metric-value">{costos['total_paginas']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Tamaño Registro</div>
                <div class="metric-value">{costos['tamano_registro']} B</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Factor de Bloqueo</div>
                <div class="metric-value">{costos['factor_bloqueo']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Estado de Índice Utilizable
        if costos["indice_existe"]:
            detalles = costos["indice_detalles"]
            st.markdown(f"""
            <div class="info-banner" style="border-left-color: #10B981; background-color: rgba(16, 185, 129, 0.1);">
                <p class="info-banner-text" style="color: #10B981; font-weight: 600;">
                    Índice Utilizable Encontrado: {detalles['nombre']}
                </p>
                <p class="info-banner-text" style="margin-top: 0.25rem;">
                    Tipo: {detalles['tipo']} | Único: {detalles['unico']} | Clave Primaria: {detalles['pk']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-banner" style="border-left-color: #F59E0B; background-color: rgba(245, 158, 11, 0.1);">
                <p class="info-banner-text" style="color: #F59E0B; font-weight: 600;">
                    No existe ningún índice en esta columna que permita una búsqueda directa (Index Seek).
                </p>
                <p class="info-banner-text" style="margin-top: 0.25rem;">
                    Se requerirá un escaneo secuencial completo de la tabla (Full Table Scan).
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # Tabla comparativa de costos
        st.subheader("Comparación de Rendimiento Físico")
        
        c_scan = costos["costo_scan"]
        c_seek = costos["costo_seek"]
        
        comparacion = {
            "Métrica": ["Accesos a Disco (Páginas)", "Tiempo Estimado (Segundos)"],
            "Búsqueda Secuencial (FTS)": [f"{c_scan['accesos']:,}", f"{c_scan['tiempo_segundos']:.6f} s"]
        }
        
        if costos["indice_existe"]:
            comparacion["Búsqueda Indexada (Seek)"] = [f"{c_seek['accesos']:,}", f"{c_seek['tiempo_segundos']:.6f} s"]
            
            # Calcular la mejora en accesos
            dif_accesos = c_scan['accesos'] - c_seek['accesos']
            dif_porc = (dif_accesos / max(1, c_scan['accesos'])) * 100
            
            st.markdown(f"""
            <div class="info-banner">
                <p class="info-banner-text">
                    <strong>Mejora estimada:</strong> Reducción del <strong>{dif_porc:.2f}%</strong> en accesos a disco e impacto temporal.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            comparacion["Búsqueda Indexada (Seek)"] = ["N/A", "N/A"]
            
        df_comp = pd.DataFrame(comparacion)
        st.table(df_comp)
        
except Exception as e:
    st.error(f"Error al ejecutar la consulta: {e}")

# Botón de retorno
render_back_button()
