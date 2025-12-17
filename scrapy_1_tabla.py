import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


url = "https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
html = response.text
soup = bs(html, "lxml")

tables = soup.find_all("table", class_="wikitable")
dfs = [pd.read_html(str(table))[0] for table in tables]

tablas_unidas = pd.concat(dfs, ignore_index=True)


tablas_unidas.to_excel("frases_latin.xlsx", index=False)
print("Archivo paises generado correctamente ")



