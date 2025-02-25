import json
import os


def extract_teams_names_from_txt(txt_file):
    """
    Extrae los nombres de los equipos de un archivo TXT y los imprime en pantalla. (originalmente usada para crear las keys del diccionario de partidos)
    """
    with open(txt_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            parts = first_line.split()
            team1_parts = []
            team2_parts = []
            score_found = False

            for part in parts:
                if part.isdigit():
                    score_found = True
                elif not score_found:
                    team1_parts.append(part)
                else:
                    team2_parts.append(part)

            team1 = " ".join(team1_parts)
            team2 = " ".join(team2_parts)
            print(f"{team1}_{team2}")
            

def extract_events_from_txt(txt_file):
    """
    Extrae los eventos de partido de un archivo TXT y los devuelve en un diccionario.
    """
    print(f"Procesando archivo TXT: {txt_file}")
    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    events = []
    asistente1_info = {}
    asistente2_info = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line == "Eventos:":
            current_section = "events"
            continue
        elif line == "AAA1:":
            current_section = "asistente_1"
            continue
        elif line == "AAA2:":
            current_section = "asistente_2"
            continue
        elif line == "" and current_section not in ["asistente_1", "asistente_2"]:
            current_section = None
            continue
        
        if current_section == "events":
            parts = line.split(sep=" ")
            minute = parts[0]

            i = 1
            codes = []
            while parts[i] != '': # or parts[i+1] != '':
                codes.append(parts[i])
                i += 1

            while parts[i] == '':
                i += 1
            description = " ".join(parts[i:])
            event = {
                "minute": minute,
                "codes": codes,
                "description": description
            }
            events.append(event)

        elif current_section == "asistente_1" and line != "":
            parts = line.split(sep=" ")
            key = parts[0].split(sep=":")[0]
            asistente1_info[key] = " ".join(parts[1:])

        elif current_section == "asistente_2" and line != "":
            parts = line.split(sep=" ")
            parts = [part for part in parts if "__" not in part]
            key = parts[0].split(sep=":")[0]
            asistente2_info[key] = " ".join(parts[1:])
    
    return {
        "events": events,
        "asistente_1": asistente1_info,
        "asistente_2": asistente2_info
    }

def extract_events_from_multiple_txts(txt_files):
    """
    Extrae los eventos de varios informes en formato TXT y los devuelve en un diccionario.
    """
    all_events = {}
    for id, match_info in txt_files.items():
        txt_file = match_info.get("txt")
        match = match_info.get("match")
        if txt_file is None:
            print(f"Archivo TXT no disponible para el partido: {match}")
            continue
        if not os.path.exists(txt_file):
            print(f"Archivo no encontrado para el partido {txt_file}")
            continue
        events = extract_events_from_txt(txt_file)
        all_events[id] = events
    return all_events