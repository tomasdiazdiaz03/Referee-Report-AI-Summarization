import ollama
from src.models.rule_phrase_system import generar_resumen_pdf_dataset, generar_resumen_txt_dataset
import json
from tqdm import tqdm
from langdetect import detect

MODELO = "gemma3:12b"

# # Prompt base
# prompt_base = """
# Responde exclusivamente en español. No incluyas ningún comentario adicional.

# Eres un experto en arbitraje de fútbol. Dado el siguiente partido, genera un resumen profesional y conciso utilizando lenguaje natural.
# Menciona todos los apartados relevantes sobre el árbitro, es decir: condición física, actuación técnica, incidencias de penaltis, incidencias disciplinarias, manejo del partido y trabajo en equipo. Si no dispones de información sobre alguno de los apartados, indica que el rendimiento en dicho apartado ha sido suficientemente bueno sin nada destacable.
# Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
# Debes incluir un único párrafo extenso para todos los apartados relacionados con el árbitro, un nuevo párrafo dedicado para el asistente 1, otro párrafo dedicado para el asistente 2 y otro párrafo dedicado para el cuarto árbitro. Si uno de ellos no tiene información, menciona que no ha sucedido ningún evento relevante sobre su rendimiento.
# Es muy importante que no cuestiones nada por ti mismo. Si no se indica claramente que ha sido un error, no lo pongas en duda ni lo interpretes como tal.
# No menciones nada antes ni después del resumen, céntrate en dar únicamente los párrafos pedidos. Aquí tienes el contenido de los apartados:

# {contenido}
# """

# Prompt base árbitro
prompt_arbitro = """
Genera un resumen de un solo párrafo de los datos del árbitro.
Si no dispones de información sobre alguno de los apartados, indica que el rendimiento en dicho apartado ha sido suficientemente bueno sin nada destacable.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
"""

# Prompt asistente 1
prompt_asistente_1 = """
Genera un resumen breve de un párrafo de los datos del asistente 1.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si el contenido del árbitro no tiene información, simplemente menciona que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
"""

# Prompt asistente 2
prompt_asistente_2 = """
Genera un resumen breve de un párrafo de los datos del asistente 2.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si el contenido del árbitro no tiene información, simplemente menciona que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
"""

# Prompt cuarto árbitro
prompt_cuarto = """
Genera un resumen breve de un párrafo de los datos del cuarto árbitro.
Si el contenido del árbitro no tiene información, simplemente menciona que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
"""


# # Prompt auxiliar simple
# prompt_aux = """
# Paso 1: Escribe un único párrafo sobre el árbitro (condición física, técnica, penaltis, disciplina, manejo y trabajo en equipo).

# Paso 2: Escribe un único párrafo sobre el asistente 1.

# Paso 3: Escribe un único párrafo sobre el asistente 2.

# Paso 4: Escribe un único párrafo sobre el cuarto árbitro.

# Si no hay información, indica que no hay eventos relevantes. Usa únicamente español.

# "El árbitro principal demostró una correcta condición física a lo largo del encuentro. Su actuación técnica fue adecuada, aunque se observa una tendencia a permitir ciertas situaciones de contacto sin mostrar una intervención contundente. En relación a las incidencias de penaltis, no se señalaron penalties, pero sí se registraron dos acciones de forcejeo en el área que no fueron consideradas falta. El manejo del partido mostró áreas de mejora, como la necesidad de una gestión más firme en situaciones de alteración como la protagonizada por los jugadores 18 y 8, donde se requería de una intervención más autoritaria para disuadir la alteración. Se observó que tuvo que indicar a un jugador de su propio equipo para que se situara correctamente en el momento de la reanudación del juego. El trabajo en equipo con los asistentes pareció correcto, sin destacar aspectos negativos.\n\nEl asistente 1 mantuvo una línea general correcta, permitiendo la continuación del juego en varias situaciones límite que terminaron en ocasiones de gol para el equipo local, en las que su criterio de interferencia con el juego fue crucial. En todas ellas, se mantuvo la continuidad del juego y no hubo motivo para considerar la existencia de fuera de juego.\n\nEl asistente 2, de manera similar, permitió la continuación del juego en varias situaciones muy ajustadas que resultaron en goles del equipo local. Su criterio de interferencia con el juego también influyó en la decisión de no señalar fuera de juego en esas acciones.\n\nEl cuarto árbitro no se registró ninguna incidencia relevante sobre su rendimiento."

# Aquí está el contenido de los apartados que debes resumir:
# {contenido}
# """

def generar_outputs(modelo, contenido, prompt):
    prompt = prompt.format(contenido=contenido)
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
    resumenes_txt = generar_resumen_txt_dataset()
    for txt_id, secciones_txt in tqdm(resumenes_txt.items(), desc="Procesando TXT"):
        print(f"\nProcesando informe TXT ID {txt_id}...")

        resumen_txt = {
            "id": txt_id,
            "tipo": "TXT",
            "input_arbitro": secciones_txt.get("arbitro", ""),
            "input_asistente_1": secciones_txt.get("asistente_1", ""),
            "input_asistente_2": secciones_txt.get("asistente_2", ""),
            "input_cuarto_arbitro": secciones_txt.get("cuarto_arbitro", "")
        }

        resumen_txt["output_arbitro"] = generar_outputs(MODELO, resumen_txt["input_arbitro"], prompt_arbitro)
        resumen_txt["output_asistente_1"] = generar_outputs(MODELO, resumen_txt["input_asistente_1"], prompt_asistente_1)
        resumen_txt["output_asistente_2"] = generar_outputs(MODELO, resumen_txt["input_asistente_2"], prompt_asistente_2)
        resumen_txt["output_cuarto_arbitro"] = generar_outputs(MODELO, resumen_txt["input_cuarto_arbitro"], prompt_cuarto)

        resultados.append(resumen_txt)

    print("Generando resúmenes PDF...")
    resumenes_pdf = generar_resumen_pdf_dataset()
    for pdf_id, secciones_pdf in tqdm(resumenes_pdf.items(), desc="Procesando TXT"):
        print(f"\nProcesando informe PDF ID {pdf_id}...")

        resumen_pdf = {
            "id": pdf_id,
            "tipo": "PDF",
            "input_arbitro": secciones_pdf.get("arbitro", ""),
            "input_asistente_1": secciones_pdf.get("asistente_1", ""),
            "input_asistente_2": secciones_pdf.get("asistente_2", ""),
            "input_cuarto_arbitro": secciones_pdf.get("cuarto_arbitro", "")
        }

        resumen_pdf["output_arbitro"] = generar_outputs(MODELO, resumen_pdf["input_arbitro"], prompt_arbitro)
        resumen_pdf["output_asistente_1"] = generar_outputs(MODELO, resumen_pdf["input_asistente_1"], prompt_asistente_1)
        resumen_pdf["output_asistente_2"] = generar_outputs(MODELO, resumen_pdf["input_asistente_2"], prompt_asistente_2)
        resumen_pdf["output_cuarto_arbitro"] = generar_outputs(MODELO, resumen_pdf["input_cuarto_arbitro"], prompt_cuarto)

        resultados.append(resumen_pdf)
        

    # Guardar los resultados en un archivo JSON
    with open("./data/output/resumenes_generados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print("Resúmenes generados y guardados en 'data/output/resumenes_generados.json'.")



if __name__ == "__main__":
    main()
