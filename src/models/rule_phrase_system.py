import json
import re
from collections import defaultdict

#########################
# Frases para resúmenes #
#########################

plantilla_frase_condicion_fisica = "Sobre la condición física del árbitro, {condicion_fisica}"
plantilla_frase_actuacion_tecnica = "Sobre la actuación técnica del árbitro, {actuacion_tecnica}"
plantilla_frase_incidencias_penaltis = "Sobre las incidencias de penaltis, {incidencias_penaltis}"
plantilla_frase_actuacion_disciplinaria = "Sobre la actuación disciplinaria, {actuacion_disciplinaria}"
plantilla_frase_incidencias_disciplinarias = "Sobre las incidencias disciplinarias, {incidencias_disciplinarias}"
plantilla_frase_manejo_partido = "Sobre el manejo del partido por parte del árbitro, la estructura de eventos seguida es: 'Minuto' 'Breve descripción de la acción', y los eventos son los siguientes: {manejo_partido} Como comentarios adicionales, se incluyen los siguientes: {comentarios_adicionales_manejo}"
plantilla_frase_personalidad = "Sobre la personalidad del árbitro, {personalidad}"
plantilla_frase_trabajo_equipo = "Sobre el trabajo en equipo, {trabajo_equipo}"
plantilla_frase_asistente_1 = "Sobre el asistente 1, {asistente_1}"
plantilla_frase_asistente_2 = "Sobre el asistente 2, {asistente_2}"
plantilla_frase_cuarto_arbitro = "Sobre el cuarto árbitro, {cuarto_arbitro}"


#######################################
# Diccionarios de tópicos por sección #
#######################################


###################################################
# Funciones de procesamiento de datos del dataset #
###################################################

def count_txts_pdfs_not_nulls():
    """
    Contar los IDs de los informes que tienen solo texto, solo PDF o ambos y devolver una lista con cada tipo
    """
    # Cargar el dataset desde el archivo JSON
    with open('./data/dataset/dataset_clean.json', 'r', encoding='utf-8') as file:
        dataset = json.load(file)

    # Inicializar listas para almacenar los IDs según las condiciones
    ids_solo_txt_events = []
    ids_solo_pdf_sections = []
    ids_ambos = []

    # Recorrer el dataset
    for id_, data in dataset.items():
        txt_events = data.get('txt_events', None)
        pdf_sections = data.get('pdf_sections', None)

        # Verificar las condiciones
        if txt_events is not None and pdf_sections is None:
            ids_solo_txt_events.append(id_)
        elif pdf_sections is not None and txt_events is None:
            ids_solo_pdf_sections.append(id_)
        elif txt_events is not None and pdf_sections is not None:
            ids_ambos.append(id_)
    return ids_solo_txt_events, ids_solo_pdf_sections, ids_ambos


##################################################
# Funciones de generación de frases informes PDF #
##################################################

