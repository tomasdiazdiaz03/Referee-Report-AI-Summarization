from transformers import Trainer, TrainingArguments, AutoModelForSeq2SeqLM, AutoTokenizer
import os
import torch
from datasets import load_dataset

# Hardcodeamos rutas y parámetros
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "train.json")

BART_MODEL_NAME = "mrm8488/t5-small-spanish"
BART_SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", BART_MODEL_NAME)
BART_TRAIN_ARGS = {
    "output_dir": BART_SAVE_DIR,
    "num_train_epochs": 3,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "logging_dir": "./logs",
    "logging_steps": 10,
    "save_total_limit": 2
}

GPT_MODEL_NAME = "mrm8488/t5-small-spanish"
GPT_SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", GPT_MODEL_NAME)
GPT_TRAIN_ARGS = {
    "output_dir": GPT_SAVE_DIR,
    "num_train_epochs": 3,
    "per_device_train_batch_size": 8,
    "per_device_eval_batch_size": 8,
    "warmup_steps": 500,
    "weight_decay": 0.01,
    "logging_dir": "./logs",
    "logging_steps": 10,
    "save_total_limit": 2
}

def train_bart():
    """Entrena el modelo BART con los datos en 'data/train.json'."""
    os.makedirs(BART_SAVE_DIR, exist_ok=True)

    print("Cargando modelo y tokenizer...")
    model = AutoModelForSeq2SeqLM.from_pretrained(BART_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(BART_MODEL_NAME)

    print("Cargando dataset...")
    dataset = load_dataset("json", data_files={"train": DATASET_PATH})["train"]

    print("Tokenizando datos...")
    def preprocess_function(examples):
        inputs = [ex["input_text"] for ex in examples["data"]]
        targets = [ex["output_text"] for ex in examples["data"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        labels = tokenizer(targets, max_length=512, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_dataset = dataset.map(preprocess_function, batched=True)

    print("Configurando entrenamiento...")
    training_args = TrainingArguments(**BART_TRAIN_ARGS)
    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_dataset)

    print("Comenzando entrenamiento...")
    trainer.train()

    print(f"Guardando modelo en {BART_SAVE_DIR}...")
    model.save_pretrained(BART_SAVE_DIR)
    tokenizer.save_pretrained(BART_SAVE_DIR)


def train_gpt():
    """Entrena el modelo GPT con los datos en 'data/train.json'."""
    os.makedirs(GPT_SAVE_DIR, exist_ok=True)

    print("Cargando modelo y tokenizer...")
    model = AutoModelForSeq2SeqLM.from_pretrained(GPT_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(GPT_MODEL_NAME)

    print("Cargando dataset...")
    dataset = load_dataset("json", data_files={"train": DATASET_PATH})["train"]

    print("Tokenizando datos...")
    def preprocess_function(examples):
        inputs = [ex["input_text"] for ex in examples["data"]]
        targets = [ex["output_text"] for ex in examples["data"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        labels = tokenizer(targets, max_length=512, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_dataset = dataset.map(preprocess_function, batched=True)

    print("Configurando entrenamiento...")
    training_args = TrainingArguments(**GPT_TRAIN_ARGS)
    trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_dataset)

    print("Comenzando entrenamiento...")
    trainer.train()

    print(f"Guardando modelo en {GPT_SAVE_DIR}...")
    model.save_pretrained(GPT_SAVE_DIR)
    tokenizer.save_pretrained(GPT_SAVE_DIR)

if __name__ == "__main__":
    train_bart()
    train_gpt()
