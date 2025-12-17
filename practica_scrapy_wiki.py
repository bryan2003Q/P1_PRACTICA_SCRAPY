# =========================
# 1. SCRAPEAR PÁGINA DE WIKIPEDIA
# =========================

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import spacy
import stanza
from io import StringIO
from collections import Counter
import logging
from deep_translator import GoogleTranslator

#logging.getLogger("stanza").setLevel(logging.ERROR)
# URL de la página de Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)"

# Encabezados HTTP para simular navegador
headers = {"User-Agent": "Mozilla/5.0"}

# Petición GET a la página web
response = requests.get(url, headers=headers)
html = response.text

# Analizar el HTML con BeautifulSoup
soup = bs(html, "lxml")

# Buscar todas las tablas HTML con la clase "wikitable"
tables = soup.find_all("table", class_="wikitable")
print(f"Número de tablas encontradas: {len(tables)}")

# Guardar los DataFrames de cada tabla
dfs = [pd.read_html(StringIO(str(table)))[0] for table in tables]

# Unir todos los DataFrames en uno solo
tabla_unificada = pd.concat(dfs, ignore_index=True)
tabla_unificada.head()

# =========================
# 2. GUARDAR EN UN ARCHIVO XLSX
# =========================


archivo_salida = "latin_phrases_wikipedia.xlsx"
tabla_unificada.to_excel(archivo_salida, index=False)
archivo_salida

# =========================
# 3. PALABRAS Y VERBOS MÁS FRECUENTES (LATÍN E INGLÉS)
# =========================

# NLP inglés y latín
nlp_en = spacy.load("en_core_web_sm")
stanza.download("la")  # Solo la primera vez
nlp_lat = stanza.Pipeline("la",verbose=False)

# Preparar textos
texto_latin = " ".join(tabla_unificada["Latin"].dropna().astype(str))
texto_english = " ".join(tabla_unificada["Translation"].dropna().astype(str))

doc_latin = nlp_lat(texto_latin)
doc_english = nlp_en(texto_english)

# =========================
# PALABRAS Y VERBOS EN LATÍN
# =========================

palabras_latin = [
    word.text.lower()
    for sent in doc_latin.sentences
    for word in sent.words
    if word.text.isalpha() and word.upos in {"NOUN", "ADJ"}
]
frecuencia_palabras_latin = Counter(palabras_latin)
frecuencia_palabras_latin.most_common(10)


print("\n palabras mas frecuentes en Latin")
for palabra, freq in frecuencia_palabras_latin.most_common(10):
    print(f"{palabra}: {freq} veces ")


verbos_latin = [
    word.lemma.lower()
    for sent in doc_latin.sentences
    for word in sent.words
    if word.upos == "VERB"
]
frecuencia_verbos_latin = Counter(verbos_latin)
frecuencia_verbos_latin.most_common(10)


print("\n verbos mas frecuentes en Latin")
for verbo, freq in frecuencia_verbos_latin.most_common(10):
    print(f"{verbo}: {freq} veces ")


# =========================
# PALABRAS Y VERBOS EN INGLÉS
# =========================

palabras_english = [
    token.text.lower() 
    for token in doc_english 
    if token.is_alpha and not token.is_stop
]
frecuencia_palabras_english = Counter(palabras_english)
frecuencia_palabras_english.most_common(10)


print("\n palabras mas frecuentes en ingles")
for palabra, freq in frecuencia_palabras_english.most_common(10):
    print(f"{palabra}: {freq} veces ")


verbos_english = [
    token.lemma_.lower() 
    for token in doc_english 
    if token.pos_ == "VERB"
    ]
frecuencia_verbos_english = Counter(verbos_english)
frecuencia_verbos_english.most_common(10)


print("\n verbos mas frecuentes en ingles")
for verbo, freq in frecuencia_verbos_english.most_common(10):
    print(f"{verbo}: {freq} veces ")

# =========================
# 4. GENERAR FRASES EN ESPAÑOL
# =========================

top_palabras_latin = [
    palabra for palabra, _ in frecuencia_palabras_latin.most_common(5)
]
top_palabras_english = [
    palabra for palabra, _ in frecuencia_palabras_english.most_common(5)
]

# Traducción de palabras
print("LATÍN:\n")
for palabra in top_palabras_latin:
    traduccion = GoogleTranslator(source="latin", target="es").translate(palabra)
    print(f"La palabra '{palabra}' significa '{traduccion}' en español.")

print("\nINGLÉS:\n")
for palabra in top_palabras_english:
    traduccion = GoogleTranslator(source="en", target="es").translate(palabra)
    print(f"La palabra '{palabra}' significa '{traduccion}' en español.")
