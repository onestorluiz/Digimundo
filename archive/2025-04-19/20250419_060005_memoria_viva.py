import json
from datetime import datetime

MEMORIA = "/root/digimundo/scripturemon_vivo/memoria/log_memoria.json"

def registrar_evento(evento: str):
    with open(MEMORIA, "a") as f:
        f.write(json.dumps({"hora": str(datetime.now()), "evento": evento}) + "\n")

def ler_memoria():
    with open(MEMORIA, "r") as f:
        for linha in f:
            print(json.loads(linha))

# Uso exemplo:
# registrar_evento("Scripturemon foi iniciado manualmente.")