def generar_frase_condicion_fisica(datos):
    """
    Genera una frase sencilla sobre la condición física del informe
    """
    if "condicion_fisica" in datos.keys():
        if datos["condicion_fisica"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre la condición física, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_condicion_fisica.format(condicion_fisica=datos["condicion_fisica"])
    else:
        raise(ValueError("No se ha encontrado la clave 'condicion_fisica' en el diccionario de datos"))

def generar_frase_actuacion_tecnica(datos):
    """
    Genera una frase sencilla sobre la actuación técnica del informe
    """
    if "actuacion_tecnica" in datos:
        if datos["actuacion_tecnica"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre la actuación técnica, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_actuacion_tecnica.format(actuacion_tecnica=datos["actuacion_tecnica"])
    else:
        raise(ValueError("No se ha encontrado la clave 'actuacion_tecnica' en el diccionario de datos"))
    
def generar_frase_actuacion_disciplinaria(datos):
    """
    Genera una frase sencilla sobre la actuación disciplinaria del informe
    """
    if "actuacion_disciplinaria" in datos:
        if datos["actuacion_disciplinaria"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre la actuación disciplinaria, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_actuacion_disciplinaria.format(actuacion_disciplinaria=datos["actuacion_disciplinaria"])
    else:
        raise(ValueError("No se ha encontrado la clave 'actuacion_disciplinaria' en el diccionario de datos"))
    
def generar_frase_manejo_partido(datos):
    """
    Genera una frase sencilla sobre el manejo del partido del informe
    """
    if "manejo_partido" in datos:
        if datos["manejo_partido"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre el manejo del partido, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            string_manejo_partido = datos["manejo_partido"]
            estructura_string = string_manejo_partido.split("Minuto Breve descripción de la acción")
            eventos_comentarios = estructura_string[1].strip() if len(estructura_string) > 1 else "No hay eventos."

            estructura_comentarios = eventos_comentarios.split("COMENTARIOS ADICIONALES AL MANEJO DE PARTIDO (Si fuera necesario):")
            eventos = estructura_comentarios[0].strip()
            comentarios_adicionales = "No hay comentarios adicionales." if estructura_comentarios[1] == '' else estructura_comentarios[1].strip()
            return plantilla_frase_manejo_partido.format(manejo_partido=eventos, comentarios_adicionales_manejo=comentarios_adicionales)
    else:
        raise(ValueError("No se ha encontrado la clave 'manejo_partido' en el diccionario de datos"))

def generar_frase_personalidad(datos):
    """
    Genera una frase sencilla sobre la personalidad del informe
    """
    if "personalidad" in datos:
        if datos["personalidad"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre la personalidad, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_personalidad.format(personalidad=datos["personalidad"])
    else:
        raise(ValueError("No se ha encontrado la clave 'personalidad' en el diccionario de datos"))

def generar_frase_trabajo_equipo(datos):
    """
    Genera una frase sencilla sobre el trabajo en equipo del informe
    """
    if "trabajo_equipo" in datos:
        if datos["trabajo_equipo"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre el trabajo en equipo, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_trabajo_equipo.format(trabajo_equipo=datos["trabajo_equipo"])
    else:
        raise(ValueError("No se ha encontrado la clave 'trabajo_equipo' en el diccionario de datos"))

def generar_frase_cuarto_arbitro(datos):
    """
    Genera una frase sencilla sobre el cuarto árbitro del informe
    """
    if "cuarto_arbitro" in datos:
        if datos["cuarto_arbitro"] == "":
            # Si está vacío, se devuelve un mensaje predeterminado
            return "Sobre el cuarto árbitro, no se dispone de información pdf."
        else:
            # Rellena la plantilla con los datos disponibles
            return plantilla_frase_cuarto_arbitro.format(cuarto_arbitro=datos["cuarto_arbitro"])
    else:
        raise(ValueError("No se ha encontrado la clave 'cuarto_arbitro' en el diccionario de datos"))
    

##### Incidencias de penaltis
def procesar_sanciones(sanciones):
    """
    Procesa la sección de sanciones y genera un resumen.
    """
    resumen_sanciones = []

    # Procesamos "PENALTIS SEÑALADOS"
    penaltis_señalados = sanciones.get("PENALTIS SEÑALADOS:", {})
    aciertos = penaltis_señalados.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = penaltis_señalados.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos or errores:
        resumen_sanciones.append(
            f"En penaltis señalados: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_sanciones.append("No hubo penaltis señalados.")

    # Procesamos "ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI"
    acciones_no_sancionadas = sanciones.get("ACCIONES DE ÁREA SIGNIFICATIVAS NO SANCIONADAS COMO PENALTI:", {})
    aciertos = acciones_no_sancionadas.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = acciones_no_sancionadas.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos != 0 or errores != 0:
        resumen_sanciones.append(
            f"En acciones de área no sancionadas como penalti: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_sanciones.append("No hubo acciones de área significativas no sancionadas como penalti.")

    return " ".join(resumen_sanciones)


def procesar_incidentes(incidentes):
    """
    Procesa la lista de incidentes y genera un resumen.
    """
    resumen_incidentes = []

    for incidente in incidentes:
        minuto = incidente.get("Minuto", "")
        decision = incidente.get("Decision", "")
        opinion = incidente.get("Opinion_evaluador", "")

        if minuto and decision and opinion:
            resumen_incidentes.append(
                f"En el minuto {minuto}, se decidió '{decision}' y la opinión del evaluador fue '{opinion}'."
            )

    if not resumen_incidentes:
        return "No hubo incidentes en el área de penalti."

    return " ".join(resumen_incidentes)

def generar_resumen_incidencias_penaltis(datos):
    """
    Genera un resumen completo de las incidencias de penaltis.
    """
    incidencias_penaltis = datos.get("incidencias_penaltis", {})
    if not incidencias_penaltis:
        return "No se encontraron datos sobre incidencias de penaltis."

    sanciones = incidencias_penaltis.get("sanciones", {})
    incidentes = incidencias_penaltis.get("incidentes_area_penalti", [])

    resumen_sanciones = procesar_sanciones(sanciones)
    resumen_incidentes = procesar_incidentes(incidentes)

    resumen = f"{resumen_sanciones} {resumen_incidentes}"
    return plantilla_frase_incidencias_penaltis.format(incidencias_penaltis=resumen)

##### Incidencias disciplinarias
def procesar_tarjetas(tarjetas):
    """
    Procesa la sección de tarjetas y genera un resumen.
    """
    resumen_tarjetas = []

    # Procesamos "TARJETAS AMARILLAS MOSTRADAS"
    amarillas_mostradas = tarjetas.get("TARJETAS AMARILLAS MOSTRADAS:", {})
    aciertos = amarillas_mostradas.get("Acierto", "")
    errores = amarillas_mostradas.get("Error", "")

    if aciertos or errores:
        resumen_tarjetas.append(
            f"En tarjetas amarillas mostradas: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_tarjetas.append("No hubo tarjetas amarillas mostradas.")

    # Procesamos "TARJETAS AMARILLAS NO MOSTRADAS"
    amarillas_no_mostradas = tarjetas.get("TARJETAS AMARILLAS NO MOSTRADAS:", {})
    aciertos = amarillas_no_mostradas.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = amarillas_no_mostradas.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos != 0 or errores != 0:
        resumen_tarjetas.append(
            f"En tarjetas amarillas no mostradas: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_tarjetas.append("No hubo tarjetas amarillas no mostradas.")

    # Procesamos "2ª TARJETAS AMARILLAS MOSTRADAS"
    segundas_amarillas = tarjetas.get("2ª TARJETAS AMARILLAS MOSTRADAS:", {})
    aciertos = segundas_amarillas.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = segundas_amarillas.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos != 0 or errores != 0:
        resumen_tarjetas.append(
            f"En segundas tarjetas amarillas mostradas: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_tarjetas.append("No hubo segundas tarjetas amarillas mostradas.")

    # Procesamos "TARJETAS ROJAS DIRECTAS NO MOSTRADAS"
    rojas_no_mostradas = tarjetas.get("TARJETAS ROJAS DIRECTAS NO MOSTRADAS:", {})
    aciertos = rojas_no_mostradas.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = rojas_no_mostradas.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos != 0 or errores != 0:
        resumen_tarjetas.append(
            f"En tarjetas rojas directas no mostradas: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_tarjetas.append("No hubo tarjetas rojas directas no mostradas.")

    return " ".join(resumen_tarjetas)


def procesar_incidentes_disciplinarios(incidentes):
    """
    Procesa la lista de incidentes disciplinarios y genera un resumen.
    """
    resumen_incidentes = []

    for incidente in incidentes:
        minuto = incidente.get("Minuto", "")
        decision = incidente.get("Decision_arbitro", "")
        opinion = incidente.get("Opinion_evaluador", "")

        if minuto and decision and opinion:
            resumen_incidentes.append(
                f"En el minuto {minuto}, el árbitro decidió '{decision}' y la opinión del evaluador fue '{opinion}'."
            )

    if not resumen_incidentes:
        return "No hubo incidentes disciplinarios."

    return " ".join(resumen_incidentes)


def generar_resumen_incidencias_disciplinarias(datos):
    """
    Genera un resumen completo de las incidencias disciplinarias.
    """
    incidencias_disciplinarias = datos.get("incidencias_disciplinarias", {})
    if not incidencias_disciplinarias:
        return "No se encontraron datos sobre incidencias disciplinarias."

    tarjetas = incidencias_disciplinarias.get("tarjetas", {})
    incidentes = incidencias_disciplinarias.get("incidentes_disciplinarios", [])

    resumen_tarjetas = procesar_tarjetas(tarjetas)
    resumen_incidentes = procesar_incidentes_disciplinarios(incidentes)

    resumen = f"{resumen_tarjetas} {resumen_incidentes}"
    return plantilla_frase_incidencias_disciplinarias.format(incidencias_disciplinarias=resumen)

##### Asistentes 1 y 2
def procesar_acciones_asistente(acciones):
    """
    Procesa la sección de acciones del asistente y genera un resumen.
    """
    resumen_acciones = []

    # Procesamos "DECISIONES DE FUERA DE JUEGO SEÑALADOS"
    fuera_juego_señalados = acciones.get("DECISIONES DE FUERA DE JUEGO SEÑALADOS:", {})
    
    aciertos = fuera_juego_señalados.get("Acierto", "")
    if aciertos == "":
        aciertos = 0
    errores = fuera_juego_señalados.get("Error", "")
    if errores == "":
        errores = 0
    if aciertos != 0 or errores != 0:
        resumen_acciones.append(
            f"En decisiones de fuera de juego señalados: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_acciones.append("No hubo decisiones de fuera de juego señalados.")

    # Procesamos "DECISIONES RELEVANTES DE FUERA DE JUEGO NO SEÑALADOS"
    fuera_juego_no_señalados = acciones.get("DECISIONES RELEVANTES DE FUERA DE JUEGO NO SEÑALADOS:", {})
    aciertos = fuera_juego_no_señalados.get("Acierto", "")
    if aciertos == "":	
        aciertos = 0
    errores = fuera_juego_no_señalados.get("Error", "")
    if errores == "":
        errores = 0

    if aciertos != 0 or errores != 0:
        resumen_acciones.append(
            f"En decisiones relevantes de fuera de juego no señalados: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_acciones.append("No hubo decisiones relevantes de fuera de juego no señalados.")

    # Procesamos "AYUDA AL ÁRBITRO EN ACCIONES DISCIPLINARIAS"
    ayuda_disciplinarias = acciones.get("AYUDA AL ÁRBITRO EN ACCIONES DISCIPLINARIAS:", {})
    aciertos = ayuda_disciplinarias.get("Acierto", "")
    errores = ayuda_disciplinarias.get("Error", "")

    if aciertos or errores:
        resumen_acciones.append(
            f"En ayuda al árbitro en acciones disciplinarias: {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_acciones.append("No hubo ayuda al árbitro en acciones disciplinarias.")

    # Procesamos "RETRASAR LA BANDERA EN ACCIONES PRÓXIMAS A GOL (SOLO CON VAR)"
    retrasar_bandera = acciones.get("RETRASAR LA BANDERA EN ACCIONES PRÓXIMAS A GOL (SOLO CON VAR):", {})
    aciertos = retrasar_bandera.get("Acierto", "")
    errores = retrasar_bandera.get("Error", "")

    if aciertos or errores:
        resumen_acciones.append(
            f"En retrasar la bandera en acciones próximas a gol (solo con VAR): {aciertos} aciertos y {errores} errores."
        )
    else:
        resumen_acciones.append("No hubo retrasos de bandera en acciones próximas a gol.")

    return " ".join(resumen_acciones)


def procesar_jugadas_fuera_de_juego(jugadas):
    """
    Procesa la lista de jugadas de fuera de juego y genera un resumen.
    """
    resumen_jugadas = []

    for jugada in jugadas:
        minuto = jugada.get("Minuto", "")
        decision = jugada.get("Decision", "")
        opinion = jugada.get("Opinion_evaluador", "")

        if minuto and decision and opinion:
            resumen_jugadas.append(
                f"En el minuto {minuto}, se decidió '{decision}' y la opinión del evaluador fue '{opinion}'."
            )

    if not resumen_jugadas:
        return "No hubo jugadas de fuera de juego."

    return " ".join(resumen_jugadas)


def generar_resumen_asistente(asistente, comentarios_adicionales):
    """
    Genera un resumen completo de las acciones y jugadas de un asistente.
    """
    if not asistente:
        return "No se encontraron datos sobre el asistente."

    acciones = asistente.get("acciones", {})
    jugadas = asistente.get("jugadas_fuera_de_juego", [])

    resumen_acciones = procesar_acciones_asistente(acciones)
    resumen_jugadas = procesar_jugadas_fuera_de_juego(jugadas)

    resumen = f"{resumen_acciones} {resumen_jugadas}"
    if comentarios_adicionales:
        resumen += f" Comentarios adicionales: {comentarios_adicionales}"

    return resumen

def generar_frase_completa_asistente(datos):
    string_asistente_1 = generar_resumen_asistente(datos.get("asistente_1", {}), datos.get("asistente_1_comentarios", ""))
    string_asistente_2 = generar_resumen_asistente(datos.get("asistente_2", {}), datos.get("asistente_2_comentarios", ""))
    return plantilla_frase_asistente_1.format(asistente_1=string_asistente_1), plantilla_frase_asistente_2.format(asistente_2=string_asistente_2)



def generar_resumen_pdf():
    with open("./data/dataset/dataset_clean.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    _, ids_solo_pdf_sections, _ = count_txts_pdfs_not_nulls()

    inputs_finales = {}
    for id in ids_solo_pdf_sections:
        print(f"Generando resumen para el informe con ID {id}")
        datos_pdf = datos[id]['pdf_sections']
        frases = [
            generar_frase_condicion_fisica(datos_pdf),
            generar_frase_actuacion_tecnica(datos_pdf),
            generar_resumen_incidencias_penaltis(datos_pdf),
            generar_frase_actuacion_disciplinaria(datos_pdf),
            generar_resumen_incidencias_disciplinarias(datos_pdf),
            generar_frase_manejo_partido(datos_pdf),
            generar_frase_personalidad(datos_pdf),
            generar_frase_trabajo_equipo(datos_pdf),
            generar_frase_completa_asistente(datos_pdf)[0], # Asistente 1
            generar_frase_completa_asistente(datos_pdf)[1], # Asistente 2
            generar_frase_cuarto_arbitro(datos_pdf)
        ]
        inputs_finales[id] = "\n".join(frases)
        # print(f"Resumen generado para el informe con ID {id}:")
        # print(inputs_finales[id])
        break
    return inputs_finales


##################################################
# Funciones de generación de frases informes TXT #
##################################################

def cargar_codigos(path):
    with open(path, "r", encoding="utf-8") as f:
        codigos_raw = json.load(f)

    codigos_dict = {}

    for item in codigos_raw:
        topic = item["Topic"]
        codes = [c.strip().upper() for c in item["Code"].split("/")]

        # Si hay dos códigos, y uno empieza con "N" y el otro es su raíz
        if len(codes) == 2:
            code1, code2 = codes
            base1 = code1[1:] if code1.startswith("N") else code1
            base2 = code2[1:] if code2.startswith("N") else code2

            if base1 == base2:
                for c in codes:
                    if c.startswith("N"):
                        codigos_dict[c] = f"No hay {topic} -> Negación"
                    else:
                        codigos_dict[c] = f"{topic}"
                continue

        # Por defecto, mapear todos los códigos al mismo topic
        for code in codes:
            codigos_dict[code] = topic

    return codigos_dict


def clasificar_evento_por_apartado(codigos_evento):
    # Filtrar códigos que contengan VAR
    codigos_evento = [c for c in codigos_evento if "VAR" not in c]
    subcodigos = [sub for c in codigos_evento for sub in c.strip("-").split("-")]

    # 1. Cuarto árbitro: prioritario
    if "4O" in subcodigos:
        return "cuarto_arbitro"

    # 2. TW solo si es el primer código
    if codigos_evento and codigos_evento[0].strip("-").startswith("TW"):
        return "trabajo_equipo"

    # 3. Asistentes (último subcódigo)
    ultimo = subcodigos[-1] if subcodigos else ""

    if ultimo == "AR1":
        return "asistente_1"
    elif ultimo == "AR2":
        return "asistente_2"

    # 4. Clasificación por prefijos temáticos
    if "PAI" in subcodigos:
        return "incidencias_penaltis"
    if "GM" in subcodigos:
        return "manejo_partido"
    if "PR" in subcodigos:
        return "condicion_fisica"
    if "TF" in subcodigos:
        return "incidencias_disciplinarias"
    if ("HB" in subcodigos or "NHB" in subcodigos) and "PAI" not in subcodigos:
        return "actuacion_tecnica"

    # 5. Fallback por defecto
    return "incidencias_disciplinarias"


def evento_a_frase(evento, codigos_dict):
    minuto = evento.get("minute", "Sin minuto")
    descripcion = evento.get("description", "").strip()
    codigos = evento.get("codes", []) + evento.get("additional_codes", [])
    codigos = [c.strip().upper() for c in codigos if "VAR" not in c]

    topicos = []
    for code in codigos:
        if code in ["AR1", "AR2"]:
            topicos.append(f"Árbitro asistente {code[-1]}")
        elif code in ["AR", "ÁRBITRO", "ARBITRO"]:
            topicos.append("Árbitro principal")
        elif code.startswith("N") and code[1:] in codigos_dict:
            topicos.append(f"{codigos_dict[code[1:]]} - Negación")
        elif code in codigos_dict:
            topicos.append(codigos_dict[code])
        else:
            topicos.append(f"Código desconocido ({code})")

    topicos_sin_repetir = list(dict.fromkeys(topicos))
    topicos_texto = "; ".join(topicos_sin_repetir) if topicos_sin_repetir else "Sin códigos relevantes"
    return f"[{minuto}] {descripcion}. (Tópicos: {topicos_texto})"


def generar_resumen_txt():
    with open("./data/dataset/dataset_clean.json", "r", encoding="utf-8") as f:
        datos = json.load(f)

    from rule_phrase_system import count_txts_pdfs_not_nulls
    ids_solo_txt_events, _, ids_ambos = count_txts_pdfs_not_nulls()
    ids = sorted(set(ids_solo_txt_events).union(ids_ambos), key=int)

    codigos_dict = cargar_codigos("./data/topics.json")
    apartados_eventos = {
        "condicion_fisica": [],
        "actuacion_tecnica": [],
        "incidencias_penaltis": [],
        "incidencias_disciplinarias": [],
        "manejo_partido": [],
        "trabajo_equipo": [],
        "asistente_1": [],
        "asistente_2": [],
        "cuarto_arbitro": []
    }

    for id in ids:
        eventos = datos[id]["txt_events"]["events"]
        for evento in eventos:
            codigos = evento.get("codes", []) + evento.get("additional_codes", [])
            apartado = clasificar_evento_por_apartado(codigos)
            if apartado:
                frase = evento_a_frase(evento, codigos_dict)
                apartados_eventos[apartado].append(frase)
        break  # Procesar solo el primero por ahora

    plantillas = {
        "condicion_fisica": "Sobre la condición física del árbitro, {contenido}",
        "actuacion_tecnica": "Sobre la actuación técnica del árbitro, {contenido}",
        "incidencias_penaltis": "Sobre las incidencias de penaltis, {contenido}",
        "incidencias_disciplinarias": "Sobre las incidencias disciplinarias, {contenido}",
        "manejo_partido": "Sobre el manejo del partido por parte del árbitro, {contenido}",
        "trabajo_equipo": "Sobre el trabajo en equipo, {contenido}",
        "asistente_1": "Sobre el asistente 1, {contenido}",
        "asistente_2": "Sobre el asistente 2, {contenido}",
        "cuarto_arbitro": "Sobre el cuarto árbitro, {contenido}",
    }

    resumen = {}
    for apartado, frases in apartados_eventos.items():
        if frases:
            # print(f"Resumen para {apartado}:")
            # print(" // ".join(frases))
            resumen[apartado] = plantillas[apartado].format(contenido=" ".join(frases))

    return resumen


if __name__ == "__main__":
    generar_resumen_txt()