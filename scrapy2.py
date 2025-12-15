# ==============================================
# SCRAPING COMPLETO DE TABLAS DE WIKIPEDIA
# ==============================================

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO
import datetime
import os

# ---------------- 1️⃣ URL --------------------
URL = "https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)"

# ---------------- 2️⃣ Configuración del navegador --------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(URL)


# ---------------- 3️⃣ Obtener HTML completo --------------------
html = driver.page_source  # HTML después de cargar la página
soup = bs(html, 'html.parser')

# ---------------- 4️⃣ Extraer todas las tablas --------------------
tablas = soup.find_all('table', class_='wikitable')

# Crear carpeta para guardar CSV si no existe
if not os.path.exists("datos"):
    os.makedirs("datos")

for index, tabla in enumerate(tablas):
    # Convertir tabla HTML a DataFrame usando StringIO (evita warning)
    df = pd.read_html(StringIO(str(tabla)))[0]
    
    # LIMPIEZA: quitar saltos de línea y asegurar que todo sea string
    df = df.astype(str).apply(lambda x: x.str.replace('\n', ' '))

  
    
    # IMPRIMIR tabla completa en consola
    print(f"\n📊 Tabla {index + 1}")
    print(df.to_string())
    
    # Guardar CSV con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = f"datos/tabla_{index+1}_{timestamp}.csv"
    df.to_csv(csv_name, index=False)
    print(f"✅ Tabla guardada en: {csv_name}")

# ---------------- 5️⃣ Cerrar navegador --------------------
driver.quit()
print("\n🏁 Scraping completado con éxito")
