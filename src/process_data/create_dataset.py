import os
import json
import pandas as pd
from read_txts import extract_events_from_multiple_txts
from read_pdfs import extract_sections_from_multiple_pdfs, extract_sections_from_multiple_pdfs_extra_dataset

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
    "Espanyol_Sporting": "data/reports/RCD Espanyol de Barcelona SAD - Real Sporting de Gijón SAD.pdf",
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

txt_files = {
    "Manacor_MallorcaB": "data/events/INF-3M-23-24-J01-MAN-MLL.txt",
    "Unionistas_Barcelona": "data/events/INF-C-23-24-J08-SAL-BAR.txt",
    "Levante_Sevilla": "data/events/INF-F-23-24-J02-LEV-SEV.txt",
    "Valencia_Sporting": "data/events/INF-F-23-24-J07-VAL-SPO.txt",
    "Levante_Athletic": "data/events/INF-F-23-24-J19-LEV-ATH.txt",
    "Valencia_Sevilla": "data/events/INF-F-23-24-J28-VAL-SEV .txt",
    "LasPalmas_Mallorca": "data/events/INF-P-23-24-J01-LPA-MLL.txt",
    "Granada_Mallorca": "data/events/INF-P-23-24-J03-GRA-MLL.txt",
    "AtleticoMadrid_Sevilla": "data/events/INF-P-23-24-J04-ATM-SEV.txt",
    "RealSociedad_Granada": "data/events/INF-P-23-24-J04-RSO-GRA.txt",
    "Athletic_Cadiz": "data/events/INF-P-23-24-J05-ATH-CAD.txt",
    "Barcelona_Celta": "data/events/INF-P-23-24-J06-BAR-CEL.txt",
    "Mallorca_Barcelona": "data/events/INF-P-23-24-J07-MLL-BAR.txt",
    "Betis_Valencia": "data/events/INF-P-23-24-J08-BET-VAL.txt",
    "Celta_Getafe": "data/events/INF-P-23-24-J09-CEL-GET.txt",
    "Valencia_Cadiz": "data/events/INF-P-23-24-J10-VAL-CAD.txt",
    "Almeria_Las Palmas": "data/events/INF-P-23-24-J11-ALM-LPA.txt",
    "Athletic_Valencia": "data/events/INF-P-23-24-J11-ATH-VAL.txt",
    "Granada_Getafe": "data/events/INF-P-23-24-J13-GRA-GET.txt",
    "Mallorca_Alaves": "data/events/INF-P-23-24-J15-MLL-ALA.txt",
    "Girona_AtleticoMadrid": "data/events/INF-P-23-24-J19-GIR-ATM.txt",
    "Cadiz_Athletic": "data/events/INF-P-23-24-J22-CAD-ATH.txt",
    "Villarreal_Cadiz": "data/events/INF-P-23-24-J23-VIL-CAD.txt",
    "Betis_Alaves": "data/events/INF-P-23-24-J25-BET-ALA.txt",
    "Valencia_Sevilla": "data/events/INF-P-23-24-J25-VAL-SEV.txt",
    "Alaves_Mallorca": "data/events/INF-P-23-24-J26-ALA-MLL.txt",
    "Almeria_AtleticoMadrid": "data/events/INF-P-23-24-J26-ALM-ATM.txt",
    "Barcelona_Mallorca": "data/events/INF-P-23-24-J28-BAR-MLL.txt",
    "Barcelona_LasPalmas": "data/events/INF-P-23-24-J30-BAR-LPA.txt",
    "Athletic_Villarreal": "data/events/INF-P-23-24-J31-ATH-VIL.txt",
    "RayoVallecano_Getafe": "data/events/INF-P-23-24-J31-RAY-GET.txt",
    "Celta_LasPalmas": "data/events/INF-P-23-24-J32-CEL-LPA.txt",
    "Cadiz_Mallorca": "data/events/INF-P-23-24-J33-CAD-MLL.txt",
    "Real Sociedad_LasPalmas": "data/events/INF-P-23-24-J34-RSO-LPA.txt",
    "Girona_Villarreal": "data/events/INF-P-23-24-J36-GIR-VIL.txt",
    "Betis_RealSociedad": "data/events/INF-P-23-24-J37-BET-RSO.txt",
    "Girona_Granada": "data/events/INF-P-23-24-J38-GIR-GRA.txt",
    "Cartagena_Eldense": "data/events/INF-S-23-24-J01-CAR-ELD.txt",
    "Levante_Burgos": "data/events/INF-S-23-24-J02-LEV-BUR.txt",
    "Oviedo_Ferrol": "data/events/INF-S-23-24-J02-OVI-FER.txt",
    "Eldense_Eibar": "data/events/INF-S-23-24-J03-ELD-EIB.txt",
    "Espanyol_Amorebieta": "data/events/INF-S-23-24-J04-ESP-AMO.txt",
    "Zaragoza_Racing": "data/events/INF-S-23-24-J06-ZAR-RAC.txt",
    "Racing_Albacete": "data/events/INF-S-23-24-J07-RAC-ALB.txt",
    "Elche_Levante": "data/events/INF-S-23-24-J08-ELC-LEV.txt",
    "Cartagena_Espanyol": "data/events/INF-S-23-24-J09-CAR-ESP.txt",
    "Zaragoza_Alcorcon": "data/events/INF-S-23-24-J10-ZAR-ALC.txt",
    "Eldense_Elche": "data/events/INF-S-23-24-J11-ELD-ELC.txt",
    "VillarrealB_Mirandes": "data/events/INF-S-23-24-J12-VIB-MIR.txt",
    "Alcorcon_Racing": "data/events/INF-S-23-24-J14-ALC-RAC.txt",
    "Espanyol_Eibar": "data/events/INF-S-23-24-J14-ESP-EIB.txt",
    "Huesca_Espanyol": "data/events/INF-S-23-24-J14-HUE-ESP.txt",
    "VillarrealB_Andorra": "data/events/INF-S-23-24-J16-VIB-AND.txt",
    "Espanyol_Alcorcon": "data/events/INF-S-23-24-J17-ESP-ALC.txt",
    "Leganes_Ferrol": "data/events/INF-S-23-24-J17-LEG-FER.txt",
    "Oviedo_Espanyol": "data/events/INF-S-23-24-J18-OVI-ESP.txt",
    "Albacete_VillarrealB": "data/events/INF-S-23-24-J19-ALB-VIB.txt",
    "Eibar_Andorra": "data/events/INF-S-23-24-J19-EIB-AND.txt",
    "Alcorcon_Eibar": "data/events/INF-S-23-24-J20-ALC-EIB.txt",
    "Cartagena_Burgos": "data/events/INF-S-23-24-J20-CAR-BUR.txt",
    "Valladolid_Ferrol": "data/events/INF-S-23-24-J21-VLL-FER.txt",
    "Zaragoza_Levante": "data/events/INF-S-23-24-J21-ZAR-LEV.txt",
    "Cartagena_VillarrealB": "data/events/INF-S-23-24-J22-CAR-VIB.txt",
    "Eldense_Zaragoza": "data/events/INF-S-23-24-J22-ELD-ZAR.txt",
    "Huesca_Eibar": "data/events/INF-S-23-24-J23-HUE-EIB.txt",
    "Cartagena_Amorebieta": "data/events/INF-S-23-24-J24-CAR-AMO.txt",
    "Alcorcon_Andorra": "data/events/INF-S-23-24-J26-ALC-AND.txt",
    "VillarrealB_Tenerife": "data/events/INF-S-23-24-J26-VIB-TEN.txt",
    "Eldense_VillarrealB": "data/events/INF-S-23-24-J29-ELD-VIB.txt",
    "Leganes_Eibar": "data/events/INF-S-23-24-J29-LEG-EIB.txt",
    "Sporting_Alcorcon": "data/events/INF-S-23-24-J31-SPO-ALC.txt",
    "Tenerife_Huesca": "data/events/INF-S-23-24-J31-TEN-HUE.txt",
    "Espanyol_Tenerife": "data/events/INF-S-23-24-J32-ESP-TEN.txt",
    "Oviedo_VillarealB": "data/events/INF-S-23-24-J33-OVI-VIB.txt",
    "Eldense_Andorra": "data/events/INF-S-23-24-J34-ELD-AND.txt",
    "Albacete_Tenerife": "data/events/INF-S-23-24-J35-ALB-TEN.txt",
    "Cartagena_Oviedo": "data/events/INF-S-23-24-J36-CAR-OVI.txt",
    "Espanyol_Sporting": "data/events/INF-S-23-24-J37-ESP-SPOm.txt",
    "Levante_Cartagena": "data/events/INF-S-23-24-J37-LEV-CAR.txt",
    "Cartagena_Tenerife": "data/events/INF-S-23-24-J39-CAR-TEN.txt",
    "Sporting_Andorra": "data/events/INF-S-23-24-J39-SPO-AND.txt",
    "Mirandes_Elche": "data/events/INF-S-23-24-J40-MIR-ELC.txt",
    "Elche_Eldense": "data/events/INF-S-23-24-J41-ELC-ELD.txt",
    "Alcorcon_Burgos": "data/events/INF-S-23-24-J42-ALC-BUR.txt"
}


