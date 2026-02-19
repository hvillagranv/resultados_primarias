import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Diccionario de contexto compartido
contexto = {
    "fecha_datos": None,
    "resultados": []
}

# Función para extraer fecha de los datos
def obtener_fecha_datos(driver, wait):
    try:
        fecha_elemento = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-pie"))
        )
        texto_fecha = fecha_elemento.text.strip()
        if texto_fecha.lower().startswith("datos del"):
            texto_fecha = texto_fecha[10:].strip()
        return texto_fecha
    except Exception as e:
        print(f"⚠️ No se pudo obtener la fecha: {e}")
        return "FECHA_DESCONOCIDA"

# Configurar Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get("https://elecciones.servel.cl/")

# Clic en "Presidente"
boton_presidente = wait.until(
    EC.element_to_be_clickable((By.XPATH, '//button[span[text()="Presidente"]]'))
)
boton_presidente.click()

# Obtener fecha
contexto["fecha_datos"] = obtener_fecha_datos(driver, wait)
print(f"🕓 Fecha de los datos: {contexto['fecha_datos']}")

# Mostrar select y acceder a "División Geográfica Chile"
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Total Votación"]'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="División Geográfica Chile"]'))).click()

# Obtener comunas desde el 3er select
selects = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select.combo.text-filtros')))
if len(selects) < 3:
    raise Exception("No se encontró el tercer select de comunas.")

select_comunas = Select(selects[2])
comunas = [
    option.text.strip()
    for option in select_comunas.options
    if option.text.strip() and option.text.strip().upper() != "SELECCIONAR"
]

# Iterar por comunas
for comuna in comunas:
    print(f"\n📍 Procesando comuna: {comuna}")

    # Recargar filtros por si se resetean
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Total Votación"]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="División Geográfica Chile"]'))).click()
    time.sleep(1)

    # Seleccionar comuna desde el tercer select
    selects = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select.combo.text-filtros')))
    select_comunas = Select(selects[2])
    select_comunas.select_by_visible_text(comuna)

    time.sleep(2)

    filas = driver.find_elements(By.CSS_SELECTOR, "tbody.divide-y > tr")
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) >= 4:
            contexto["resultados"].append({
                "Comuna": comuna,
                "Lista/Candidato": celdas[0].text.strip(),
                "Partido": celdas[1].text.strip(),
                "Votos": celdas[2].text.strip(),
                "Porcentaje": celdas[3].text.strip()
            })

    totales = driver.find_elements(By.CSS_SELECTOR, "tfoot.foot_tab tr")
    for fila in totales:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) >= 4:
            contexto["resultados"].append({
                "Comuna": comuna,
                "Lista/Candidato": celdas[0].text.strip(),
                "Partido": "",
                "Votos": celdas[2].text.strip(),
                "Porcentaje": celdas[3].text.strip()
            })

# Extranjero
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="En el Extranjero"]'))).click()
time.sleep(2)

filas = driver.find_elements(By.CSS_SELECTOR, "tbody.divide-y > tr")
for fila in filas:
    celdas = fila.find_elements(By.TAG_NAME, "td")
    if len(celdas) >= 4:
        contexto["resultados"].append({
            "Comuna": "EXTRANJERO",
            "Lista/Candidato": celdas[0].text.strip(),
            "Partido": celdas[1].text.strip(),
            "Votos": celdas[2].text.strip(),
            "Porcentaje": celdas[3].text.strip()
        })

totales = driver.find_elements(By.CSS_SELECTOR, "tfoot.foot_tab tr")
for fila in totales:
    celdas = fila.find_elements(By.TAG_NAME, "td")
    if len(celdas) >= 4:
        contexto["resultados"].append({
            "Comuna": "EXTRANJERO",
            "Lista/Candidato": celdas[0].text.strip(),
            "Partido": "",
            "Votos": celdas[2].text.strip(),
            "Porcentaje": celdas[3].text.strip()
        })

driver.quit()

# Guardar CSV
df = pd.DataFrame(contexto["resultados"])
df["Fecha Datos"] = contexto["fecha_datos"]
df["Votos"] = df["Votos"].str.replace(".", "", regex=False)
df["Votos"] = pd.to_numeric(df["Votos"], errors="coerce").fillna(0).astype(int)
df.to_csv("resultados_por_comuna.csv", index=False, encoding="utf-8-sig")
print("\n✅ Resultados guardados en resultados_por_comuna.csv")
