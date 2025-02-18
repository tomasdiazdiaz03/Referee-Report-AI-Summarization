import os
import json
import pdfplumber
import re
import pandas as pd
from tqdm import tqdm

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
            text_asistente = match.group(0).strip()
            match_tabla = re.search(r"Acierto Error Beneficio/Duda\n(.*?)(?=\nJUGADAS DE FUERA DE JUEGO)", text_asistente, re.DOTALL)
            if match_tabla:
                return match_tabla.group(1).strip()
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
            # r"Árbitro asistente 1: (.|\n)*((Acierto Error Beneficio/Duda(.|\n)*)(JUGADAS DE FUERA DE JUEGO))"),
            r"(Árbitro asistente 1:(.|\n)*COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 1 \(Si fuera necesario\):)"),
        "asistente_1_comentarios": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 1 \(Si fuera necesario\):", 
            r"Árbitro asistente 2: .*"),
        "asistente_2": extract_text_asistentes(pdf_path, 
            # r"Árbitro asistente 2: (.|\n)*((Acierto Error Beneficio/Duda(.|\n)*)(JUGADAS DE FUERA DE JUEGO))"),
            r"(Árbitro asistente 2:(.|\n)*COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 2 \(Si fuera necesario\):)"),
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

def extract_sections_from_multiple_pdfs(matches):
    all_sections = []
    for id, match_info in tqdm(matches.items(), desc="Procesando informes PDF"):
        pdf_path = match_info.get("pdf")
        match = match_info.get("match")
        if pdf_path is None:
            print(f"Archivo PDF no disponible para el partido: {match}")
            continue
        if not os.path.exists(pdf_path):
            print(f"Archivo no encontrado: {pdf_path}")
            continue
        try:
            sections = extract_all_sections(pdf_path)
            sections = {"id": id, "match": match, **sections}
            all_sections.append(sections)
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")
    return all_sections

if __name__ == "__main__":
    pass
    # sections = extract_all_sections(pdf_paths["Albacete_VillarrealB"])
    # for section, text in sections.items():
    #     print(f"--- {section.upper()} ---\n{text}\n")
