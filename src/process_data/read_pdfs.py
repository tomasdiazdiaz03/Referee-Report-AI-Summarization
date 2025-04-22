import os
import json
import pdfplumber
import re
import pandas as pd
from tqdm import tqdm

def extract_all_text_from_pdf(pdf_path):
    """
    Abre un archivo PDF y extrae todo el texto de todas las páginas.
    """
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])


def extract_text_between_markers(pdf_path, start_marker, end_marker):
    """
    Abre un archivo PDF y extrae el texto contenido entre dos marcadores determinados, en este caso, las expresiones regulares.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        start_match = re.search(start_marker, text)
        end_match = re.search(end_marker, text[start_match.end():]) if start_match else None
        if start_match and end_match:
            return text[start_match.end():start_match.end() + end_match.start()].strip()
        return ""

def extract_tablas_asistentes(asistente1, pdf_path):
    """
    Extrae las dos tablas del PDF correspondientes a los incidentes relacionados con uno de los asistentes y devuelve un diccionario con los datos estructurados.
    """
    asistente = {
        "acciones": {},
        "jugadas_fuera_de_juego": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        break_asistente1 = False
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                # Convertir la tabla en DataFrame para facilitar su manejo
                df = pd.DataFrame(table)

                # Si es la primera tabla, buscamos las filas con la cantidad de acciones no sancionadas
                if "DECISIONES DE FUERA DE JUEGO SEÑALADOS:" in df.to_string():
                    df.columns = df.iloc[0]  # Primera fila como encabezado
                    df = df[1:]  # Eliminar la primera fila
                    df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)  # Limpiar nombres de columnas

                    for _, row in df.iterrows():
                        if row.iloc[0] in ["DECISIONES DE FUERA DE JUEGO SEÑALADOS:", 
                                      "DECISIONES RELEVANTES DE FUERA DE JUEGO NO SEÑALADOS:",
                                      "AYUDA AL ÁRBITRO EN ACCIONES DE ÁREA",
                                      "AYUDA AL ÁRBITRO EN ACCIONES DISCIPLINARIAS:",
                                      "RETRASAR LA BANDERA EN ACCIONES PRÓXIMAS A GOL (SOLO CON VAR):"]:
                            asistente["acciones"][row.iloc[0]] = {
                                "Acierto": row.iloc[1] if row.iloc[1] != "" else "0",
                                "Error": row.iloc[2] if row.iloc[2] != "" else "0"
                            }
                        elif row.iloc[0] == "INFRACCIONES INDICADAS":
                            asistente["acciones"][row.iloc[0]] = {
                                "Error": row.iloc[2] if row.iloc[2] != "" else "0"
                            }

                # Si es la segunda tabla, extraer incidentes del área de penalti
                elif "JUGADAS DE FUERA DE JUEGO" in df.to_string() and df.shape[1] == 5:
                    headers = df.iloc[1]  # Segunda fila como encabezado
                    df = df[2:]  # Eliminar las dos primeras filas
                    df.columns = headers  # Asignar encabezados
                    df = df.rename(columns=lambda x: x.strip())  # Limpiar nombres de columnas
                    
                    # Guardar los incidentes en la lista
                    for _, row in df.iterrows():
                        asistente["jugadas_fuera_de_juego"].append({
                            "Minuto": row.get("Minuto", "").strip(),
                            "Decision": row.get("Decisión", "").strip(),
                            "Opinion_evaluador": row.get("Opinión del evaluador", "").strip()
                        })
                    if asistente1:
                        break_asistente1 = True
                        break
            if break_asistente1:
                break

    return asistente

def extract_penalty_incidences_from_pdf(pdf_path):
    """
    Extrae y concatena las tablas del PDF correspondientes a los incidentes de área de penalti,
    acumulando todas las tablas después de "ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI"
    hasta el delimitador "OTRAS ACCIONES DE ACTUACIÓN TÉCNICA RESEÑABLES".
    Omite filas nulas.
    """
    incidences = {
        "sanciones": {},
        "incidentes_area_penalti": []
    }

    accumulating = False  # Bandera para acumular tablas después del marcador inicial
    all_incidentes_rows = []  # Lista para acumular filas de todas las tablas combinadas

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)

                # Si encontramos "ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI", procesamos esa tabla
                if "ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI" in df.to_string():
                    df.columns = df.iloc[0]  # Primera fila como encabezado
                    df = df[1:]  # Eliminar encabezado viejo
                    df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)

                    for _, row in df.iterrows():
                        if row.iloc[0] in ["PENALTIS SEÑALADOS:", "ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI:"]:
                            incidences["sanciones"][row.iloc[0]] = {
                                "Acierto": row.iloc[1] if row.iloc[1] != "" else "0",
                                "Error": row.iloc[2] if row.iloc[2] != "" else "0"
                            }

                    # Activar acumulación de tablas tras encontrar la tabla de "ACCIONES DE ÁREA SIGNIFICATIVAS"
                    accumulating = True

                # Si estamos acumulando tablas tras el marcador inicial
                elif accumulating:
                    # Si encontramos el delimitador final, detener la acumulación
                    if "OTRAS ACCIONES DE ACTUACIÓN TÉCNICA RESEÑABLES" in df.to_string():
                        accumulating = False
                        break

                    # Procesar encabezados dinámicamente en función de si es la primera tabla acumulada o no
                    if len(all_incidentes_rows) == 0:
                        df = df[2:]  # Eliminar las dos primeras filas para la primera tabla acumulada
                    else:
                        df.columns = df.iloc[0]  # Usar la primera fila como encabezado si hay tablas continuas
                        df = df[1:]  # Eliminar encabezado viejo

                    # Agregar filas de la tabla a la lista acumuladora
                    all_incidentes_rows.extend(df.values.tolist())

    # Crear DataFrame final concatenado y eliminar filas con valores nulos
    if all_incidentes_rows:
        df_final = pd.DataFrame(all_incidentes_rows, columns=['Minuto', 'Decisión', 'Opinión del evaluador', 'Tipo acción', 'Breve descripción de la acción'])
        df_final.drop(columns=['Tipo acción', 'Breve descripción de la acción'], inplace=True)
        df_final.dropna(subset=["Minuto", "Decisión", "Opinión del evaluador"], inplace=True)

        # Recorrer el DataFrame filtrado y añadir las filas relevantes al diccionario final
        for _, row in df_final.iterrows():
            if all(row):  # Verificar que no haya valores nulos
                incidences["incidentes_area_penalti"].append({
                    "Minuto": row.get("Minuto", "").strip(),
                    "Decision": row.get("Decisión", "").strip(),
                    "Opinion_evaluador": row.get("Opinión del evaluador", "").strip()
                })

    return incidences

def extract_discipline_incidences_from_pdf(pdf_path):
    """
    Extrae y concatena las tablas del PDF correspondientes a los incidentes disciplinarios,
    acumulando todas las tablas después de "TARJETAS AMARILLAS MOSTRADAS" hasta encontrar el delimitador final.
    Omite filas nulas y aquellas que contengan el string "INCIDENTES DISCIPLINARIOS".
    """
    incidences = {
        "tarjetas": {},
        "incidentes_disciplinarios": []
    }

    accumulating = False  # Bandera para acumular las tablas tras "TARJETAS AMARILLAS MOSTRADAS"
    all_incidentes_rows = []  # Lista para acumular filas

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                df = pd.DataFrame(table)

                # Si encontramos "TARJETAS AMARILLAS MOSTRADAS", procesamos esa tabla específica
                if "TARJETAS AMARILLAS MOSTRADAS" in df.to_string():
                    df.columns = df.iloc[0]  # Primera fila como encabezado
                    df = df[1:]  # Eliminar encabezado viejo
                    df = df.rename(columns=lambda x: x.strip() if isinstance(x, str) else x)

                    for _, row in df.iterrows():
                        if row.iloc[0] in ["TARJETAS AMARILLAS MOSTRADAS:", "2ª TARJETAS AMARILLAS MOSTRADAS:", "2ª TARJETAS AMARILLAS NO MOSTRADAS:",
                                           "TARJETAS ROJAS DIRECTAS MOSTRADAS:", "TARJETAS ROJAS DIRECTAS NO MOSTRADAS:"]:
                            incidences["tarjetas"][row.iloc[0]] = {
                                "Acierto": row.iloc[1] if row.iloc[1] != "" else "0",
                                "Error": row.iloc[2] if row.iloc[2] != "" else "0"
                            }
                        elif row.iloc[0] == "TARJETAS AMARILLAS NO MOSTRADAS:":
                            incidences["tarjetas"][row.iloc[0]] = {
                                "Error": row.iloc[2] if row.iloc[2] != "" else "0"
                            }

                    # Activar acumulación de tablas tras encontrar la tabla de "TARJETAS AMARILLAS MOSTRADAS"
                    accumulating = True

                # Si estamos acumulando tablas (después de encontrar "TARJETAS AMARILLAS MOSTRADAS")
                elif accumulating:
                    # Si encontramos el delimitador, detener la acumulación
                    if "COMENTARIOS ADICIONALES A LA ACTUACIÓN DISCIPLINARIA" in df.to_string():
                        accumulating = False
                        break

                    # Procesar la tabla acumulada: asignar encabezados si es la primera tabla acumulada
                    if len(all_incidentes_rows) == 0:
                        df = df[2:]  # Eliminar las dos primeras filas
                    else:
                        df.columns = df.iloc[0]  # Asignar encabezado si hay más tablas continuas
                        df = df[1:]

                    # Agregar las filas de la tabla a la lista acumuladora
                    all_incidentes_rows.extend(df.values.tolist())

    # Crear DataFrame con las filas acumuladas y eliminar filas nulas o con "INCIDENTES DISCIPLINARIOS"
    if all_incidentes_rows:
        df_final = pd.DataFrame(all_incidentes_rows, columns=['Minuto', 'Decisión árbitro', 'Opinión del evaluador', 'Tipo acción', 'Breve descripción de la acción'])
        df_final.drop(columns=['Tipo acción', 'Breve descripción de la acción'], inplace=True)
        df_final.dropna(subset=["Minuto", "Decisión árbitro", "Opinión del evaluador"], inplace=True)

        # Recorrer el DataFrame filtrado y añadir las filas relevantes al diccionario final
        for _, row in df_final.iterrows():
            # Ignorar filas vacías y aquellas que contengan "INCIDENTES DISCIPLINARIOS"
            if all(row) and "INCIDENTES DISCIPLINARIOS" not in row.to_string():
                incidences["incidentes_disciplinarios"].append({
                    "Minuto": row.get("Minuto", "").strip(),
                    "Decision_arbitro": row.get("Decisión árbitro", "").strip(),
                    "Opinion_evaluador": row.get("Opinión del evaluador", "").strip()
                })

    return incidences

def extract_all_sections(pdf_path):
    """
    Extrae todas las secciones de un informe dado en formato PDF.
    """
    sections = {
        "condicion_fisica": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA CONDICIÓN FÍSICA Y POSICIONAMIENTO \(Si fuera necesario\):", 
            r"2 - ACTUACIÓN TÉCNICA"),
        "actuacion_tecnica": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA ACTUACIÓN TÉCNICA \(Si fuera necesario\):", 
            r"3 - ACTUACIÓN DISCIPLINARIA"),
        "incidencias_penaltis": extract_penalty_incidences_from_pdf(pdf_path),
        "actuacion_disciplinaria": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA ACTUACIÓN DISCIPLINARIA \(Si fuera necesario\):", 
            r"4 - MANEJO DEL PARTIDO"),
        "incidencias_disciplinarias": extract_discipline_incidences_from_pdf(pdf_path),
        "manejo_partido": extract_text_between_markers(pdf_path, 
            r"ACCIONES RESEÑABLES DEL ÁREA DE MANEJO DE PARTIDO", 
            r"5 - PERSONALIDAD"),
        "personalidad": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES A LA PERSONALIDAD \(Si fuera necesario\):", 
            r"6 - TRABAJO EN EQUIPO"),
        "trabajo_equipo": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL TRABAJO EN EQUIPO \(Si fuera necesario\):", 
            r"Árbitro asistente 1: .*"),
        "asistente_1": extract_tablas_asistentes(True, pdf_path), # r"(Árbitro asistente 1:(.|\n)*COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 1 \(Si fuera necesario\):)"),
        "asistente_1_comentarios": extract_text_between_markers(pdf_path, 
            r"COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 1 \(Si fuera necesario\):", 
            r"Árbitro asistente 2: .*"),
        "asistente_2": extract_tablas_asistentes(False, pdf_path), # r"(Árbitro asistente 2:(.|\n)*COMENTARIOS ADICIONALES SOBRE EL ÁRBITRO ASISTENTE 2 \(Si fuera necesario\):)"),
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
    """
    Extrae las secciones de todos los informes PDF de una lista de partidos, en caso de que exista la ruta.
    """
    all_sections = {}
    for id, match_info in tqdm(matches.items(), desc="Procesando informes PDF"):
        pdf_path = match_info.get("pdf")
        if pdf_path is None:
            print(f"Archivo PDF no disponible para el partido: {match_info.get("match")}")
            continue
        if not os.path.exists(pdf_path):
            print(f"Archivo no encontrado: {pdf_path}")
            continue
        try:
            sections = extract_all_sections(pdf_path)
            all_sections[id] = sections
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")
    return all_sections


if __name__ == "__main__":
    pdf_path = "data/reports/Levante UD SAD - Rayo Vallecano de Madrid SAD.pdf"
    # pdf_path = "data/reports/UD Ibiza SAD - SD Ponferradina SAD.pdf"
    # print(extract_all_text_from_pdf(pdf_path))
    # print(extract_discipline_incidences_from_pdf(pdf_path))
    print(extract_penalty_incidences_from_pdf(pdf_path))
    # extract_discipline_incidences_from_pdf(pdf_path)
    # Imprimir todas las secciones de data1 de forma legible
    # for section, content in data1.items():
    #     print(f"--- {section.upper()} ---")
    #     if isinstance(content, pd.DataFrame):
    #         print(content.to_string(index=False))
    #     elif isinstance(content, dict):
    #         for key, value in content.items():
    #             print(f"{key}: {value}")
    #     else:
    #         print(content)
    #     print("\n")