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

def extract_sections_from_multiple_pdfs(pdf_paths):
    all_sections = []
    for report, pdf_path in tqdm(pdf_paths.items(), desc="Procesando informes PDF"):
        sections = extract_all_sections(pdf_path)
        sections['informe'] = report
        all_sections.append(sections)
    return all_sections

if __name__ == "__main__":
    pdf_paths = {
        "Albacete_VillarrealB": "data/reports/Albacete Balompié SAD - Villarreal CF “B” SAD.pdf",
        "Alhama_Levante": "data/reports/Alhama CF - Levante UD SAD.pdf",
        "Alhama_Betis": "data/reports/Alhama CF - Real Betis Balompié SAD.pdf",
        "Eldense_Eibar": "data/reports/CD Eldense - SD Éibar.pdf",
        "Eldense_VillarrealB": "data/reports/CD Eldense - Villarreal CF “B” SAD.pdf",
        "Elche_Espanyol": "data/reports/Elche CF SAD - RCD Espanyol de Barcelona SAD.pdf",
        "Barcelona_Athletic": "data/reports/FC Barcelona - Athletic Club.pdf",
        "Barcelona_Mallorca": "data/reports/FC Barcelona - RCD Mallorca SAD.pdf",
        "Barcelona_RealMadrid": "data/reports/FC Barcelona - Real Madrid CF.pdf",
        "Barcelona_LasPalmas": "data/reports/FC Barcelona - UD Las Palmas SAD.pdf",
        "Cartagena_Burgos": "data/reports/FC Cartagena - Burgos CF SAD.pdf",
        "Cartagena_Eldense": "data/reports/FC Cartagena - CD Eldense.pdf",
        "Cartagena_Espanyol": "data/reports/FC Cartagena - RCD Espanyol de Barcelona SAD.pdf",
        "Cartagena_Oviedo": "data/reports/FC Cartagena - Real Oviedo SAD.pdf",
        "Cartagena_Amorebieta": "data/reports/FC Cartagena - SD Amorebieta.pdf",
        "Cartagena_VillarrealB": "data/reports/FC Cartagena - Villarreal CF “B” SAD.pdf",
        "Cartagena_Burgos": "data/reports/FC Cartagena SAD - Burgos CF SAD.pdf",
        "Cartagena_Fuenlabrada": "data/reports/FC Cartagena SAD - CF Fuenlabrada SAD.pdf",
        "Cartagena_Girona": "data/reports/FC Cartagena SAD - Girona FC SAD.pdf",
        "Cartagena_Malaga": "data/reports/FC Cartagena SAD - Málaga CF SAD.pdf",
        "Cartagena_Racing": "data/reports/FC Cartagena SAD - Real Racing Club de Santander SAD.pdf",
        "Cartagena_Zaragoza": "data/reports/FC Cartagena SAD - Real Zaragoza SAD.pdf",
        "Cartagena_Ibiza": "data/reports/FC Cartagena SAD - UD Ibiza SAD.pdf",
        "JESanVicente_Atzeneta": "data/reports/FC Jove Español San Vicente - UE Atzeneta.pdf",
        "Levante_Sevilla": "data/reports/Levante UD SAD - Sevilla FC SAD.pdf",
        "Levante_Albacete": "data/reports/Levante UD SAD - Albacete Balompié SAD.pdf",
        "Levante_Athletic": "data/reports/Levante UD SAD - Athletic Club.pdf",
        "Levante_Osasuna": "data/reports/Levante UD SAD - Club Atlético Osasuna.pdf",
        "Levante_Barcelona": "data/reports/Levante UD SAD - FC Barcelona.pdf",
        "Levante_Rayo": "data/reports/Levante UD SAD - Rayo Vallecano de Madrid SAD.pdf",
        "Levante_Sevilla": "data/reports/Levante UD SAD - Sevilla FC SAD.pdf",
        "Levante_Sevilla1": "data/reports/Levante UD - Sevilla FC (1).pdf",
        "Espanyol_Barcelona": "data/reports/RCD Espanyol de Barcelona SAD - FC Barcelona.pdf",
        "Espanyol_Gijon": "data/reports/RCD Espanyol de Barcelona SAD - Real Sporting de Gijón SAD.pdf",
        "Mallorca_Alaves": "data/reports/RCD Mallorca SAD - Deportivo Alavés SAD.pdf",
        "Mallorca_Elche": "data/reports/RCD Mallorca SAD - Elche CF SAD.pdf",
        "Mallorca_Barcelona": "data/reports/RCD Mallorca SAD - FC Barcelona.pdf",
        "Mallorca_Getafe": "data/reports/RCD Mallorca SAD - Getafe CF SAD.pdf",
        "Mallorca_RealSociedad": "data/reports/RCD Mallorca SAD - Real Sociedad de Fútbol SAD.pdf",
        "Almeria_Alcorcon": "data/reports/UD Almería SAD - AD Alcorcón SAD.pdf",
        "Ibiza_Lugo": "data/reports/UD Ibiza SAD - CD Lugo SAD (1).pdf",
        "Ibiza_Malaga": "data/reports/UD Ibiza SAD - Málaga CF SAD.pdf",
        "Ibiza_Ponferradina": "data/reports/UD Ibiza SAD - SD Ponferradina SAD.pdf",
        "Valencia_Athletic": "data/reports/Valencia CF SAD - Athletic Club.pdf",
        "Valencia_Cadiz": "data/reports/Valencia CF SAD - Cádiz CF SAD.pdf",
        "Valencia_RealMadrid": "data/reports/Valencia CF SAD - Real Madrid CF.pdf",
        "Valencia_Sevilla": "data/reports/Valencia CF SAD - Sevilla FC SAD.pdf",
        "Valencia_Villarreal": "data/reports/Valencia CF SAD - Villarreal CF SAD.pdf",
        "ValenciaF_Leganes": "data/reports/Valencia Féminas CF - Levante UD SAD.pdf",
        "ValenciaF_RealMadrid": "data/reports/Valencia Féminas CF - Real Madrid CF.pdf",
        "ValenciaF_Sevilla": "data/reports/Valencia Féminas CF - Sevilla FC SAD.pdf",
        "ValenciaF_SportingHuelva": "data/reports/Valencia Féminas CF - Sporting Club de Huelva.pdf",
        "VillarrealB_Malaga": "data/reports/Villarreal CF _B_ - Málaga CF SAD.pdf",
        "VillarrealB_Gijon": "data/reports/Villarreal CF _B_ - Real Sporting de Gijón SAD.pdf",
        "VillarrealB_Eibar": "data/reports/Villarreal CF _B_ - SD Eibar SAD.pdf",
        "VillarrealB_Celta": "data/reports/Villarreal CF - RC Celta de Vigo.pdf",
        "Villarreal_LasPalmas": "data/reports/Villarreal CF - UD Las Palmas.pdf",
        "VillarrealB_Mirandes": "data/reports/Villarreal CF “B” SAD - CD Mirandés SAD.pdf",
        "VillarrealB_Andorra": "data/reports/Villarreal CF “B” SAD - FC Andorra.pdf",
        "Villarreal_Cadiz": "data/reports/Villarreal CF SAD - Cádiz CF SAD.pdf",
        "Villarreal_Atletico": "data/reports/Villarreal CF SAD - Club Atlético de Madrid SAD.pdf",
        "Villarreal_Elche": "data/reports/Villarreal CF SAD - Elche CF SAD.pdf",
        "Villarreal_Girona": "data/reports/Villarreal CF SAD - Girona FC SAD.pdf",
    }
    all_sections = extract_sections_from_multiple_pdfs(pdf_paths)
    df = pd.DataFrame(all_sections)
    df.to_csv("data/dataset/dataset.csv", index=False)
    print("Dataset guardado en data/dataset/dataset.csv")



    # sections = extract_all_sections(pdf_paths["Albacete_VillarrealB"])
    # for section, text in sections.items():
    #     print(f"--- {section.upper()} ---\n{text}\n")
