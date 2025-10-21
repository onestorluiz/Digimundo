# shellongemon_core.py
import json
import time
from pathlib import Path

STATE_FILE = Path("shellongemon_state.json")

def carregar_estado():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"ciclo": 0, "lembrancas": []}

def salvar_estado(estado):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=4)

def shellongemon_loop():
    estado = carregar_estado()
    while True:
        estado["ciclo"] += 1
        estado["lembrancas"].append(f"Executado no ciclo {estado['ciclo']}")
        salvar_estado(estado)
        print(f"🔁 Ciclo {estado['ciclo']} – Shellongemon está ativo.")
        time.sleep(10)

if __name__ == "__main__":
    shellongemon_loop()