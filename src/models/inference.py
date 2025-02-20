from transformers import GPT2Tokenizer, GPT2LMHeadModel, BartTokenizer, BartForConditionalGeneration
import json

# Cargar modelos
gpt_model = GPT2LMHeadModel.from_pretrained("../../models/gpt2_model")
gpt_tokenizer = GPT2Tokenizer.from_pretrained("../../models/gpt2_model")
bart_model = BartForConditionalGeneration.from_pretrained("../../models/bart_model")
bart_tokenizer = BartTokenizer.from_pretrained("../../models/bart_model")

# Función para generar informe
def generar_informe(partido):
    # Paso 1: Generación estructurada con GPT
    input_text = f"Árbitro: {partido['pdf_data']['arbitro']['actuacion_tecnica']}..."
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

print(generar_informe(dataset[0]))
