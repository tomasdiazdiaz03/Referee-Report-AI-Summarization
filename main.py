from flask import Flask, request, render_template, redirect, url_for, session
import os
import uuid

from src.process_data.read_pdfs import extract_all_sections
from src.process_data.read_txts import extract_events_from_txt
from src.process_data.preprocess import preprocess_match_data, eliminar_beneficio_duda
from src.models.rule_phrase_system import generar_resumen_pdf, generar_resumen_txt
from src.models.prompt_gemma import generar_outputs

app = Flask(__name__)
app.secret_key = 'clave_TFM'
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODELO = "gemma3:12b"

PROMPTS = {
    "arbitro": """
Genera un resumen de un solo párrafo de los datos del árbitro.
Si no dispones de información sobre alguno de los apartados, indica que el rendimiento en dicho apartado ha sido suficientemente bueno sin nada destacable.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
""",
    "asistente_1": """
Genera un resumen breve de un párrafo de los datos del asistente 1.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si no tiene información, indica que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
""",
    "asistente_2": """
Genera un resumen breve de un párrafo de los datos del asistente 2.
Si hay cero aciertos, no menciones los aciertos. Si hay cero errores, no menciones los errores.
Si no tiene información, indica que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
""",
    "cuarto_arbitro": """
Genera un resumen breve de un párrafo de los datos del cuarto árbitro.
Si no tiene información, indica que no ha sucedido ningún evento relevante sobre su rendimiento.
Si un evento no se indica claramente que ha sido un error, no lo pongas en duda.

Aquí tienes el contenido de los apartados:
{contenido}
"""
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reprocess', methods=['POST'])
def reprocess_file():
    if 'last_file' not in session:
        return redirect(url_for('index'))
    
    filepath = session['last_file']
    
    if filepath.lower().endswith('.pdf'):
        result = process_pdf(filepath)
    elif filepath.lower().endswith('.txt'):
        result = process_txt(filepath)
    else:
        return redirect(url_for('index'))

    return render_template('resultado.html', resultado=result)

# Modifica la función upload_file para guardar el archivo en la sesión
@app.route('/upload', methods=['POST'])
def upload_report():
    file = request.files['file']
    if not file:
        return redirect(url_for('index'))
    
    file_id = str(uuid.uuid4())
    filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{file.filename}")
    file.save(filename)
    session['last_file'] = filename  # Guardamos la ruta del archivo en la sesión

    if file.filename.lower().endswith('.pdf'):
        result = process_pdf(filename)
    elif file.filename.lower().endswith('.txt'):
        result = process_txt(filename)
    else:
        return redirect(url_for('index'))

    return render_template('resultado.html', resultado=result)

def process_pdf(filepath):
    sections = extract_all_sections(filepath)
    match = {"pdf_sections": sections, "txt_events": None}
    match = preprocess_match_data(match)
    match = eliminar_beneficio_duda(match)
    resumenes = generar_resumen_pdf(match)
    outputs = {rol: generar_outputs(MODELO, texto, PROMPTS[rol]) for rol, texto in resumenes.items()}
    return outputs

def process_txt(filepath):
    events = extract_events_from_txt(filepath)
    match = {"pdf_sections": None, "txt_events": {"events": events}}
    match = preprocess_match_data(match)
    match = eliminar_beneficio_duda(match)
    resumenes = generar_resumen_txt(match)
    outputs = {rol: generar_outputs(MODELO, texto, PROMPTS[rol]) for rol, texto in resumenes.items()}
    return outputs

if __name__ == '__main__':
    app.run(debug=True)
