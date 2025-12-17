import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from collections import Counter
import math


url = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
headers = {"User-Agent": "Mozilla/5.0"}


response=requests.get(url, headers=headers)
html=response.text

soup=bs(html, "lxml")

tables=soup.find_all("table", class_="wikitable")

dfs=[pd.read_html(str(table))[0] for table in tables]
tablas_unidas=pd.concat(dfs,ignore_index=True)
tablas_unidas.to_excel("paises_ley_benford.xlsx",index=False)

print("Archivo paises ley benford generado correctamente ")


#limpia de datos numericos
columna_poblacion = tablas_unidas.columns[1]

numeros = (
    tablas_unidas[columna_poblacion]
    .astype(str)
    .str.replace(",", "", regex=False)
    .astype(int)
)


primeros_digitos=[str(n)[0] for n in numeros if n>0]


conteo=Counter(primeros_digitos)
total=sum(conteo.values())


datos_benford=[]

for  d in range(1,10):
    cantidad=conteo.get(str(d),0)
    
    freq_real=cantidad/total
    freq_teorica=math.log10(1+1/d)
    
    datos_benford.append(
        {
            "Dígito":d,
            "Cantidad":cantidad,
            "Frecuencia Real":freq_real,
            "Frecuencia Teórica":freq_teorica
            }
    )
    
    
# Fila total
datos_benford.append({
    "Dígito":"Total",
    "Cantidad": total
    
})    
    
    
df_benford=pd.DataFrame(datos_benford)
df_benford.to_excel("resultados_benford.xlsx", index=False)


