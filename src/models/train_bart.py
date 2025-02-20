from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
import json

# Cargar datos
with open("../../data/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Procesar datos: tomamos el output del primer modelo como entrada
train_texts = []
for partido in dataset:
    input_text = f"{partido['pdf_data']['resumen_final']}"
    output_text = f"{partido['pdf_data']['resumen_final']} (Mejorado)"
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
