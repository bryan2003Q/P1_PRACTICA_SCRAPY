import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

url="https://en.wikipedia.org/wiki/Web_scraping"

headers={"User-Agent":"Mozilla/5.0"}

response=requests.get(url,headers=headers)
html=response.text
soup=bs(html,"lxml")

paragraphs=[p.get_text(strip=True) for p in soup.find_all("p")]
df=pd.DataFrame(paragraphs,columns=["Parrafo"])
df.to_excel("parrafos_web_scraping.xlsx", index=False)

print("Archivo 'parrafos_web_scraping.xlsx' generado correctamente")


