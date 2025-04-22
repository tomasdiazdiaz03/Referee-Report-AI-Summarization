import os
import json
from datasets import load_metric
from transformers import pipeline
from bert_score import score as bertscore
import evaluate

# Rutas base
BASE_DIR = os.path.dirname(__file__)
PDF_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "pdf_resumenes.json")  # Ruta del JSON con los resúmenes reales
GENERATED_OUTPUTS_PATH = os.path.join(BASE_DIR, "..", "outputs", "generated_resumenes.json")  # Ruta con resúmenes generados por el modelo

# Cargar datos
def cargar_datos():
    with open(PDF_DATA_PATH, "r", encoding="utf-8") as f1, open(GENERATED_OUTPUTS_PATH, "r", encoding="utf-8") as f2:
        refs = json.load(f1)
        hyps = json.load(f2)
    return refs, hyps

# Evaluación con ROUGE
def evaluar_rouge(referencias, predicciones):
    rouge = evaluate.load("rouge")
    resultados = rouge.compute(predictions=predicciones, references=referencias)
    return resultados

# Evaluación con BERTScore
def evaluar_bertscore(referencias, predicciones):
    P, R, F1 = bertscore(predicciones, referencias, lang="es")
    return {
        "bert_precision": P.mean().item(),
        "bert_recall": R.mean().item(),
        "bert_f1": F1.mean().item()
    }

# Función principal
def main():
    refs, hyps = cargar_datos()

    ids_comunes = set(refs.keys()) & set(hyps.keys())
    refs_filtradas = [refs[i] for i in ids_comunes]
    hyps_filtradas = [hyps[i] for i in ids_comunes]

    print("📝 Evaluando con ROUGE...")
    rouge_scores = evaluar_rouge(refs_filtradas, hyps_filtradas)
    print("🔢 Resultados ROUGE:", rouge_scores)

    print("\\n🧠 Evaluando con BERTScore...")
    bert_scores = evaluar_bertscore(refs_filtradas, hyps_filtradas)
    print("🔢 Resultados BERTScore:", bert_scores)

if __name__ == "__main__":
    main()