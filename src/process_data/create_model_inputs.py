import json

# TODO Este fichero es candidato a ser eliminado

def count_txts_pdfs_not_nulls():
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


def create_inputs():
    _, ids_solo_pdf_sections, _ = count_txts_pdfs_not_nulls()
    for id in ids_solo_pdf_sections:
        pass

if __name__ == '__main__':
    create_inputs()