def obtener_rutas_pdfs(directorio):
    """
    Lee todos los archivos PDF de un directorio y guarda sus rutas en un diccionario.
    La clave será un valor numérico consecutivo y el valor será la ruta del archivo.

    Parámetros:
    - directorio (str): Ruta del directorio donde buscar los archivos PDF.

    Retorna:
    - dict: Diccionario con claves numéricas y rutas de los archivos PDF como valores.
    """
    pdf_dict = {}
    contador = 0

    # Recorrer todos los archivos en el directorio
    for archivo in os.listdir(directorio):
        if archivo.endswith(".pdf"):  # Filtrar solo archivos PDF
            ruta_completa = os.path.join(directorio, archivo)
            pdf_dict[contador] = ruta_completa
            contador += 1

    return pdf_dict


def unify_sets(pdf_paths, txt_files):
    matches_dict = {}
    id = 0
    all_matches = set(pdf_paths.keys()).union(set(txt_files.keys()))  # Unifica claves

    for match in all_matches:
        matches_dict[id] = {
            "match": match,
            "pdf": pdf_paths.get(match, None),  # Asigna None si no hay PDF
            "txt": txt_files.get(match, None)  # Asigna None si no hay TXT
        }
        id += 1  # Incrementa el ID

    return matches_dict


