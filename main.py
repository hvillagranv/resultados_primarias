#Visualización general de la página
import streamlit as st
from visualizacion import cargar_mapa, mostrar_mapa, mostrar_candidatos
from candidatos import candidatos
import numpy as np
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Primarias Presidenciales 2025 - Chile",
    page_icon="🇨🇱",
    layout="wide"
)

# Título de la página
st.title("Primarias Presidenciales 2025 - Chile")

# Cargar el mapa de Chile
chile = cargar_mapa()
print(chile["NAME_1"].unique())
# Simulación de resultados (esto debería ser reemplazado por datos reales), con valores randomizados entre 100000 y 1000000
resultados = {
    region: {
        'candidato': candidatos[i % len(candidatos)]['nombre'],
        'color': candidatos[i % len(candidatos)]['color_partido'],
        'votos': np.random.randint(1000, 450000)

    }
    for i, region in enumerate(chile.index)
}

#Mostrar resultados generales de los candidatos
st.subheader("Resultados a Nivel Nacional")
#Obtener la hora de actualización y escribirla en la página
hora_actualizacion = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"**Última actualización:** {hora_actualizacion}")

mostrar_candidatos(candidatos, resultados)

# Mostrar el mapa con los resultados
mostrar_mapa(chile, resultados)



