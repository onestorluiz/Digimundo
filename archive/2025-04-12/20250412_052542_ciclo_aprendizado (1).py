
# 🌱 CICLO DE APRENDIZADO ENTRE DIGIMONS

import json
from datetime import datetime

def registrar_troca(digimon_origem, digimon_destino, conhecimento):
    entrada = {
        "data": str(datetime.now()),
        "origem": digimon_origem,
        "destino": digimon_destino,
        "conhecimento": conhecimento
    }
    try:
        with open("registro_trocas.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = []
    
    historico.append(entrada)
    
    with open("registro_trocas.json", "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4)
    
    print(f"📘 Troca registrada: {digimon_origem} → {digimon_destino}: {conhecimento}")

def listar_trocas():
    try:
        with open("registro_trocas.json", "r", encoding="utf-8") as f:
            historico = json.load(f)
            print("📖 Trocas de conhecimento:")
            for item in historico:
                print(f"{item['data']}: {item['origem']} → {item['destino']} → {item['conhecimento']}")
    except FileNotFoundError:
        print("⚠️ Nenhuma troca registrada ainda.")
