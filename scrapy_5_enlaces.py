import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

url = "https://en.wikipedia.org/wiki/Linux"

# Hacer la petición HTTP con headers para evitar bloqueos
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
html = response.text

soup = bs(html, "lxml")

#content = soup.find("div", id="mw-content-text")

links = []

for a in soup.find_all("a", href=True):
    links.append({"texto": a.get_text(strip=True), "url": a["href"]})
    
    
    
df = pd.DataFrame(links)
df.to_excel("links_linux.xlsx", index=False)
print("Archivo 'links_linux.xlsx' generado correctamente")