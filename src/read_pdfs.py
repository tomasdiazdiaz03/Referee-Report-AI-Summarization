import pdfplumber
import re

def extract_all_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])


def extract_text_between_markers(pdf_path, start_marker, end_marker):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        start_match = re.search(start_marker, text)
        end_match = re.search(end_marker, text[start_match.end():]) if start_match else None
        if start_match and end_match:
            return text[start_match.start():start_match.end() + end_match.start()].strip()
        return ""

def extract_text_asistentes(pdf_path, pattern):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        match = re.search(pattern, text)
        if match:
            return match.group(3).strip() if match.group(3) else ""
        return ""

def extract_all_sections(pdf_path):
    sections = {
        "condicion_fisica": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA CONDICIÓN FÍSICA Y POSICIONAMIENTO \(Si fuera necesario\):", 
            r"2 - ACTUACIÓN TÉCNICA"),
        "actuacion_tecnica": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA ACTUACIÓN TÉCNICA \(Si fuera necesario\):", 
            r"3 - ACTUACIÓN DISCIPLINARIA"),
        "actuacion_disciplinaria": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA ACTUACIÓN DISCIPLINARIA \(Si fuera necesario\):", 
            r"4 - MANEJO DEL PARTIDO"),
        "manejo_partido": extract_text_between_markers(pdf_path, 
            r"ACCIONES RESEÑABLES DEL ÁREA DE MANEJO DE PARTIDO", 
            r"5 - PERSONALIDAD"),
        "personalidad": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA PERSONALIDAD \(Si fuera necesario\):", 
            r"6 - TRABAJO EN EQUIPO"),
        "trabajo_equipo": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL TRABAJO EN EQUIPO \(Si fuera necesario\):", 
            r"Árbitro asistente 1: .*"),
        "asistente_1": extract_text_asistentes(pdf_path, 
            r"Árbitro asistente 1: (.|\n)*((Acierto Error Beneficio/Duda(.|\n)*)(JUGADAS DE FUERA DE JUEGO))"),
        "asistente_1_comentarios": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 1 \(Si fuera necesario\):", 
            r"Árbitro asistente 2: .*"),
        "asistente_2": extract_text_asistentes(pdf_path, 
            r"Árbitro asistente 2: (.|\n)*((Acierto Error Beneficio/Duda(.|\n)*)(JUGADAS DE FUERA DE JUEGO))"),
        "asistente_2_comentarios": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 2 \(Si fuera necesario\):", 
            r"4º Árbitro: .*"),
        "cuarto_arbitro": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL CUARTO ÁRBITRO \(Si fuera necesario\):", 
            r"Resumen final"),
        "resumen_final": extract_text_between_markers(pdf_path, 
            r"Resumen final", 
            r"OTRAS INCIDENCIAS RESEÑABLES NO INCLUIDAS ANTERIORMENTE:")
    }
    return sections

def extract_sections_from_multiple_pdfs(pdf_paths):
    all_sections = {}
    for pdf_path in pdf_paths:
        sections = extract_all_sections(pdf_path)
        all_sections[pdf_path] = sections
    return all_sections

if __name__ == "__main__":
    pdf_paths = [
        "data/reports/Albacete Balompié SAD - Villarreal CF “B” SAD.pdf",
        "data/reports/Alhama CF - Levante UD SAD.pdf"
    ]
    all_sections = extract_sections_from_multiple_pdfs(pdf_paths)
    for pdf_path, sections in all_sections.items():
        print(f"--- {pdf_path} ---")
        for section, text in sections.items():
            print(f"--- {section.upper()} ---\n{text}\n")

    # print(extract_all_text_from_pdf(pdf_paths[0]))