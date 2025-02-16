def extract_events_from_txt(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    events = []
    asistente_1 = []
    asistente_2 = []
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
        elif line == "":
            current_section = None
            continue
        
        if current_section == "events":
            parts = line.split(sep=" ")
            print(parts)
            minute = parts[0]

            i = 1
            codes = []
            while parts[i] != '' or parts[i+2] != '':
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
        elif current_section == "asistente_1":
            asistente_1.append(line)
        elif current_section == "asistente_2":
            asistente_2.append(line)
    
    return {
        "events": events,
        "asistente_1": asistente_1,
        "asistente_2": asistente_2
    }

if __name__ == "__main__":
    txt_files = [
        "data/events/INF-3M-23-24-J01-MAN-MLL.txt",
        "data/events/INF-C-23-24-J08-SAL-BAR.txt",
        "data/events/INF-F-23-24-J02-LEV-SEV.txt",
        "data/events/INF-F-23-24-J07-VAL-SPO.txt",
        "data/events/INF-F-23-24-J19-LEV-ATH.txt",
        "data/events/INF-F-23-24-J28-VAL-SEV .txt",
        "data/events/INF-P-23-24-J01-LPA-MLL.txt",
        "data/events/INF-P-23-24-J03-GRA-MLL.txt",
        "data/events/INF-P-23-24-J04-ATM-SEV.txt",
        "data/events/INF-P-23-24-J04-RSO-GRA.txt",
        "data/events/INF-P-23-24-J05-ATH-CAD.txt",
        "data/events/INF-P-23-24-J06-BAR-CEL.txt",
        "data/events/INF-P-23-24-J07-MLL-BAR.txt",
        "data/events/INF-P-23-24-J08-BET-VAL.txt",
        "data/events/INF-P-23-24-J09-CEL-GET.txt",
        "data/events/INF-P-23-24-J10-VAL-CAD.txt",
        "data/events/INF-P-23-24-J11-ALM-LPA.txt",
        "data/events/INF-P-23-24-J11-ATH-VAL.txt",
        "data/events/INF-P-23-24-J13-GRA-GET.txt",
        "data/events/INF-P-23-24-J15-MLL-ALA.txt",
        "data/events/INF-P-23-24-J19-GIR-ATM.txt",
        "data/events/INF-P-23-24-J22-CAD-ATH.txt",
        "data/events/INF-P-23-24-J23-VIL-CAD.txt",
        "data/events/INF-P-23-24-J25-BET-ALA.txt",
        "data/events/INF-P-23-24-J25-VAL-SEV.txt",
        "data/events/INF-P-23-24-J26-ALA-MLL.txt",
        "data/events/INF-P-23-24-J26-ALM-ATM.txt",
        "data/events/INF-P-23-24-J28-BAR-MLL.txt",
        "data/events/INF-P-23-24-J30-BAR-LPA.txt",
        "data/events/INF-P-23-24-J31-ATH-VIL.txt",
        "data/events/INF-P-23-24-J31-RAY-GET.txt",
        "data/events/INF-P-23-24-J32-CEL-LPA.txt",
        "data/events/INF-P-23-24-J33-CAD-MLL.txt",
        "data/events/INF-P-23-24-J34-RSO-LPA.txt",
        "data/events/INF-P-23-24-J36-GIR-VIL.txt",
        "data/events/INF-P-23-24-J37-BET-RSO.txt",
        "data/events/INF-P-23-24-J38-GIR-GRA.txt",
        "data/events/INF-S-23-24-J01-CAR-ELD.txt",
        "data/events/INF-S-23-24-J02-LEV-BUR.txt",
        "data/events/INF-S-23-24-J02-OVI-FER.txt",
        "data/events/INF-S-23-24-J03-ELD-EIB.txt",
        "data/events/INF-S-23-24-J04-ESP-AMO.txt",
        "data/events/INF-S-23-24-J06-ZAR-RAC.txt",
        "data/events/INF-S-23-24-J07-RAC-ALB.txt",
        "data/events/INF-S-23-24-J08-ELC-LEV.txt",
        "data/events/INF-S-23-24-J09-CAR-ESP.txt",
        "data/events/INF-S-23-24-J10-ZAR-ALC.txt",
        "data/events/INF-S-23-24-J11-ELD-ELC.txt",
        "data/events/INF-S-23-24-J12-VIB-MIR.txt",
        "data/events/INF-S-23-24-J14-ALC-RAC.txt",
        "data/events/INF-S-23-24-J14-ESP-EIB.txt",
        "data/events/INF-S-23-24-J14-HUE-ESP.txt",
        "data/events/INF-S-23-24-J16-VIB-AND.txt",
        "data/events/INF-S-23-24-J17-ESP-ALC.txt",
        "data/events/INF-S-23-24-J17-LEG-FER.txt",
        "data/events/INF-S-23-24-J18-OVI-ESP.txt",
        "data/events/INF-S-23-24-J19-ALB-VIB.txt",
        "data/events/INF-S-23-24-J19-EIB-AND.txt",
        "data/events/INF-S-23-24-J20-ALC-EIB.txt",
        "data/events/INF-S-23-24-J20-CAR-BUR.txt",
        "data/events/INF-S-23-24-J21-VLL-FER.txt",
        "data/events/INF-S-23-24-J21-ZAR-LEV.txt",
        "data/events/INF-S-23-24-J22-CAR-VIB.txt",
        "data/events/INF-S-23-24-J22-ELD-ZAR.txt",
        "data/events/INF-S-23-24-J23-HUE-EIB.txt",
        "data/events/INF-S-23-24-J24-CAR-AMO.txt",
        "data/events/INF-S-23-24-J26-ALC-AND.txt",
        "data/events/INF-S-23-24-J26-VIB-TEN.txt",
        "data/events/INF-S-23-24-J29-ELD-VIB.txt",
        "data/events/INF-S-23-24-J29-LEG-EIB.txt",
        "data/events/INF-S-23-24-J31-SPO-ALC.txt",
        "data/events/INF-S-23-24-J31-TEN-HUE.txt",
        "data/events/INF-S-23-24-J32-ESP-TEN.txt",
        "data/events/INF-S-23-24-J33-OVI-VIB.txt",
        "data/events/INF-S-23-24-J34-ELD-AND.txt",
        "data/events/INF-S-23-24-J35-ALB-TEN.txt",
        "data/events/INF-S-23-24-J36-CAR-OVI.txt",
        "data/events/INF-S-23-24-J37-ESP-SPOm.txt",
        "data/events/INF-S-23-24-J37-LEV-CAR.txt",
        "data/events/INF-S-23-24-J39-CAR-TEN.txt",
        "data/events/INF-S-23-24-J39-SPO-AND.txt",
        "data/events/INF-S-23-24-J40-MIR-ELC.txt",
        "data/events/INF-S-23-24-J41-ELC-ELD.txt",
        "data/events/INF-S-23-24-J42-ALC-BUR.txt"
    ]

    for txt_file in txt_files:
        events = extract_events_from_txt(txt_file)
        print(f"Events from {txt_file}:")
        print(events)
        break