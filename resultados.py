# resultados.py

import streamlit as st
import numpy as np
from utils import (
    calcular_total_votos,
    calcular_porcentaje,
    obtener_candidato_ganador,
    obtener_color_candidato,
    obtener_mapeo_regiones,
    obtener_regiones_ordenadas
)

def generar_resultados(chile, candidatos):
    votos_por_region = {
    row["NAME_1"]: {
        c['nombre']: np.random.randint(1000, 250000)
        for c in candidatos
    }
    for _, row in chile.iterrows()
    }   

    resultados = {}
    for _, row in chile.iterrows():
        nombre_region = row["NAME_1"]
        votos_region = votos_por_region[nombre_region]
        total_votos = sum(votos_region.values())
        ganador = max(votos_region, key=votos_region.get)
        votos_ganador = votos_region[ganador]
        porcentaje = (votos_ganador / total_votos) * 100 if total_votos > 0 else 0
        color = next(c['color_partido'] for c in candidatos if c['nombre'] == ganador)

        resultados[nombre_region] = {
            "candidato": ganador,
            "color": color,
            "votos": votos_ganador,
            "porcentaje": porcentaje
        }

    return votos_por_region, resultados

def obtener_region_seleccionada(chile):
    nombres_regiones, _, mapeo_inverso = obtener_mapeo_regiones()
    regiones_ordenadas = obtener_regiones_ordenadas(chile)
    selected = st.selectbox("Selecciona una región:", regiones_ordenadas)
    return selected, mapeo_inverso.get(selected)

def obtener_candidatos_region(region_idx, votos_region, total_votos, candidatos):
    return sorted([
        {
            "candidato": c,
            "votos": votos_region[c['nombre']],
            "porcentaje": (votos_region[c['nombre']] / total_votos) * 100 if total_votos > 0 else 0
        }
        for c in candidatos
    ], key=lambda x: x["votos"], reverse=True)

def renderizar_tarjetas_candidatos(candidatos_votos, ganador):
    with st.container():
        filas = (len(candidatos_votos) + 1) // 2
        for i in range(filas):
            cols = st.columns(2)
            for j in range(2):
                idx = i * 2 + j
                if idx < len(candidatos_votos):
                    data = candidatos_votos[idx]
                    c = data["candidato"]
                    html = f"""
                    <div class="candidato-card" style="{'box-shadow: 0 0 0 6px white;' if c['nombre'] == ganador else ''}">
                        <div class="candidato-img-container">
                            <img src="{c['imagen']}" class="candidato-img" style="border-color:{c['color_partido']};" />
                            <img src="{c['icono_partido']}" class="logo-partido" />
                        </div>
                        <div class="candidato-nombre">{c['nombre']}</div>
                        <div class="candidato-partido">{c['partido']}</div>
                        <div class="candidato-votos">Votos: {data['votos']:,}</div>
                        <div class="candidato-porcentaje">{data['porcentaje']:.2f}%</div>
                    </div>
                    """
                    cols[j].markdown(html, unsafe_allow_html=True)

def mostrar_resultados_regionales(chile, votos_por_region, resultados, candidatos):
    selected_region, region_original = obtener_region_seleccionada(chile)
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    region_placeholder = st.empty()

    if region_original:
        region_data = chile[chile["NAME_1"] == region_original]
        if not region_data.empty:
            nombre_region = region_data["NAME_1"].values[0]
            votos_region = votos_por_region[nombre_region]
            ganador = resultados[nombre_region]['candidato']
            total = sum(votos_region.values())

            with region_placeholder:
                candidatos_votos = obtener_candidatos_region(nombre_region, votos_region, total, candidatos)
                renderizar_tarjetas_candidatos(candidatos_votos, ganador)