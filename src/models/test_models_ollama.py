import ollama
import random
from tqdm import tqdm
from rule_phrase_system import generar_resumen_pdf

# Lista de modelos a probar en Ollama
# MODELOS = ["mistral", "gemma3:4b", "llama3.1:8b", "deepseek-r1:7b"] # Primera prueba
# MODELOS = ["mistral", "gemma3:4b", "gemma3:12b"] # Segunda prueba
MODELOS = ["gemma3:4b", "gemma3:12b"] # Prueba solo con Gemma


# Diccionario para almacenar los resultados
resultados = {}

# Función para obtener los 15 primeros partidos (simulado)
def cargar_partidos():
    datos_partidos = generar_resumen_pdf()
    ids = list(datos_partidos.keys())
    resumenes = list(datos_partidos.values())
    return [f"Partido {i+1} con id {ids[i]}: {resumenes[i]}" for i in range(5)]

# Función para generar resumen con un modelo
def generar_outputs(modelo, contenido):
    prompt = f"""
    Eres un experto en arbitraje de fútbol. Dado el siguiente partido, genera un resumen profesional y conciso utilizando lenguaje natural y mencionando todos los apartados en un párrafo más o menos extenso. Quiero que, en caso de no haber información sobre un apartado, lo ignores:

    {contenido}
    """
    respuesta = ollama.chat(model=modelo, messages=[
        {'role': 'system', 'content': 'Eres un experto en arbitraje y redacción deportiva.'},
        {'role': 'user', 'content': prompt}
    ])
    return respuesta['message']['content']

# Obtener los primeros 15 partidos
# print(len(cargar_partidos()))
partidos = cargar_partidos()

# Iterar sobre cada partido
for i, partido in enumerate(partidos, start=1):
    print(f"\n**Partido {i}**")

    # Generar resúmenes con cada modelo con barra de progreso
    respuestas = {}
    for modelo in tqdm(MODELOS, desc="Generando respuestas", unit="modelo"):
        respuestas[modelo] = generar_outputs(modelo, partido)

    # Mezclar aleatoriamente las respuestas sin mostrar el modelo
    opciones = list(respuestas.values())
    random.shuffle(opciones)

    # Mostrar respuestas numeradas
    for idx, opcion in enumerate(opciones, start=1):
        print(f"\n- Opción {idx}:")
        print(opcion)

    # Pedir al usuario que seleccione la mejor opción
    eleccion = int(input("\nElige la mejor respuesta (1 o 2): ")) - 1

    # Guardar la respuesta elegida y el modelo correspondiente
    modelo_elegido = [m for m, r in respuestas.items() if r == opciones[eleccion]][0]
    resultados[partido] = (opciones[eleccion], modelo_elegido)

# Mostrar resultados finales
print("\n**Resultados Finales**")
for partido, (respuesta, modelo) in resultados.items():
    print(f"\n{partido}")
    print(f"Respuesta elegida: {respuesta[:100]}...")  # Solo los primeros 100 caracteres
    print(f"Generada por: {modelo}")