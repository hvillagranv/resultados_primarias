# resultados.py

import streamlit as st
import numpy as np
import pandas as pd
from utils import (
    obtener_mapeo_regiones,
    obtener_regiones_ordenadas,
    normalizar_nombre_region,
)

def generar_resultados(chile, candidatos, archivo):
    import pandas as pd

    df = pd.read_csv(archivo, encoding="utf-8")
    df["Votos"] = df["Votos"].astype(str).str.replace(".", "", regex=False)
    df["Votos"] = pd.to_numeric(df["Votos"], errors="coerce").fillna(0).astype(int)

    # Mapas de nombres
    mapa_nombres = {
        "1 GONZALO WINTER ETCHEBERRY": "Gonzalo Winter",
        "2 JEANNETTE JARA ROMAN": "Jeannette Jara",
        "3 CAROLINA TOHA MORALES": "Carolina Tohá",
        "4 JAIME MULET MARTINEZ": "Jaime Mulet"
    }

    mapa_regiones = {
        "DE ARICA Y PARINACOTA": "Arica y Parinacota",
        "DE TARAPACA": "Tarapacá",
        "DE ANTOFAGASTA": "Antofagasta",
        "DE ATACAMA": "Atacama",
        "DE COQUIMBO": "Coquimbo",
        "DE VALPARAISO": "Valparaíso",
        "METROPOLITANA DE SANTIAGO": "Metropolitana de Santiago",
        "DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS": "O'Higgins",
        "DEL MAULE": "Maule",
        "DE ÑUBLE": "Ñuble",
        "DEL BIOBIO": "Biobío",
        "DE LA ARAUCANIA": "La Araucanía",
        "DE LOS RIOS": "Los Ríos",
        "DE LOS LAGOS": "Los Lagos",
        "DE AYSEN DEL GENERAL CARLOS IBAÑEZ DEL CAMPO": "Aysén",
        "DE MAGALLANES Y DE LA ANTARTICA CHILENA": "Magallanes"
    }

    # Reemplazo de nombres
    df["Lista/Candidato"] = df["Lista/Candidato"].replace(mapa_nombres)
    df["Región"] = df["Región"].replace(mapa_regiones)

    nombres_validos = list(mapa_nombres.values())
    df = df[df["Lista/Candidato"].isin(nombres_validos)]

    votos_por_region = {}
    for _, row in chile.iterrows():
        nombre_region_raw = row["NAME_1"]
        nombre_region = normalizar_nombre_region(nombre_region_raw) or nombre_region_raw

        df_region = df[df["Región"] == nombre_region]
        votos_region = {}

        for c in candidatos:
            nombre_candidato = c["nombre"]
            votos = df_region[df_region["Lista/Candidato"] == nombre_candidato]["Votos"].sum()
            votos_region[nombre_candidato] = votos

        votos_por_region[nombre_region] = votos_region

    # Agregar votos del extranjero como una región adicional
    votos_extranjero_region = {}
    for c in candidatos:
        nombre_candidato = c["nombre"]
        votos_extranjero = df[
            (df["Lista/Candidato"] == nombre_candidato) &
            (df["Región"].str.upper().str.contains("EXTRANJERO"))
        ]["Votos"].sum()
        votos_extranjero_region[nombre_candidato] = votos_extranjero

    votos_por_region["EXTRANJERO"] = votos_extranjero_region

    # Calcular resultados por región (incluye EXTRANJERO)
    resultados = {}
    for region, votos_region in votos_por_region.items():
        total_votos = sum(votos_region.values())
        if total_votos == 0:
            continue  # evitar regiones vacías
        ganador = max(votos_region, key=votos_region.get)
        votos_ganador = votos_region[ganador]
        porcentaje = (votos_ganador / total_votos) * 100
        color = next(c['color_partido'] for c in candidatos if c['nombre'] == ganador)

        resultados[region] = {
            "candidato": ganador,
            "color": color,
            "votos": votos_ganador,
            "porcentaje": porcentaje
        }

    # Total Nacional (suma de todas las regiones, incluye EXTRANJERO, excluye Total Nacional si existe)
    votos_nacionales = {}
    for c in candidatos:
        nombre_candidato = c["nombre"]
        votos_totales = sum(
            v.get(nombre_candidato, 0)
            for region, v in votos_por_region.items()
            if region != "Total Nacional"
        )
        votos_nacionales[nombre_candidato] = votos_totales

    total_votos_nacional = sum(votos_nacionales.values())
    ganador_nacional = max(votos_nacionales, key=votos_nacionales.get)
    votos_ganador_nacional = votos_nacionales[ganador_nacional]
    porcentaje_nacional = (votos_ganador_nacional / total_votos_nacional) * 100 if total_votos_nacional > 0 else 0
    color_nacional = next(c['color_partido'] for c in candidatos if c['nombre'] == ganador_nacional)

    resultados["Total Nacional"] = {
        "candidato": ganador_nacional,
        "color": color_nacional,
        "votos": votos_ganador_nacional,
        "porcentaje": porcentaje_nacional
    }
    votos_por_region["Total Nacional"] = votos_nacionales

    # Normalizar nombres de regiones
    votos_por_region_normalizado = {}
    resultados_normalizado = {}

    for region, votos in votos_por_region.items():
        region_normalizada = normalizar_nombre_region(region) or region
        votos_por_region_normalizado[region_normalizada] = votos

    for region, datos in resultados.items():
        region_normalizada = normalizar_nombre_region(region) or region
        resultados_normalizado[region_normalizada] = datos

    return votos_por_region_normalizado, resultados_normalizado

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
    import streamlit as st

    def normalizar_nombre_region(nombre_raw):
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
        return nombres_regiones.get(nombre_raw, nombre_raw)

    selected_region, region_original = obtener_region_seleccionada(chile)
    st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)
    region_placeholder = st.empty()

    if region_original:
        # Filtrar el GeoDataFrame con el nombre original
        region_data = chile[chile["NAME_1"] == region_original]
        if not region_data.empty:
            nombre_region_normalizado = normalizar_nombre_region(region_original)

            # Usar nombre normalizado para acceder a votos y resultados
            votos_region = votos_por_region.get(nombre_region_normalizado, {})
            ganador = resultados.get(nombre_region_normalizado, {}).get('candidato', None)
            total = sum(votos_region.values()) if votos_region else 0

            with region_placeholder:
                candidatos_votos = obtener_candidatos_region(nombre_region_normalizado, votos_region, total, candidatos)
                renderizar_tarjetas_candidatos(candidatos_votos, ganador)
