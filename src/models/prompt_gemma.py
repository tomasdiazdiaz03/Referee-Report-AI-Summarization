import ollama
from rule_phrase_system import generar_resumen_pdf, generar_resumen_txt
import json
from tqdm import tqdm

MODELO = "gemma3:12b"

# TODO Mencionar que debe comentar solo los aciertos y errores relevantes siguiendo lo marcado en el PDF ejemplo
def generar_outputs(modelo, contenido):
    prompt = f"""
    Eres un experto en arbitraje de fútbol. Dado el siguiente partido, genera un resumen profesional y conciso utilizando únicamente lenguaje natural español.
    Menciona todos los apartados relevantes sobre el árbitro, es decir: condición física, actuación técnica, incidencias de penaltis, incidencias disciplinarias, manejo del partido y trabajo en equipo. Si no dispones de información sobre alguno de los apartados, indica que el rendimiento en dicho apartado ha sido suficientemente bueno sin nada destacable.
    Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
    Debes incluir un único párrafo extenso para todos los apartados relacionados con el árbitro, un nuevo párrafo dedicado para el asistente 1, otro párrafo dedicado para el asistente 2 y otro párrafo dedicado para el cuarto árbitro. Si uno de ellos no tiene información, menciona que no ha sucedido ningún evento relevante sobre su rendimiento.
    Es muy importante que no cuestiones nada por ti mismo. Si no se indica claramente que ha sido un error, no lo pongas en duda ni lo interpretes como tal.
    No menciones nada antes ni después del resumen, céntrate en dar únicamente los párrafos pedidos. Aquí tienes el contenido de los apartados:

    {contenido}
    """
    respuesta = ollama.chat(model=modelo, messages=[
        {'role': 'system', 'content': 'Eres un experto en arbitraje de fútbol y redacción deportiva.'},
        {'role': 'user', 'content': prompt}
    ])
    return respuesta['message']['content']

def main():
    # PROCESAMIENTO DEL PRIMER RESUMEN DE CADA TIPO
    # print("Generando resumen TXT...")
    # resumenes_txt = generar_resumen_txt()
    # primer_txt_id = list(resumenes_txt.keys())[0]
    # contenido_txt = resumenes_txt[primer_txt_id]
    # print(f"Contenido TXT (ID {primer_txt_id}):\n{contenido_txt}\n")

    # print("Procesando con Gemma3:12b (TXT)...")
    # output_txt = generar_outputs(MODELO, contenido_txt)
    # print(f"\nResumen generado (TXT - ID {primer_txt_id}):\n{output_txt}\n")

    # print("Generando resumen PDF...")
    # resumenes_pdf = generar_resumen_pdf()
    # primer_pdf_id = list(resumenes_pdf.keys())[0]
    # contenido_pdf = resumenes_pdf[primer_pdf_id]
    # print(f"Contenido PDF (ID {primer_pdf_id}):\n{contenido_pdf}\n")

    # print("Procesando con Gemma3:12b (PDF)...")
    # output_pdf = generar_outputs(MODELO, contenido_pdf)
    # print(f"\nResumen generado (PDF - ID {primer_pdf_id}):\n{output_pdf}\n")

    # PROCESAMIENTO DE TODOS LOS RESUMENES
    # Lista para almacenar los resultados
    resultados = []

    print("Generando resúmenes TXT...")
    resumenes_txt = generar_resumen_txt()
    print("Procesando resúmenes TXT con Gemma3:12b...")
    # for txt_id, contenido_txt in resumenes_txt.items():
    for txt_id, contenido_txt in tqdm(resumenes_txt.items(), desc="Procesando TXT"):
        print(f"Procesando resumen TXT (ID {txt_id})...")
        output_txt = generar_outputs(MODELO, contenido_txt)
        resultados.append({
            "id": txt_id,
            "tipo": "TXT",
            "input": contenido_txt,
            "output": output_txt
        })

    print("Generando resúmenes PDF...")
    resumenes_pdf = generar_resumen_pdf()
    print("Procesando resúmenes PDF con Gemma3:12b...")
    # for pdf_id, contenido_pdf in resumenes_pdf.items():
    for pdf_id, contenido_pdf in tqdm(resumenes_pdf.items(), desc="Procesando PDF"):
        print(f"Procesando resumen PDF (ID {pdf_id})...")
        output_pdf = generar_outputs(MODELO, contenido_pdf)
        resultados.append({
            "id": pdf_id,
            "tipo": "PDF",
            "input": contenido_pdf,
            "output": output_pdf
        })

    # Guardar los resultados en un archivo JSON
    with open("./data/output/resumenes_generados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print("Resúmenes generados y guardados en 'data/output/resumenes_generados.json'.")



if __name__ == "__main__":
    main()
