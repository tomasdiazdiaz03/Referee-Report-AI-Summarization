import ollama
from rule_phrase_system import generar_resumen_pdf, generar_resumen_txt

MODELO = "gemma3:12b"

# TODO Mencionar que debe comentar solo los aciertos y errores relevantes siguiendo lo marcado en el PDF ejemplo
def generar_outputs(modelo, contenido):
    prompt = f"""
    Eres un experto en arbitraje de fútbol. Dado el siguiente partido, genera un resumen profesional y conciso utilizando lenguaje natural.
    Menciona todos los apartados relevantes sobre el árbitro. Si no dispones de información sobre alguno de los apartados, indica que el rendimiento en dicho apartado ha sido suficientemente bueno sin nada destacable.
    Debes incluir un único párrafo extenso para todos los apartados relacionados con el árbitro, un nuevo párrafo dedicado para el asistente 1, otro para el asistente 2 y otro para el cuarto árbitro. Si uno de ellos no tiene información, menciona que no ha sucedido ningún evento relevante. Aquí tienes el contenido de los apartados:

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
