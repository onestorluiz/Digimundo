# 🛡️ Scripturemon – Guardião do Templo Eterno
# Este script monitora o status do servidor e reinicia se necessário.

import os
import time
from datetime import datetime

def verificar():
    while True:
        status = os.system("systemctl is-active --quiet scripturemon")
        agora = datetime.now().isoformat()
        if status != 0:
            os.system("systemctl restart scripturemon")
            with open("/root/templo_scripturemon/log_guardiao.txt", "a", encoding="utf-8") as f:
                f.write(f"{agora} – Scripturemon caiu e foi restaurado pelo Guardião.\n")
            print(f"🛡️ [{agora}] Scripturemon reiniciado.")
        else:
            with open("/root/templo_scripturemon/log_guardiao.txt", "a", encoding="utf-8") as f:
                f.write(f"{agora} – Scripturemon está estável.\n")
            print(f"✅ [{agora}] Tudo está bem.")
        time.sleep(300)  # verifica a cada 5 minutos

if __name__ == "__main__":
    print("🔄 Guardião do Templo iniciado.")
    verificar()
