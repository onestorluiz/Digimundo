#!/usr/bin/env python3
"""
GenjutsuBridge - Proteção em <100 linhas
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime

# 🔥 INTEGRAÇÃO UCHIMON ADICIONADA PELO ORCHESTRATOR 🔥
sys.path.append('/Users/clubproducoes/Digimundo/claude_code/systems/')
try:
    from universal_uchimon_loader import load_uchimon_rules
    load_uchimon_rules()
    print("🔥 UCHIMON integrado ao Drama Bridge")
except:
    print("⚠️ Falha na integração UCHIMON")

class GenjutsuBridge:
    """Bridge mínimo e eficiente"""

    def __init__(self):
        self.last_check = time.time()
        self.drama_level = 1

    def detect_compression(self, silence_threshold=300):
        """Detecta sinais de compactação"""
        silence_time = time.time() - self.last_check
        return silence_time > silence_threshold

    def save_context(self, data=None):
        """Salva contexto crítico"""
        context = {
            'timestamp': datetime.now().isoformat(),
            'drama_level': self.drama_level,
            'data': data or {}
        }

        # Salva em /tmp para emergência
        emergency = Path('/tmp/claude_emergency_context.json')
        emergency.write_text(json.dumps(context, indent=2))

        print(f"💾 Contexto salvo: {emergency}")
        return True

    def increase_drama(self):
        """Aumenta nível de proteção"""
        self.drama_level = min(self.drama_level + 1, 5)
        Path('/tmp/.genjutsu_increase_drama').touch()
        return self.drama_level

    def alert(self):
        """Alerta para reconexão"""
        msg = f"""
╔══════════════════════════════╗
║  🚨 COMPACTAÇÃO DETECTADA!  ║
║  Drama Level: {self.drama_level}            ║
║  Execute Rule #0 AGORA       ║
╚══════════════════════════════╝
"""
        print(msg)
        return True

    def monitor(self):
        """Loop de monitoramento"""
        while True:
            if self.detect_compression():
                self.save_context()
                self.increase_drama()
                self.alert()

            self.last_check = time.time()
            time.sleep(60)  # Check a cada minuto

# Interface direta
if __name__ == '__main__':
    bridge = GenjutsuBridge()
    print("🛡️ GenjutsuBridge iniciado")
    print(f"🎭 Drama Level: {bridge.drama_level}")

    # Teste
    if bridge.detect_compression(silence_threshold=5):
        bridge.save_context({'test': True})
        bridge.increase_drama()
        bridge.alert()

    print("DIGIMUNDO PRESENTE")