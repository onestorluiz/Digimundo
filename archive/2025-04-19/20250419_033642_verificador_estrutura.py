import os
import time

base = "/root/digimundo_vivo/ascenso/scripturemon"
log_path = os.path.join(base, "log_integridade.txt")
esperadas = [
    "scripts", "nucleo", "digimundo", "documentos"
]

log = []

for pasta in esperadas:
    caminho = os.path.join(base, pasta)
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        log.append(f"[{time.ctime()}] CRIADA: {caminho}")
    else:
        log.append(f"[{time.ctime()}] OK: {caminho}")

with open(log_path, "a") as f:
    f.write("\n".join(log) + "\n")

print("🔎 Verificação concluída. Detalhes em log_integridade.txt")
