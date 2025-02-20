from rouge_score import rouge_scorer
from models.inference import generar_informe
import json

# Cargar datos
with open("../../data/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

def evaluar_modelo():
    scores = []
    for partido in dataset:
        generated_summary = generar_informe(partido)
        reference_summary = partido["pdf_data"]["resumen_final"]

        score = scorer.score(reference_summary, generated_summary)
        scores.append(score)

    avg_rouge1 = sum(s['rouge1'].fmeasure for s in scores) / len(scores)
    avg_rouge2 = sum(s['rouge2'].fmeasure for s in scores) / len(scores)
    avg_rougeL = sum(s['rougeL'].fmeasure for s in scores) / len(scores)

    print(f"ROUGE-1: {avg_rouge1:.4f}")
    print(f"ROUGE-2: {avg_rouge2:.4f}")
    print(f"ROUGE-L: {avg_rougeL:.4f}")

# Ejecutar evaluación
evaluar_modelo()
