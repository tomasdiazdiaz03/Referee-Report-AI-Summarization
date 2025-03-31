from transformers import pipeline
from rule_phrase_system import generar_resumen
import torch

# Ruta del modelo local descargado
local_model_path = "./models/EleutherAI/gpt-neo-1.3B"

# Crear un pipeline usando el modelo local
resumen_model = pipeline(
    "text-generation", 
    model=local_model_path,
    tokenizer=local_model_path,
    device=0 if torch.cuda.is_available() else -1  # Utiliza GPU si está disponible
)

# Generar los resúmenes estructurados
resumenes_estructurados = generar_resumen()

# Lista para almacenar los resúmenes generados
respuestas = []

# Parametrización personalizable para la generación de texto
parametros_generacion = {
    "max_new_tokens": 200,
    "num_return_sequences": 1,
    "temperature": 0.7,      # Controlar aleatoriedad: menor = más determinista
    "top_k": 50,             # Considerar solo los 50 tokens con mayor puntuación
    "top_p": 0.9,            # Nucleus sampling: elegir tokens acumulando 90% de probabilidad
    "do_sample": True        # Habilitar sampling aleatorio
}

# Procesar los resúmenes estructurados
for id, resumen_base in resumenes_estructurados.items():
    prompt = f"""
    Reescribe el siguiente informe arbitral de manera profesional, respetando los apartados y mejorando el estilo:

    {resumen_base}
    """
    
    # Usar el pipeline con los parámetros configurados
    salida = resumen_model(prompt, **parametros_generacion)[0]['generated_text']
    
    # Almacenar el resumen generado
    respuestas.append(salida)
    break  # Procesa solo uno por ahora (quitar el break si quieres más resúmenes)

# Imprimir el primer resumen generado
if respuestas:
    print("Resumen generado:")
    print(respuestas[0])