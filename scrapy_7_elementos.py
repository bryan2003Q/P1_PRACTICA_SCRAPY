import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


url = "https://en.wikipedia.org/wiki/COVID-19_pandemic"
headers={"User-Agent":"Mozilla/5.0"}
response=requests.get(url, headers=headers)
html=response.text
soup=bs(html, "lxml")

elements=soup.find_all("div", class_="hatnote")

texts=[e.get_text(strip=True)[:500] for e in elements]
df=pd.DataFrame(texts, columns=["Contenido"])
df.to_excel("contenido_hatnote.xlsx", index=False)

print("Archivo 'contenido_hatnote.xlsx' generado correctamente")
