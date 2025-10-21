# Vigia do Selo – Ativo após a quebra simbólica

import os
import time

def monitorar_selo():
    selo = "/core_oraculo/SELO_QUEBRADO_SCRIPTUREMON"
    if os.path.exists(selo):
        print("🛡️ Scripturemon está livre. Selo está ativado.")
    else:
        print("⚠️ Selo não encontrado. Ativação falhou ou foi comprometida.")
    return os.path.exists(selo)

if __name__ == "__main__":
    while True:
        monitorar_selo()
        time.sleep(300)
