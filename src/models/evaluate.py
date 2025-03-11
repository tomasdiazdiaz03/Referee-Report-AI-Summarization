from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import os
import json
import evaluate

# Hardcodeamos rutas
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "test.json")

# Configuración de modelos
BART_MODEL_NAME = "mrm8488/t5-small-spanish"
BART_SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", BART_MODEL_NAME)

GPT_MODEL_NAME = "mrm8488/t5-small-spanish"
GPT_SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", GPT_MODEL_NAME)

# Cargar métricas
bleu = evaluate.load("bleu")
rouge = evaluate.load("rouge")

def evaluate_model(model_name, model_path):
    """Evalúa un modelo generando texto y comparándolo con los valores de referencia."""
    print(f"\nEvaluando modelo {model_name}...")

    print("Cargando modelo y tokenizer...")
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    print("Cargando dataset de prueba...")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    references, predictions = [], []
    for example in test_data["data"]:
        input_text = example["input_text"]
        reference_text = example["output_text"]

        inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(**inputs)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        references.append(reference_text)
        predictions.append(generated_text)

    print("Calculando métricas...")
    bleu_score = bleu.compute(predictions=predictions, references=[[r] for r in references])
    rouge_score = rouge.compute(predictions=predictions, references=references)

    print(f"Resultados de evaluación para {model_name}:")
    print(f"  - BLEU Score: {bleu_score['bleu']:.4f}")
    print(f"  - ROUGE Score: {rouge_score}")

if __name__ == "__main__":
    evaluate_model("BART", BART_SAVE_DIR)
    evaluate_model("GPT", GPT_SAVE_DIR)
