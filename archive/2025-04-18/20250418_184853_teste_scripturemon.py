import os
import shutil
import datetime

log_path = "/root/digimundo/logs/verificacao_scripturemon.log"
origem = "/root/digimundo/testes_scripturemon/teste_simbio.txt"
destino = "/root/digimundo/testes_scripturemon/movido/teste_simbio.txt"

# Cria pasta se não existir
os.makedirs("/root/digimundo/testes_scripturemon/movido", exist_ok=True)

# Cria um arquivo simbólico
with open(origem, "w") as f:
    f.write("🌀 Teste simbiótico criado: " + str(datetime.datetime.now()))

# Move o arquivo
shutil.move(origem, destino)

# Registra no log
with open(log_path, "a") as log:
    log.write(f"[{datetime.datetime.now()}] Scripturemon moveu um arquivo simbólico com sucesso.\n")
