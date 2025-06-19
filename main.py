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
votos_por_region = {
    region: {
        candidato['nombre']: np.random.randint(1000, 250000)
        for candidato in candidatos
    }
    for region in chile.index
}

resultados = {}
for i, region in enumerate(chile.index):
    votos_region = votos_por_region[region]
    total_votos = sum(votos_region.values())
    ganador = max(votos_region, key=votos_region.get)
    votos_ganador = votos_region[ganador]
    porcentaje = (votos_ganador / total_votos) * 100 if total_votos > 0 else 0
    idx_candidato = next(idx for idx, c in enumerate(candidatos) if c['nombre'] == ganador)
    resultados[region] = {
        'candidato': ganador,
        'color': candidatos[idx_candidato]['color_partido'],
        'votos': votos_ganador,
        'porcentaje': porcentaje
    }

#Mostrar resultados generales de los candidatos
st.subheader("Resultados a Nivel Nacional")
#Obtener la hora de actualización y escribirla en la página
hora_actualizacion = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"**Última actualización:** {hora_actualizacion}")

mostrar_candidatos(candidatos, resultados)

# Calcular número de filas de candidatos para la visión nacional
filas_nacional = (len(candidatos) + 1) // 2
altura_fig = max(6, filas_nacional * 2.2)  # Ajusta el factor 2.2 según tu diseño

col1, col2 = st.columns([1, 2])  # 1/3 y 2/3

with col1:
    mostrar_mapa(chile, resultados)

with col2:
    st.subheader("Resultados Regionales")
    # Diccionario de nombres normalizados
    nombres_regiones = {
        "Arica y Parinacota": "Arica y Parinacota",
        "Tarapacá": "Tarapacá",
        "Antofagasta": "Antofagasta",
        "Atacama": "Atacama",
        "Coquimbo": "Coquimbo",
        "Valparaíso": "Valparaíso",
        "Santiago Metropolitan": "Metropolitana de Santiago",
        "Libertador General Bernardo O'Hi": "O'Higgins",
        "Maule": "Maule",
        "Ñuble": "Ñuble",
        "Bío-Bío": "Biobío",
        "Araucanía": "La Araucanía",
        "Los Ríos": "Los Ríos",
        "Los Lagos": "Los Lagos",
        "Aysén del General Ibañez del Cam": "Aysén",
        "Magallanes y Antártica Chilena": "Magallanes"
    }

    # Orden de norte a sur
    orden_norte_sur = [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana de Santiago", "O'Higgins", "Maule",
        "Ñuble", "Biobío", "La Araucanía", "Los Ríos", "Los Lagos",
        "Aysén", "Magallanes"
    ]

    # Crear mapeo inverso: nombre corregido -> nombre original
    mapeo_inverso = {v: k for k, v in nombres_regiones.items()}

    # Obtener nombres corregidos presentes en el DataFrame y ordenarlos
    regiones_corregidas = [nombres_regiones[r] for r in chile["NAME_1"] if r in nombres_regiones]
    regiones_ordenadas = [r for r in orden_norte_sur if r in regiones_corregidas]

    # Selector con nombres corregidos
    selected_region = st.selectbox("Selecciona una región:", regiones_ordenadas)
    region_placeholder = st.empty()  # Espacio reservado

    if selected_region:
        # Obtener el nombre original para filtrar datos
        region_original = mapeo_inverso[selected_region]
        region_data = chile[chile["NAME_1"] == region_original]
        if not region_data.empty:
            idx = region_data.index[0]
            with region_placeholder:
                st.markdown(f"**Región:** {selected_region}")
                st.markdown(f"**Candidato Ganador:** {resultados[idx]['candidato']}")
                st.markdown(f"**Votos Totales:** {sum(votos_por_region[idx].values()):,}")

                votos_region = votos_por_region[idx]
                total_votos = sum(votos_region.values())
                ganador = resultados[idx]['candidato']

                # Cargar estilos CSS (igual que en mostrar_candidatos)
                with open("estilos.css", encoding="utf-8") as f:
                    estilos = f"<style>{f.read()}</style>"
                st.markdown(estilos, unsafe_allow_html=True)

                # Preparar datos de candidatos regionales
                candidatos_votos = []
                for candidato in candidatos:
                    nombre = candidato['nombre']
                    votos = votos_region[nombre]
                    porcentaje = (votos / total_votos) * 100 if total_votos > 0 else 0
                    candidatos_votos.append({
                        "candidato": candidato,
                        "votos": votos,
                        "porcentaje": porcentaje
                    })

                # Ordenar de mayor a menor cantidad de votos regionales
                candidatos_votos.sort(key=lambda x: x["votos"], reverse=True)

                # Mostrar tarjetas de candidatos en filas de 2 (todas las filas)
                with st.container():
                    filas = (len(candidatos_votos) + 1) // 2
                    for i in range(filas):
                        cols = st.columns(2)
                        for j in range(2):
                            idx = i * 2 + j
                            if idx < len(candidatos_votos):
                                data = candidatos_votos[idx]
                                candidato = data["candidato"]
                                votos = data["votos"]
                                porcentaje = data["porcentaje"]
                                color_borde = candidato['color_partido']
                                imagen = candidato['imagen']
                                logo = candidato['icono_partido']

                                # Destacar al ganador regional con marco blanco grueso
                                card_style = (
                                    "box-shadow: 0 0 0 6px white;" if candidato['nombre'] == ganador else ""
                                )

                                html = f"""
                                <div class="candidato-card" style="{card_style}">
                                    <div class="candidato-img-container">
                                        <img src="{imagen}" class="candidato-img" style="border-color:{color_borde};" />
                                        <img src="{logo}" class="logo-partido" />
                                    </div>
                                    <div class="candidato-nombre">{candidato['nombre']}</div>
                                    <div class="candidato-partido">{candidato['partido']}</div>
                                    <div class="candidato-votos">Votos: {votos:,}</div>
                                    <div class="candidato-porcentaje">{porcentaje:.2f}%</div>
                                </div>
                                """
                                cols[j].markdown(html, unsafe_allow_html=True)
