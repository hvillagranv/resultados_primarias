'''
Mostrar un mapa con los resultados de las primarias 2025 en Chile
Cada región debe tener un color de acuerdo al candidato que ganó en ella.
Al hacer click en la región se debe mostrar a cada candidato, su porcentaje y cantidad de votos.
Este script se cargará en streamlit y se mostrará en la página de visualización.
'''
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import os

def mostrar_candidatos(candidatos, resultados, votos_por_region):
    import streamlit as st

    # Cargar estilos CSS
    with open("estilos.css", encoding="utf-8") as f:
        estilos = f"<style>{f.read()}</style>"
    st.markdown(estilos, unsafe_allow_html=True)

    # Votos nacionales totales por candidato, incluyendo extranjero
    votos_nacionales = votos_por_region.get("Total Nacional", {})
    votos_extranjero = votos_por_region.get("EXTRANJERO", {})

    votos_combinados = {}
    for nombre in set(votos_nacionales.keys()).union(votos_extranjero.keys()):
        votos_combinados[nombre] = votos_nacionales.get(nombre, 0) + votos_extranjero.get(nombre, 0)

    total_votos = sum(votos_combinados.values())

    candidatos_votos = []
    for candidato in candidatos:
        nombre = candidato["nombre"]
        votos_totales = votos_nacionales.get(nombre, 0)
        porcentaje = (votos_totales / total_votos) * 100 if total_votos > 0 else 0
        candidatos_votos.append({
            "candidato": candidato,
            "votos": votos_totales,
            "porcentaje": porcentaje
        })

    # Ordenar candidatos por votos
    candidatos_votos.sort(key=lambda x: x["votos"], reverse=True)

    # Mostrar tarjetas con resultados
    st.markdown("### Resultados Nacionales (incluye votos en el extranjero)")

    cols = st.columns(len(candidatos))
    for i, data in enumerate(candidatos_votos):
        candidato = data["candidato"]
        votos_totales = data["votos"]
        porcentaje = data["porcentaje"]
        color_borde = candidato['color_partido']
        imagen = candidato['imagen']
        logo = candidato['icono_partido']

        card_style = (
            "box-shadow: 0 0 0 6px white; margin-bottom:" if i == 0 else ""
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
        </div>
        """
        cols[i].markdown(html, unsafe_allow_html=True)


@st.cache_data
def cargar_mapa():
    """
    Carga y transforma el mapa de regiones de Chile desde SHP o GeoJSON.
    Si no existe el archivo GeoJSON simplificado, lo genera automáticamente.
    Retorna: GeoDataFrame con geometrías simplificadas en EPSG:4326.
    """
    ruta_geojson = "fuentes/regiones_chile.geojson"
    ruta_shapefile = "fuentes/gadm41_CHL_1.shp"

    if os.path.exists(ruta_geojson):
        chile = gpd.read_file(ruta_geojson)
        return chile

    # Si no existe el GeoJSON, generar desde SHP
    print("🔄 Generando GeoJSON desde shapefile...")
    gdf = gpd.read_file(ruta_shapefile)

    # Proyección a UTM zona 19S (Chile continental)
    gdf = gdf.to_crs(epsg=32719)

    # Unificar geometrías multipart
    gdf = gdf.explode(index_parts=False)

    # Simplificar geometría
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=1000, preserve_topology=True)

    # Filtrar solo el continente
    gdf = gdf[
        (gdf.geometry.centroid.x > 50000) & (gdf.geometry.centroid.x < 900000)
    ].copy()

    # Reproyectar a WGS84 para uso en web
    gdf = gdf.to_crs(epsg=4326)

    # 🔧 Agrupar por nombre de región para unir geometrías disjuntas
    gdf = gdf.dissolve(by="NAME_1", as_index=True)
    gdf.index.name = None
    gdf = gdf.reset_index()

    os.makedirs("fuentes", exist_ok=True)
    gdf.to_file(ruta_geojson, driver="GeoJSON")
    print(f"✅ GeoJSON agrupado guardado en: {ruta_geojson}")

    return gdf

def mostrar_mapa(regiones, resultados):
    import matplotlib.pyplot as plt
    import streamlit as st
    from matplotlib.patches import Patch

    regiones = regiones.copy()
    regiones = regiones.set_index("NAME_1")

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

    # Mapear colores y ganadores usando nombre normalizado para buscar en resultados
    regiones["color"] = regiones.index.map(
        lambda nombre: resultados.get(normalizar_nombre_region(nombre), {}).get('color', '#CCCCCC')
    )
    regiones["ganador"] = regiones.index.map(
        lambda nombre: resultados.get(normalizar_nombre_region(nombre), {}).get('candidato', 'Sin datos')
    )

    fig, ax = plt.subplots(1, 1, figsize=(6,12))
    regiones.plot(ax=ax, color=regiones["color"], edgecolor="black", linewidth=0.3)

    # Recortar el eje Y para expandir verticalmente el mapa
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    rango = ylim[1] - ylim[0]
    padding = rango * 0.05
    ax.set_ylim(ylim[0] - padding, ylim[1] + padding)

    plt.subplots_adjust(left=0, right=0.6, top=1, bottom=0)

    legend_elements = []
    candidatos_vistos = set()
    for idx in regiones.index:
        nombre_normalizado = normalizar_nombre_region(idx)
        candidato = resultados.get(nombre_normalizado, {}).get('candidato', None)
        color = resultados.get(nombre_normalizado, {}).get('color', None)
        if candidato and candidato not in candidatos_vistos:
            legend_elements.append(Patch(facecolor=color, edgecolor='black', label=candidato))
            candidatos_vistos.add(candidato)

    legend = ax.legend(
        handles=legend_elements,
        title="Ganador por región",
        loc='lower left',
        bbox_to_anchor=(-0.7, 0),
        frameon=False,
        labelcolor='white',
        title_fontsize=16,
        fontsize=12,
        borderaxespad=0
    )
    legend.get_title().set_color('white')

    plt.title(
        'Resultados de las Primarias Presidenciales\n2025 a nivel regional',
        color='white',
        multialignment='center'
    )
    ax.set_axis_off()
    fig.patch.set_alpha(0)
    st.pyplot(fig, transparent=True)
