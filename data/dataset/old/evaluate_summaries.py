import os
import json
from bert_score import score as bertscore
import evaluate

# Rutas base
DATASET_PATH = os.path.join("./data/dataset/dataset_updated.json")  # Resumen real de referencia
GENERATED_OUTPUTS_PATH = os.path.join("./data/output/resumenes_generados.json")  # Resumen generado por el modelo

def cargar_datos():
    with open(DATASET_PATH, "r", encoding="utf-8") as f1, open(GENERATED_OUTPUTS_PATH, "r", encoding="utf-8") as f2:
        dataset = json.load(f1)
        generados = json.load(f2)

    referencias = {}
    predicciones = {}

    for item in generados:
        if item.get("tipo") != "PDF":
            continue

        id_str = str(item.get("id"))
        if id_str not in dataset:
            continue

        resumen_ref_raw = dataset[id_str]['pdf_sections'].get("resumen_final")
        resumen_ref = str(resumen_ref_raw).strip() if resumen_ref_raw else ""

        resumen_arbitro = item.get("output_arbitro", "").strip()
        resumen_asistente_1 = item.get("output_asistente_1", "").strip()
        resumen_asistente_2 = item.get("output_asistente_2", "").strip()
        resumen_cuarto = item.get("output_cuarto_arbitro", "").strip()

        if not resumen_ref or not resumen_arbitro:
            continue  # ignorar si falta algo importante

        resumen_completo = (
            f"**Resumen Árbitro:** {resumen_arbitro}\n\n"
            f"**Resumen Asistente 1:** {resumen_asistente_1}\n\n"
            f"**Resumen Asistente 2:** {resumen_asistente_2}\n\n"
            f"**Resumen Cuarto Árbitro:** {resumen_cuarto}"
        )

        referencias[id_str] = resumen_ref
        predicciones[id_str] = resumen_completo

    return referencias, predicciones

def evaluar_rouge(referencias, predicciones):
    rouge = evaluate.load("rouge")
    resultados = rouge.compute(predictions=list(predicciones.values()), references=list(referencias.values()))
    return resultados

def evaluar_bertscore(referencias, predicciones):
    P, R, F1 = bertscore(list(predicciones.values()), list(referencias.values()), lang="es")
    return {
        "bert_precision": P.mean().item(),
        "bert_recall": R.mean().item(),
        "bert_f1": F1.mean().item()
    }

def main():
    referencias, predicciones = cargar_datos()

    if not referencias or not predicciones:
        print("❌ No se encontraron pares válidos de referencia/hipótesis.")
        return

    print("Evaluando con ROUGE...")
    rouge_scores = evaluar_rouge(referencias, predicciones)
    print("Resultados ROUGE:", rouge_scores)

    print("\nEvaluando con BERTScore...")
    bert_scores = evaluar_bertscore(referencias, predicciones)
    print("Resultados BERTScore:", bert_scores)

if __name__ == "__main__":
    main()
