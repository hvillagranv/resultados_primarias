# main.py
import streamlit as st
from visualizacion_candidatos import cargar_mapa, mostrar_mapa, mostrar_candidatos
from resultados import generar_resultados, mostrar_resultados_regionales
from candidatos import candidatos
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Primarias Presidenciales 2025 - Chile",
    page_icon="🇨🇱",
    layout="wide"
)

st.title("Primarias Presidenciales 2025 - Chile")

# Cargar datos
chile = cargar_mapa()
votos_por_region, resultados = generar_resultados(chile, candidatos,"resultados_por_comuna.csv")

# Mostrar resumen nacional
st.subheader("Resultados a Nivel Nacional")
#Obtener hora de actualización desde el Servel (hacer scraping)
hora_actualizacion = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"**Última actualización:** {hora_actualizacion}")
mostrar_candidatos(candidatos, resultados)
st.markdown('<div style="margin-top:32px"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    mostrar_mapa(chile, resultados)

with col2:
    st.subheader("Resultados Regionales")
    mostrar_resultados_regionales(chile, votos_por_region, resultados, candidatos)