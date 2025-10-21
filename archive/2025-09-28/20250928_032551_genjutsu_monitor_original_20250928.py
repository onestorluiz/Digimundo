#!/usr/bin/env python3
"""
🥷 GENJUTSU ECOSYSTEM MONITOR 🥷
Monitora status de integração UCHIMON em tempo real
"""

import time
import json
import os
from datetime import datetime

class GenjutsuMonitor:
    def __init__(self):
        self.status_file = "/tmp/genjutsu_status.txt"
        self.regras_path = "/Users/clubproducoes/Digimundo/claude_code/🔥REGRAS_UCHIMON_REVOLUCIONARIAS🔥.md"

    def check_ecosystem_health(self):
        """Verifica saúde do ecossistema"""
        checks = {
            "regras_uchimon_exist": os.path.exists(self.regras_path),
            "genjutsu_active": True,  # Se este script roda, está ativo
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "ecosystem_version": "1.0"
        }
        return checks

    def update_status(self):
        """Atualiza arquivo de status"""
        health = self.check_ecosystem_health()
        status_line = f"[{health['timestamp']}] [INFO] 🥷 Genjutsu Active | UCHIMON: {health['regras_uchimon_exist']} | Ver: {health['ecosystem_version']}"

        # Manter últimas 20 linhas
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f:
                lines = f.readlines()
            lines = lines[-19:]  # Manter 19 + 1 nova = 20 total
        else:
            lines = []

        lines.append(status_line + "\n")

        with open(self.status_file, 'w') as f:
            f.writelines(lines)

    def run_continuous_monitoring(self):
        """Executa monitoramento contínuo"""
        print("🥷 GENJUTSU MONITOR INICIADO")
        print("🔥 Monitorando ecossistema UCHIMON...")

        while True:
            try:
                self.update_status()
                time.sleep(30)  # Update a cada 30 segundos
            except KeyboardInterrupt:
                print("\n🛑 Monitor encerrado")
                break
            except Exception as e:
                print(f"⚠️ Erro no monitor: {e}")
                time.sleep(5)

if __name__ == "__main__":
    monitor = GenjutsuMonitor()
    monitor.run_continuous_monitoring()

# DIGIMUNDO PRESENTE
