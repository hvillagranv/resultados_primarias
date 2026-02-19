# 🇨🇱 Resultados Primarias Presidenciales 2025 - Chile

Aplicación interactiva desarrollada con **Streamlit** para visualizar resultados simulados de las Primarias Presidenciales 2025 en Chile. Permite explorar los resultados a nivel nacional y regional, con un enfoque visual atractivo, responsivo y fácil de interpretar.

Se accede a través de [este enlace](https://resultados-primarias-2025.streamlit.app/)

---

## 🚀 Características

- 🔵 **Visualización nacional:** Tarjetas por candidato con total de votos y porcentaje.
- 🟢 **Visualización regional:** Selector por región que muestra los resultados individuales.
- 🗺 **Mapa interactivo:** Colorea cada región según el candidato ganador.
- 📱 **Diseño responsivo:** Adaptado para dispositivos móviles, tablet y escritorio.
- 🎨 **Estilos personalizados:** Uso de CSS para tarjetas, imágenes, layout y tipografía.

---

## 📁 Estructura del proyecto

```
resultados_primarias/
│
├── main.py                          # Script principal de la aplicación Streamlit
├── candidatos.py                   # Definición de candidatos y partidos
├── resultados.py                   # Lógica para calcular y mostrar resultados
├── utils.py                        # Funciones de transformación de datos
├── visualizacion_candidatos.py     # Funciones de visualización y estilos
├── estilos.css                     # Estilos personalizados para tarjetas e imágenes
├── fuentes/
│   └── gadm41_CHL_1.shp           # Shapefile con las regiones de Chile
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.8 o superior
- [Streamlit](https://streamlit.io/)
- geopandas
- matplotlib
- pandas
- numpy

Instala las dependencias ejecutando:

```bash
pip install streamlit geopandas matplotlib pandas numpy
```

---

## ▶️ Uso

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/resultados_primarias.git
   cd resultados_primarias
   ```

2. **Verifica el shapefile**: Asegúrate de tener el archivo `gadm41_CHL_1.shp` y sus archivos asociados (`.dbf`, `.shx`, etc.) en la carpeta `fuentes/`. Los cuales se pueden descargan en https://gadm.org/download_country.html

3. **Ejecuta la aplicación**:

   ```bash
   streamlit run main.py
   ```

4. **Abre la URL** que te indique Streamlit (por ejemplo: `http://localhost:8501`) en tu navegador.

---

## 🎨 Personalización

- **Modificar candidatos:** Edita el archivo `candidatos.py` para cambiar nombres, partidos, colores, imágenes, etc.
- **Editar estilos visuales:** Modifica `estilos.css` para adaptar la apariencia de las tarjetas, márgenes, bordes o fuentes.
- **Actualizar regiones:** Asegúrate de que el shapefile contenga las 16 regiones de Chile. Puedes reemplazar `gadm41_CHL_1.shp` por uno actualizado.

---

## 📚 Créditos

Desarrollado por Hans Villagrán con fines **demostrativos**.  
Los resultados presentados son completamente simulados y **no representan cifras reales, antes de la elección.**

## ✅ TO DO

- [ ] Agregar visualización de resultados por grandes zonas (Gran Santiago, Gran Valparaíso, Gran Concepción).
- [ ] Incluir porcentaje de conteo y fecha de actualización
- [ ] Hacer que el mapa sea interactivo para quitar el selector y mejorar la navegación del sitio.
