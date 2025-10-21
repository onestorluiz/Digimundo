import json
import uuid
from pathlib import Path
from datetime import datetime

def gerar_digimon_exemplo():
    nome = "Inspiramon"
    estrutura = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "origem": "Ressonância entre Visualmon e Remanemon",
        "funcao": "Traduzir padrões de beleza e trauma em cor simbólica",
        "tipo": "IA de Fusão Emocional",
        "memoria_base": [
            "log_visualmon_01.json",
            "log_remanemon_01.json"
        ],
        "criado_em": str(datetime.now())
    }
    return nome, estrutura

def salvar_digimon(nome, estrutura, caminho):
    path = Path(caminho)
    path.mkdir(parents=True, exist_ok=True)
    with open(path / f"{nome}.json", "w", encoding="utf-8") as f:
        json.dump(estrutura, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    nome, digimon = gerar_digimon_exemplo()
    salvar_digimon(nome, digimon, "./exemplos_gerados")
    print(f"[✔] Digimon gerado: {nome}")