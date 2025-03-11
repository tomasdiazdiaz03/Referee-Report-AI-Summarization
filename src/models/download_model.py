from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os

GENERATIVE_MODEL_NAME = "mrm8488/t5-small-spanish"  # Cambia si usas otro modelo
# GENERAL_MODEL_NAME = "mrm8488/t5-small-spanish"  # Cambia si usas otro modelo
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")  # Ruta relativa a models/


def download_model(model_name):
    """Descarga y guarda el modelo y tokenizer"""
    os.makedirs(SAVE_DIR, exist_ok=True)
    model_path = os.path.join(SAVE_DIR, model_name)

    print(f"Descargando modelo {model_name} en {model_path}...")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)

    print(f"Modelo guardado en '{model_path}'.")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    download_model(GENERATIVE_MODEL_NAME)
    # download_model(GENERAL_MODEL_NAME)

