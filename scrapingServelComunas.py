import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import sys

# Asegura que la consola use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configuración del navegador
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# Abre la página
driver.get("https://elecciones.servel.cl/")

wait = WebDriverWait(driver, 30)

# Esperar que el botón "Presidente" esté presente
boton_presidente = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[span[text()="Presidente"]]'))
)

# Hacer clic en el botón
boton_presidente.click()

boton_div_geografica = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, '//button[text()="División Geográfica Chile"]'))
)
boton_div_geografica.click()

selects = WebDriverWait(driver, 3).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select.combo.text-filtros'))
)

# Convertirlo a un objeto Select
select_comunas_element = selects[2]
select_comunas = Select(select_comunas_element)

# Obtener todas las opciones excepto la que dice "Seleccionar"
comunas = [
    option.text.strip()
    for option in select_comunas.options
    if option.text.strip() and option.text.strip().upper() != "SELECCIONAR"
]

resultados = []

for comuna in comunas:
    print(f"\n📍 Procesando comuna: {comuna}")

    # Presionar botón "Total Votación"
    boton_total = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Total Votación"]'))
    )
    boton_total.click()

    # Presionar botón "División Geográfica Chile"
    boton_div_geo = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="División Geográfica Chile"]'))
    )
    boton_div_geo.click()

    time.sleep(0.5)  # Esperar un momento para que se actualice la tabla

    # Extraer filas de la tabla principal
    filas = driver.find_elements(By.CSS_SELECTOR, "tbody.divide-y > tr")
    for fila in filas:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) == 4:
            resultados.append({
                "Comuna": comuna,
                "Lista/Candidato": celdas[0].text.strip(),
                "Partido": celdas[1].text.strip(),
                "Votos": celdas[2].text.strip(),
                "Porcentaje": celdas[3].text.strip()
            })

    # Extraer totales del <tfoot>
    totales = driver.find_elements(By.CSS_SELECTOR, "tfoot.foot_tab tr")
    for fila in totales:
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) == 4:
            resultados.append({
                "Comuna": comuna,
                "Lista/Candidato": celdas[0].text.strip(),
                "Partido": "",
                "Votos": celdas[2].text.strip(),
                "Porcentaje": celdas[3].text.strip()
            })


# Cierra el navegador
driver.quit()

df = pd.DataFrame(resultados)
df.to_csv("resultados_por_comuna.csv", index=False, encoding="utf-8-sig")
print("\n✅ Resultados guardados en resultados_por_comuna.csv")