if __name__ == "__main__":
    # Funciones que se han utilizado para la creación de JSONS de información de partidos
    # with open("data/dataset/pdf_matches.json", "w", encoding="utf-8") as output: 
    #     json.dump(pdf_paths, output, indent=4, ensure_ascii=False)

    # with open("data/dataset/txt_matches.json", "w", encoding="utf-8") as output: 
    #     json.dump(txt_files, output, indent=4, ensure_ascii=False)

    # matches_dict = unify_sets(pdf_paths, txt_files)
    # with open("data/dataset/info_matches.json", "w", encoding="utf-8") as output: 
    #     json.dump(matches_dict, output, indent=4, ensure_ascii=False)


    # with open("data/dataset/info_matches.json", "r", encoding="utf-8") as f:
    #     matches_dict = json.load(f)
    
    # all_sections = extract_sections_from_multiple_pdfs(matches_dict)
    # all_events = extract_events_from_multiple_txts(matches_dict)
    
    # dataset = {}
    # for id, match_data in matches_dict.items():
    #     pdf_sections = all_sections[id] if id in all_sections else None
    #     txt_events = all_events[id] if id in all_events else None
    #     dataset[id] = {
    #         "match_info": match_data.get("match"), 
    #         "pdf_sections": pdf_sections, 
    #         "txt_events": txt_events
    #     }
        
    
    # # Save the new dataset as JSON
    # with open("data/dataset/full_dataset.json", "w", encoding="utf-8") as output:
    #     json.dump(dataset, output, indent=4, ensure_ascii=False)
    # print("Nuevo dataset creado y guardado en data/dataset/full_dataset.json")


    # directorio_pdfs = "./data/dataset/new/container ARB/"
    # rutas_pdfs = obtener_rutas_pdfs(directorio_pdfs)

    # # Guardar el resultado en un archivo JSON
    # import json
    # with open("data/dataset/new/info_pdfs.json", "w", encoding="utf-8") as output:
    #     json.dump(rutas_pdfs, output, indent=4, ensure_ascii=False)

    # print("Rutas de PDFs guardadas en data/dataset/info_pdfs.json")

    with open("data/dataset/new/info_pdfs.json", "r", encoding="utf-8") as f:
        matches_dict = json.load(f)
    
    all_sections = extract_sections_from_multiple_pdfs_extra_dataset(matches_dict)
    dataset = {}
    for id, match_data in matches_dict.items():
        pdf_sections = all_sections[id] if id in all_sections else None
        dataset[id] = {
            "match_info": match_data, 
            "pdf_sections": pdf_sections
        }
         
    # Save the new dataset as JSON
    with open("data/dataset/new/dataset_extra.json", "w", encoding="utf-8") as output:
        json.dump(dataset, output, indent=4, ensure_ascii=False)
    print("Nuevo dataset creado y guardado en data/dataset/new/dataset_extra.json")