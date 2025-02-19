import pandas as pd
import json

# Ruta al archivo XLSX
file_path = "data\TOPICS.xlsx"

# Leer el archivo XLSX
df = pd.read_excel(file_path)

# Eliminar filas con valores NaN en ambas columnas
df = df.dropna(subset=['Unnamed: 1', 'Unnamed: 2'])

# Crear una lista de tuplas con los valores correspondientes de 'Unnamed: 1' y 'Unnamed: 2'
topics = list(zip(df['Unnamed: 1'], df['Unnamed: 2']))

# Convertir la lista de tuplas en una lista de diccionarios
topics_dict = [{'Topic': topic, 'Code': code} for topic, code in topics]

# Guardar la lista de diccionarios en un archivo JSON
with open('data/topics.json', 'w', encoding='utf-8') as f:
    json.dump(topics_dict, f, ensure_ascii=False, indent=4)

print("Datos guardados en data/topics.json")