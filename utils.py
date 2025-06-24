def calcular_total_votos(votos_region):
    return sum(votos_region.values())

def calcular_porcentaje(votos_candidato, total_votos):
    return (votos_candidato / total_votos) * 100 if total_votos > 0 else 0

def obtener_candidato_ganador(votos_region):
    return max(votos_region, key=votos_region.get)

def obtener_color_candidato(candidatos, nombre):
    for c in candidatos:
        if c['nombre'] == nombre:
            return c['color_partido']
    return "#CCCCCC"  # Color por defecto si no se encuentra

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
    return nombres_regiones.get(nombre_raw)

def obtener_mapeo_regiones():
    nombres = {
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
    orden = [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana de Santiago", "O'Higgins", "Maule",
        "Ñuble", "Biobío", "La Araucanía", "Los Ríos", "Los Lagos",
        "Aysén", "Magallanes"
    ]
    mapeo_inverso = {v: k for k, v in nombres.items()}
    return nombres, orden, mapeo_inverso

def obtener_regiones_ordenadas(chile):
    nombres, orden, _ = obtener_mapeo_regiones()
    corregidas = [nombres[r] for r in chile["NAME_1"] if r in nombres]
    return [r for r in orden if r in corregidas]