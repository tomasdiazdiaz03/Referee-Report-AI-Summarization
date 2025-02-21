from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
import json

# Cargar datos
with open("../../data/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Procesar datos: combinamos pdf_sections y txt_events
train_texts = []
for partido in dataset.values():
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
    
    # Si hay resumen final, lo usamos como salida
    if partido.get("pdf_sections") and partido["pdf_sections"].get("resumen_final"):
        output_text = partido["pdf_sections"]["resumen_final"]
    else:
        output_text = "Resumen no disponible"
    
    train_texts.append((input_text, output_text))

# Tokenización
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")
inputs = tokenizer([x[0] for x in train_texts], padding=True, truncation=True, return_tensors="pt")
outputs = tokenizer([x[1] for x in train_texts], padding=True, truncation=True, return_tensors="pt")

# Modelo
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large")

# Configurar entrenamiento
training_args = TrainingArguments(
    output_dir="../../models/bart_model",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_steps=1000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=inputs,
    eval_dataset=outputs,
)

# Entrenar
trainer.train()

# Guardar modelo
model.save_pretrained("../../models/bart_model")
tokenizer.save_pretrained("../../models/bart_model")