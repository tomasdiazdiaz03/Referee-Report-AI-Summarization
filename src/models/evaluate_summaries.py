import os
import json
from bert_score import score as bertscore
import evaluate

# Rutas base
DATASET_PATH = os.path.join("./data/dataset/dataset_updated.json")  # Ruta del JSON con los resúmenes reales
GENERATED_OUTPUTS_PATH = os.path.join("./data/output/resumenes_generados.json")  # Ruta con resúmenes generados por el modelo

# Cargar datos de referencia y generados
def cargar_datos():
    with open(DATASET_PATH, "r", encoding="utf-8") as f1, open(GENERATED_OUTPUTS_PATH, "r", encoding="utf-8") as f2:
        dataset = json.load(f1)
        generados = json.load(f2)

    referencias = {}
    predicciones = {}

    for item in generados:
        if str(item.get("tipo")) == "PDF":
            # Solo procesar resúmenes PDF
            id_str = str(item.get("id"))
            output = item.get("output", "").strip()

            if id_str in dataset:
                # print(dataset[id_str]['pdf_sections'].get("resumen_final"))
                # resumen_ref = dataset[id_str]['pdf_sections'].get("resumen_final").strip()
                resumen_ref_raw = dataset[id_str]['pdf_sections'].get("resumen_final")
                resumen_ref = str(resumen_ref_raw).strip() if resumen_ref_raw else ""
                if resumen_ref and output:
                    referencias[id_str] = resumen_ref
                    predicciones[id_str] = output

    return referencias, predicciones

# Evaluación con ROUGE
def evaluar_rouge(referencias, predicciones):
    rouge = evaluate.load("rouge")
    resultados = rouge.compute(predictions=list(predicciones.values()), references=list(referencias.values()))
    return resultados

# Evaluación con BERTScore
def evaluar_bertscore(referencias, predicciones):
    P, R, F1 = bertscore(list(predicciones.values()), list(referencias.values()), lang="es")
    return {
        "bert_precision": P.mean().item(),
        "bert_recall": R.mean().item(),
        "bert_f1": F1.mean().item()
    }

# Función principal
def main():
    referencias, predicciones = cargar_datos()

    if not referencias or not predicciones:
        print("No se encontraron pares válidos de referencia/hipótesis.")
        return

    print("Evaluando con ROUGE...")
    rouge_scores = evaluar_rouge(referencias, predicciones)
    print("Resultados ROUGE:", rouge_scores)

    print("\nEvaluando con BERTScore...")
    bert_scores = evaluar_bertscore(referencias, predicciones)
    print("Resultados BERTScore:", bert_scores)

if __name__ == "__main__":
    main()