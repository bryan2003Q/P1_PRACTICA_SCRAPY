from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime

# 🔹 1. URL (AQUÍ PEGAS EL LINK QUE TE DÉ EL PROFESOR)
URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population"

# 🔹 2. Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get(URL)

# 🔹 3. Esperar a que las tablas carguen
wait = WebDriverWait(driver, 10)
tables = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.wikitable"))
)

print(f"Tablas encontradas: {len(tables)}")

# 🔹 4. Extraer cada tabla
for index, table in enumerate(tables):
    rows = table.find_elements(By.TAG_NAME, "tr")

    data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])

    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    
     # --- LIMPIEZA ---
    df = df.applymap(lambda x: x.replace('\n', ' ') if isinstance(x, str) else x)
    df.columns = df.iloc[0]  # primera fila como encabezado
    df = df[1:].reset_index(drop=True)
    
    
    #Imprimir y guardar
    
    print(f"\n📊 Tabla {index + 1}")
    print(df.to_string())
    
    #Guardar la tabla en csv
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"datos/tabla_{index+1}_{timestamp}.csv", index=False)

# 🔹 5. Cerrar navegador
driver.quit()
