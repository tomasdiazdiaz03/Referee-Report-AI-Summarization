import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
import json

# Cargar datos
with open("../../data/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Procesar datos: concatenamos los campos importantes como entrada de entrenamiento
train_texts = []
for partido in dataset:
    input_text = f"Árbitro: {partido['pdf_data']['arbitro']['actuacion_tecnica']} "
    input_text += f"Asistente 1: {partido['pdf_data']['asistente_1']['comentarios']} "
    input_text += f"Asistente 2: {partido['pdf_data']['asistente_2']['comentarios']} "
    output_text = partido['pdf_data']['resumen_final']  # Resumen de referencia
    train_texts.append(f"{input_text} => {output_text}")

# Tokenización
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
inputs = tokenizer(train_texts, padding=True, truncation=True, return_tensors="pt")

# Modelo
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Configurar entrenamiento
training_args = TrainingArguments(
    output_dir="../../models/gpt2_model",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_steps=1000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=inputs,
)

# Entrenar
trainer.train()

# Guardar modelo entrenado
model.save_pretrained("../../models/gpt2_model")
tokenizer.save_pretrained("../../models/gpt2_model")