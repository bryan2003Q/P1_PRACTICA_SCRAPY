import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
html = response.text

soup = bs(html, "lxml")

data = []

for a in soup.select("a[href]"):

    text = a.get_text(strip=True)
    href = a["href"]
    if text:  # Solo agregar si hay texto visible
        data.append({"texto": text, "url": href})

df = pd.DataFrame(data)
df.to_excel("texto_y_links_ai.xlsx", index=False)


print("Archivo 'texto_y_links_ai.xlsx' generado correctamente")