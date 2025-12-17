import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://en.wikipedia.org/wiki/Solar_System"


# Hacer la petición HTTP con headers para evitar bloqueos
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
html = response.text

soup=bs(html,"lxml")

images=[img["src"]for img in soup.find_all("img", src=True)]

df=pd.DataFrame(images, columns=["Imagen_URL"])
df.to_excel("imagenes_sistema_solar.xlsx", index=False)

print("Archivo 'imagenes_sistema_solar.xlsx' generado correctamente")