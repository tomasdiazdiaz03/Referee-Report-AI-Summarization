import re
import json
import unicodedata

dataset_path = "./data/dataset/full_dataset.json"

##############################
### SECCIÓN PARA DATOS TXT ###
##############################

def extract_additional_codes_from_description(event):
    """
    Extrae códigos adicionales de la descripción del evento y los mueve a un nuevo campo.
    
    - Los códigos están separados por espacios y contienen símbolos como '-', '+', o son abreviaciones en mayúsculas.
    - Una vez extraídos los códigos, se eliminan de la descripción.
    """
    description = event.get("description", "").strip()

    # Expresión regular para encontrar códigos con el formato esperado
    pattern = r"^([-+]?[A-ZÁÉÍÓÚÑÇ0-9]+(?:-[A-ZÁÉÍÓÚÑÇ0-9]+)*)\s*"

    additional_codes = []
    while True:
        match = re.match(pattern, description)
        if not match:
            break  # Salimos cuando ya no encontramos más códigos

        code = match.group(1)
        additional_codes.append(code)
        description = description[len(code):].strip()  # Eliminamos el código extraído de la descripción

    # Tokenizamos la descripción en palabras
    tokens = description.split()

    # Filtramos para eliminar los tokens que sean exactamente "+" o "-" (los guiones de jugadores como 10-CEL forman parte de un token con más palabras)
    filtered_tokens = [token for token in tokens if token not in {"+", "-"}]

    # Reconstruimos la descripción sin los separadores no deseados
    description_cleaned = " ".join(filtered_tokens)
    description_processed = normalize_text(description_cleaned)

    print(description)
    print(description_processed)
    print(additional_codes)
    print("-------------------")

    # Actualizar el evento con los códigos extraídos
    event["additional_codes"] = additional_codes
    event["description"] = description_processed  # Guardamos la descripción limpia

    return event


def parse_assistant_events(event_string):
    """
    Convierte una cadena de eventos concatenados en una lista estructurada de eventos.
    
    Parámetro:
    - event_string (str): cadena con los eventos en formato "minuto-código (descripción opcional)" sin separación clara.

    Retorna:
    - list[dict]: Lista con subdiccionarios que contienen "minute", "code" y "description".
    """
    # Expresión regular para detectar cada evento (minuto-código) seguido opcionalmente de una descripción
    pattern = r"(\d{2}:\d{2})-([A-Z]+)(?:\s*([^\d{2}:\d{2}-]*))?"
    
    matches = re.findall(pattern, event_string)

    events = []
    for match in matches:
        minute, code, description = match
        description = description.strip() if description else ""  # Limpiar descripción si existe
        events.append({"minute": minute, "code": code, "description": description})

    return events


###########################################
### SECCIÓN COMÚN DE DATOS DE PDF Y TXT ###
###########################################

def normalize_text(text):
    """Normaliza el texto eliminando espacios innecesarios y caracteres extraños."""
    text = text.strip()  # Elimina espacios al inicio y final
    text = re.sub(r"\s+", " ", text)  # Reemplaza múltiples espacios con uno solo
    text = unicodedata.normalize("NFKC", text)  # Normaliza caracteres unicode (como comillas raras)
    return text


def preprocess_match_data(match):
    """Aplica limpieza a todos los textos de un partido."""
    if match["pdf_sections"] is not None:
        for section in match["pdf_sections"]:
            if isinstance(match["pdf_sections"][section], dict):  
                for key in match["pdf_sections"][section]:  
                    match["pdf_sections"][section][key] = normalize_text(match["pdf_sections"][section][key])
            else:
                match["pdf_sections"][section] = normalize_text(match["pdf_sections"][section])
    
    if match["txt_events"] is not None:
        for section in match["txt_events"]:
            if isinstance(match["txt_events"][section], list):
                new_events = [extract_additional_codes_from_description(event) for event in match["txt_events"][section]]
                match["txt_events"][section] = new_events
            elif isinstance(match["txt_events"][section], dict):
                new_assistant = {}
                for key, event_string in match["txt_events"][section].items():
                    new_assistant[key] = parse_assistant_events(event_string)
                match["txt_events"][section] = new_assistant
    return match

if __name__ == "__main__":
    # Cargar dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # # Preprocesar cada partido
    # processed_dataset = [preprocess_match_data(match) for match in dataset]

    # # Guardar dataset preprocesado
    # with open("../../data/dataset_clean.json", "w", encoding="utf-8") as f:
    #     json.dump(processed_dataset, f, ensure_ascii=False, indent=4)

    # print("Preprocesamiento completado. Datos guardados en dataset_clean.json")
    for _, match in dataset.items():
        preprocess_match_data(match)
        break