'''
Mostrar un mapa con los resultados de las primarias 2025 en Chile
Cada región debe tener un color de acuerdo al candidato que ganó en ella.
Al hacer click en la región se debe mostrar a cada candidato, su porcentaje y cantidad de votos.
Este script se cargará en streamlit y se mostrará en la página de visualización.
'''
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

def mostrar_candidatos(candidatos, resultados):
    #Cargar el archivo estilos.css para mostrar los candidatos
    with open("estilos.css", encoding="utf-8") as f:
        estilos = f"<style>{f.read()}</style>"
    st.markdown(estilos, unsafe_allow_html=True)

    # Calcular votos totales por candidato
    total_votos = sum(resultados[region]['votos'] for region in resultados)
    candidatos_votos = []
    for candidato in candidatos:
        votos_totales = sum(
            resultados[region]['votos']
            for region in resultados
            if resultados[region]['candidato'] == candidato['nombre']
        )
        porcentaje = (votos_totales / total_votos) * 100 if total_votos > 0 else 0
        candidatos_votos.append({
            "candidato": candidato,
            "votos": votos_totales,
            "porcentaje": porcentaje
        })

    # Ordenar de mayor a menor cantidad de votos
    candidatos_votos.sort(key=lambda x: x["votos"], reverse=True)

    cols = st.columns(len(candidatos))
    for i, data in enumerate(candidatos_votos):
        candidato = data["candidato"]
        votos_totales = data["votos"]
        porcentaje = data["porcentaje"]
        color_borde = candidato['color_partido']
        imagen = candidato['imagen']
        logo = candidato['icono_partido']

        # Destacar al ganador con marco blanco grueso en toda la tarjeta
        card_style = (
            "box-shadow: 0 0 0 6px white;" if i == 0 else ""
        )

        html = f"""
        <div class="candidato-card" style="{card_style}">
            <div class="candidato-img-container">
                <img src="{imagen}" class="candidato-img" style="border-color:{color_borde};" />
                <img src="{logo}" class="logo-partido" />
            </div>
            <div class="candidato-nombre">{candidato['nombre']}</div>
            <div class="candidato-partido">{candidato['partido']}</div>
            <div class="candidato-votos">Votos Totales: {votos_totales:,}</div>
            <div class="candidato-porcentaje">{porcentaje:.2f}%</div>
            <div class="candidato-color-dot" style="color:{color_borde};">●</div>
        </div>
        """
        cols[i].markdown(html, unsafe_allow_html=True)

def cargar_mapa():
    import geopandas as gpd
    gpd.options.use_pygeos = True
    chile = gpd.read_file("fuentes/gadm41_CHL_1.shp")
    # Reproyectar a UTM 19S (metros)
    chile = chile.to_crs(epsg=32719)
    chile = chile.explode(index_parts=False)
    #Ajustar el mapa solo al territorio continental de Chile
    continente = chile[
        (chile.geometry.centroid.x > 50000) & (chile.geometry.centroid.x < 900000) 
    ].copy()
    # Opcional: volver al CRS original si lo necesitas
    # continente = continente.to_crs(epsg=4326)
    return continente

def mostrar_mapa(regiones, resultados):
    regiones = regiones.copy()
    regiones["color"] = regiones.index.map(lambda idx: resultados[idx]['color'])
    regiones["ganador"] = regiones.index.map(lambda idx: resultados[idx]['candidato'])

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    regiones.plot(ax=ax, color=regiones["color"], edgecolor="black", linewidth=0.3)

    from matplotlib.patches import Patch
    legend_elements = []
    candidatos_vistos = set()
    for idx in regiones.index:
        candidato = resultados[idx]['candidato']
        color = resultados[idx]['color']
        if candidato not in candidatos_vistos:
            legend_elements.append(Patch(facecolor=color, edgecolor='black', label=candidato))
            candidatos_vistos.add(candidato)
    legend = ax.legend(
        handles=legend_elements,
        title="Ganador por región",
        loc='lower left',
        bbox_to_anchor=(-0.7, 0),  # Fuera del área del mapa, ajusta el segundo valor si es necesario
        frameon=False,
        labelcolor='white',
        title_fontsize=7,
        fontsize=7,
        borderaxespad=0
    )
    legend.get_title().set_color('white')

    plt.title('Resultados de las Primarias Presidenciales 2025 en Chile', color='white')
    ax.set_axis_off()
    fig.patch.set_alpha(0)
    st.pyplot(fig, transparent=True)

