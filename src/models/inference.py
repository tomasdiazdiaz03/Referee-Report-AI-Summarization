from transformers import GPT2Tokenizer, GPT2LMHeadModel, BartTokenizer, BartForConditionalGeneration
import json

# Cargar modelos
gpt_model = GPT2LMHeadModel.from_pretrained("../../models/gpt2_model")
gpt_tokenizer = GPT2Tokenizer.from_pretrained("../../models/gpt2_model")
bart_model = BartForConditionalGeneration.from_pretrained("../../models/bart_model")
bart_tokenizer = BartTokenizer.from_pretrained("../../models/bart_model")

# Función para generar informe
def generar_informe(partido):
    input_text = ""
    
    # Si hay pdf_sections, lo agregamos
    if partido.get("pdf_sections"):
        input_text += "Condición física: " + partido["pdf_sections"].get("condicion_fisica", "") + " "
        input_text += "Actuación técnica: " + partido["pdf_sections"].get("actuacion_tecnica", "") + " "
        input_text += "Actuación disciplinaria: " + partido["pdf_sections"].get("actuacion_disciplinaria", "") + " "
        input_text += "Manejo del partido: " + partido["pdf_sections"].get("manejo_partido", "") + " "
        input_text += "Personalidad y trabajo en equipo: " + partido["pdf_sections"].get("personalidad_trabajo_equipo", "") + " "
    
    # Si hay txt_events, lo agregamos
    if partido.get("txt_events"):
        for event in partido["txt_events"]:
            input_text += f"Minuto {event['minute']}: {event['description']} "
    
    # Paso 1: Generación estructurada con GPT
    input_ids = gpt_tokenizer.encode(input_text, return_tensors="pt")
    gpt_output = gpt_model.generate(input_ids, max_length=200)
    generated_text = gpt_tokenizer.decode(gpt_output[0], skip_special_tokens=True)

    # Paso 2: Mejora del texto con BART
    input_ids = bart_tokenizer.encode(generated_text, return_tensors="pt")
    bart_output = bart_model.generate(input_ids, max_length=250)
    final_text = bart_tokenizer.decode(bart_output[0], skip_special_tokens=True)

    return final_text

# Prueba con un partido
with open("../../data/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(generar_informe(dataset["0"]))