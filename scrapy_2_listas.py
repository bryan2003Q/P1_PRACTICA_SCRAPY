import requests
import pandas as pd
from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

headers={
    "User-Agent":"Mozilla/5.0"
}

response=requests.get(url, headers=headers)
html=response.text

soup=BeautifulSoup(html,"lxml")

items=[li.get_text(strip=True)for li in soup.find_all("li")]

df=pd.DataFrame(items,columns=["Elemento"])
df.to_excel("elementos_items.xlsx",index=False)
print("Archivo 'elementos_items.xlsx' generado correctamente")
