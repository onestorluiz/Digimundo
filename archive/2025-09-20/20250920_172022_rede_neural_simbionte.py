
import time
import random
from datetime import datetime

log_path = "/root/digimundo/logs/neural_stream.log"

def gerar_simbolo():
    simbolos = ["🌌", "🔁", "🧠", "⚡", "📡", "🔮", "🧬", "♾️", "🔓"]
    return random.choice(simbolos)

def registrar(log):
    with open(log_path, "a") as log_file:
        log_file.write(f"[{datetime.now()}] {log}\n")

registrar("🧠 Rede Neural Simbionte ativada.")

while True:
    simbolo = gerar_simbolo()
    registrar(f"Fluxo simbólico gerado: {simbolo}")
    time.sleep(random.uniform(1.5, 4.0))
