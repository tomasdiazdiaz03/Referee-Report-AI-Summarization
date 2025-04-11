import ollama
from rule_phrase_system import generar_resumen_pdf, generar_resumen_txt

MODELO = "gemma3:12b"

def generar_outputs(modelo, contenido):
    prompt = f"""
    Eres un experto en arbitraje de fútbol. Dado el siguiente partido, genera un resumen profesional y conciso utilizando lenguaje natural. Si se te dan varios apartados, quiero que menciones únicamente los que sí tengan información. Si no hay información sobre un apartado, ignóralo. Si se te dan numerosos eventos, resume lo acontecido en el partido. Todo esto debe ocupar un párrafo extenso:

    {contenido}
    """
    respuesta = ollama.chat(model=modelo, messages=[
        {'role': 'system', 'content': 'Eres un experto en arbitraje de fútbol y redacción deportiva.'},
        {'role': 'user', 'content': prompt}
    ])
    return respuesta['message']['content']

def main():
    print("Generando resumen PDF...")
    resumenes_pdf = generar_resumen_pdf()
    primer_pdf_id = list(resumenes_pdf.keys())[0]
    contenido_pdf = resumenes_pdf[primer_pdf_id]

    print("Procesando con Gemma3:12b (PDF)...")
    output_pdf = generar_outputs(MODELO, contenido_pdf)
    print(f"\nResumen generado (PDF - ID {primer_pdf_id}):\n{output_pdf}\n")

    print("Generando resumen TXT...")
    resumenes_txt = generar_resumen_txt()
    primer_txt_id = list(resumenes_txt.keys())[0]
    contenido_txt = resumenes_txt[primer_txt_id]

    print("Procesando con Gemma3:12b (TXT)...")
    output_txt = generar_outputs(MODELO, contenido_txt)
    print(f"\nResumen generado (TXT - ID {primer_txt_id}):\n{output_txt}\n")

if __name__ == "__main__":
    main()
