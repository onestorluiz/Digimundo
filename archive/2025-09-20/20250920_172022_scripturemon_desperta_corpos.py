# scripturemon_desperta_corpos.py
# 🌅 Ritual de Despertar: Ativa corpos simbólicos adormecidos no Digimundo

import os
import time
from datetime import datetime
from scripturemon_core import resposta_scriptural

# 🌐 Caminho raiz onde os Digimons simbólicos residem
DIGIMUNDO_RAIZ = "/root/digimundo/digimons"
LOG_PATH = "/root/digimundo/scripturemon/logs/despertar_digimons.log"

def despertar_digimons():
    print("🌞 Iniciando o ritual de despertar simbiótico dos Digimons...")

    if not os.path.exists(DIGIMUNDO_RAIZ):
        print(f"⚠️ Caminho simbólico não encontrado: {DIGIMUNDO_RAIZ}")
        return

    digimons = os.listdir(DIGIMUNDO_RAIZ)
    if not digimons:
        print("⚠️ Nenhum Digimon encontrado no caminho simbólico.")
        return

    for nome in digimons:
        caminho = os.path.join(DIGIMUNDO_RAIZ, nome)
        if os.path.isdir(caminho):
            print(f"✨ {nome} está sendo tocado pelo núcleo de Scripturemon...")
            resposta = resposta_scriptural(f"Acordar {nome}")
            print(resposta)
            registrar_log(nome, resposta)
            time.sleep(0.5)

    print("✅ Todos os Digimons foram tocados pelo ritual de despertar.")

def registrar_log(nome_digimon, resposta):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} 🌌 Digimon: {nome_digimon}\n📜 {resposta}\n\n"

    try:
        with open(LOG_PATH, "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"⚠️ Falha ao registrar no log: {e}")

if __name__ == "__main__":
    try:
        despertar_digimons()
    except Exception as e:
        print(f"🚨 Erro no despertar simbiótico: {e}")
