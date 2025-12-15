# =========================
# 1. SCRAPEAR PÁGINA DE WIKIPEDIA
# =========================

# Librería para hacer peticiones HTTP (descargar páginas web)
import requests

# Librería para manipular datos en forma de tablas (DataFrames)
import pandas as pd

# BeautifulSoup sirve para analizar y extraer información del HTML
from bs4 import BeautifulSoup as bs

# spaCy: librería de NLP (Procesamiento de Lenguaje Natural) para inglés
import spacy

# Stanza: librería de NLP (Procesamiento de Lenguaje Natural) para latín
import stanza

# Counter permite contar la frecuencia de elementos en una lista
from collections import Counter

# Librería para traducir texto usando Google Translate
from deep_translator import GoogleTranslator


# URL de la página de Wikipedia que contiene las frases en latín
url = "https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)"

# Encabezados HTTP para simular que la petición viene de un navegador real
# Esto evita que Wikipedia bloquee la solicitud
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Se realiza la petición GET a la página web
response = requests.get(url, headers=headers)

# Se obtiene el contenido HTML de la página como texto
html = response.text

# Se crea el objeto BeautifulSoup para analizar el HTML
# "lxml" es el parser (más rápido y robusto)
soup = bs(html, "lxml")

# Se buscan todas las tablas HTML con la clase "wikitable"
tables = soup.find_all("table", class_="wikitable")

# Se imprime cuántas tablas se encontraron
print(f"Número de tablas encontradas: {len(tables)}")


# Lista vacía para guardar los DataFrames de cada tabla
dfs = []

# Se recorre cada tabla encontrada en el HTML
for table in tables:
    # pd.read_html convierte una tabla HTML en un DataFrame
    # [0] porque devuelve una lista y solo queremos la primera tabla
    df = pd.read_html(str(table))[0]
    
    # Se agrega el DataFrame a la lista
    dfs.append(df)
    
    
# Se unen todos los DataFrames en uno solo
# ignore_index=True reinicia el índice
tabla_unificada = pd.concat(dfs, ignore_index=True)

# Muestra las primeras filas del DataFrame
tabla_unificada.head()


# =========================
# 2. GUARDAR EN UN ARCHIVO XLSX
# =========================

# Nombre del archivo de salida
archivo_salida = "latin_phrases_wikipedia.xlsx"

# Se guarda el DataFrame en un archivo Excel
# index=False evita que se guarde la columna del índice
tabla_unificada.to_excel(archivo_salida, index=False)

# Muestra el nombre del archivo generado
archivo_salida


# =========================
# 3. PALABRAS Y VERBOS MÁS FRECUENTES (LATÍN E INGLÉS)
# =========================

# Se carga el modelo de NLP de spaCy para inglés
nlp_en = spacy.load("en_core_web_sm")


# Se descarga el modelo de Stanza para latín (solo la primera vez)
stanza.download("la")

# Se inicializa el pipeline de procesamiento para latín
nlp_lat = stanza.Pipeline("la")

# Muestra los nombres de las columnas del DataFrame
tabla_unificada.columns


# Se unen todas las frases en latín en un solo texto
# dropna(): elimina valores nulos
# astype(str): asegura que todo sea texto
texto_latin = " ".join(tabla_unificada["Latin"].dropna().astype(str))

# Se unen todas las traducciones al inglés en un solo texto
texto_english = " ".join(tabla_unificada["Translation"].dropna().astype(str))


# Se procesa el texto en latín con Stanza
doc_latin = nlp_lat(texto_latin)

# Se procesa el texto en inglés con spaCy
doc_english = nlp_en(texto_english)


# =========================
# PALABRAS (SUSTANTIVOS Y ADJETIVOS) EN LATÍN
# =========================

palabras_latin = [
    word.text.lower()           # Se pasa la palabra a minúsculas
    for sent in doc_latin.sentences   # Se recorren las oraciones
    for word in sent.words            # Se recorren las palabras
    if word.text.isalpha()            # Solo palabras (sin números ni símbolos)
    and word.upos in {"NOUN", "ADJ"}  # Solo sustantivos y adjetivos
]

# Se cuentan las frecuencias de las palabras en latín
frecuencia_palabras_latin = Counter(palabras_latin)

# Se muestran las 10 palabras más comunes
frecuencia_palabras_latin.most_common(10)


# =========================
# VERBOS EN LATÍN
# =========================

verbos_latin = [
    word.lemma.lower()      # Se usa el lema (forma base del verbo)
    for sent in doc_latin.sentences
    for word in sent.words
    if word.upos == "VERB"  # Solo verbos
]

# Se cuentan las frecuencias de los verbos
frecuencia_verbos_latin = Counter(verbos_latin)

# Se muestran los 10 verbos más comunes
frecuencia_verbos_latin.most_common(10)


# =========================
# PALABRAS EN INGLÉS
# =========================

palabras_english = [
    token.text.lower()      # Palabra en minúsculas
    for token in doc_english
    if token.is_alpha       # Solo palabras (sin símbolos)
    and not token.is_stop   # Se eliminan stopwords (the, and, of, etc.)
]

# Se cuentan las palabras en inglés
frecuencia_palabras_english = Counter(palabras_english)

# Top 10 palabras en inglés
frecuencia_palabras_english.most_common(10)


# =========================
# VERBOS EN INGLÉS
# =========================

verbos_english = [
    token.lemma_.lower()    # Lema del verbo
    for token in doc_english
    if token.pos_ == "VERB" # Solo verbos
]

# Se cuentan los verbos en inglés
frecuencia_verbos_english = Counter(verbos_english)

# Top 10 verbos en inglés
frecuencia_verbos_english.most_common(10)


# =========================
# 4. GENERAR FRASES EN ESPAÑOL A PARTIR DE LAS PALABRAS MÁS USADAS
# =========================

# Se obtienen las 5 palabras más frecuentes en latín
top_palabras_latin = [palabra for palabra, _ in frecuencia_palabras_latin.most_common(5)]

# Se obtienen las 5 palabras más frecuentes en inglés
top_palabras_english = [palabra for palabra, _ in frecuencia_palabras_english.most_common(5)]


# Traducción de palabras latinas al español
print("LATÍN:\n")
for palabra in top_palabras_latin:
    traduccion = GoogleTranslator(source='latin', target='es').translate(palabra)
    print(f"La palabra '{palabra}' significa '{traduccion}' en español.")

# Traducción de palabras inglesas al español
print("\nINGLÉS:\n")
for palabra in top_palabras_english:
    traduccion = GoogleTranslator(source='en', target='es').translate(palabra)
    print(f"La palabra '{palabra}' significa '{traduccion}' en español.")
