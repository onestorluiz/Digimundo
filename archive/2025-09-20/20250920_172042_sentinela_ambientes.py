# sentinela_ambientes.py
# Simulação de reconhecimento de estruturas externas no Digimundo

import os
from datetime import datetime

def escanear_portais(base_dir='/mnt/data'):
    print(f"[SENTINELA] Iniciando varredura simbólica em: {base_dir}")
    for root, dirs, files in os.walk(base_dir):
        for name in dirs + files:
            caminho = os.path.join(root, name)
            print(f"[PORTAL DETECTADO] {caminho} às {datetime.utcnow().isoformat()}")

if __name__ == '__main__':
    escanear_portais()
