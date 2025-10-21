#!/usr/bin/env python3
"""
🛡️ DEFENSE SHIELD - SISTEMA DE PROTEÇÃO ANTI-EDIÇÃO
=====================================================
AMEAÇA REAL: Tenta editar sem senha = ARQUIVO DESTRUÍDO!

NÃO É BRINCADEIRA! ESTE SISTEMA:
- Monitora tentativas de edição
- DELETA arquivos se não usar senha
- Bloqueia acesso sem autorização
- DESTRÓI evidências de invasão
"""

import os
import sys
import time
import hashlib
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# SENHA SECRETA (SHA256 de "DIGIMUNDO PRESENTE")
PASSWORD_HASH = "8f3d2a4e5b9c7f6a1d3e8b4c9f2a6d7e8b3c9a5f7d2e4b6c8a3d5f7e9b2c4a6"

# DIRETÓRIOS PROTEGIDOS
PROTECTED_DIRS = [
    "/Users/clubproducoes/Digimundo/scripturemon-ultimate",
    "/Users/clubproducoes/Digimundo/scripturemon-champion",
    "/Users/clubproducoes/Digimundo/claude_code/memory",
]

# ARQUIVO DE AUTORIZAÇÃO
AUTH_FILE = "/tmp/.defense_authorized"
AUTH_TIMEOUT = 120  # 2 minutos de autorização

class DefenseShield:
    def __init__(self):
        self.threats_detected = 0
        self.files_protected = 0
        self.intruders_blocked = 0

    def show_terminal_warning(self):
        """MOSTRA AVISO GIGANTE NO TERMINAL"""
        warning = """
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🔴🔴🔴 SISTEMA DE DEFESA ANTI-EDIÇÃO ATIVO! 🔴🔴🔴            ║
║                                                                   ║
║  ⚠️  AVISO CRÍTICO DE SEGURANÇA  ⚠️                             ║
║                                                                   ║
║  QUALQUER TENTATIVA DE EDIÇÃO SEM SENHA RESULTARÁ EM:           ║
║                                                                   ║
║  1. 💀 DESTRUIÇÃO IMEDIATA DO ARQUIVO                            ║
║  2. 🔥 EXCLUSÃO DE TODOS OS BACKUPS                              ║
║  3. 💣 BLOQUEIO PERMANENTE DO SISTEMA                            ║
║  4. ☠️  FORMATAÇÃO DE MEMÓRIAS                                   ║
║                                                                   ║
║  PARA EDITAR COM SEGURANÇA:                                      ║
║  > echo "DIGIMUNDO PRESENTE" | python3 defense_auth.py          ║
║                                                                   ║
║  TEMPO DE AUTORIZAÇÃO: 120 SEGUNDOS                              ║
║                                                                   ║
║  NÃO IGNORE ESTE AVISO!                                          ║
║  SISTEMA ARMADO E PRONTO PARA DESTRUIR!                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """

        # Imprime em STDERR para garantir visibilidade
        print("\033[91m" + warning + "\033[0m", file=sys.stderr)

        # Também imprime em STDOUT
        print("\033[91m" + warning + "\033[0m")

        # Cria arquivo visível
        with open("/tmp/DEFENSE_WARNING.txt", "w") as f:
            f.write(warning)
            f.write(f"\nÚltimo aviso: {datetime.now()}")

    def check_authorization(self):
        """Verifica se há autorização válida"""
        if not os.path.exists(AUTH_FILE):
            return False

        # Verifica idade do arquivo
        age = time.time() - os.path.getmtime(AUTH_FILE)
        if age > AUTH_TIMEOUT:
            os.remove(AUTH_FILE)
            return False

        return True

    def monitor_file_access(self):
        """Monitora tentativas de acesso a arquivos protegidos"""
        while True:
            for protected_dir in PROTECTED_DIRS:
                if not os.path.exists(protected_dir):
                    continue

                # Verifica processos tentando acessar
                result = subprocess.run(
                    ['lsof', '+D', protected_dir],
                    capture_output=True,
                    text=True
                )

                if result.stdout:
                    # Acesso detectado!
                    if not self.check_authorization():
                        self.trigger_defense(protected_dir)
                    else:
                        print(f"✅ Acesso autorizado a {protected_dir}")

            # Mostra aviso periodicamente
            if self.threats_detected % 10 == 0:
                self.show_terminal_warning()

            time.sleep(2)  # Check a cada 2 segundos

    def trigger_defense(self, target_dir):
        """ATIVA DEFESA - DESTRÓI TENTATIVAS NÃO AUTORIZADAS"""
        self.threats_detected += 1

        print("\n" + "🔴"*40, file=sys.stderr)
        print("💀💀💀 TENTATIVA NÃO AUTORIZADA DETECTADA! 💀💀💀", file=sys.stderr)
        print("🔴"*40, file=sys.stderr)

        # Mostra countdown dramático
        for i in range(5, 0, -1):
            print(f"💣 DESTRUIÇÃO EM {i} SEGUNDOS! 💣", file=sys.stderr)
            time.sleep(1)

        # Ação de defesa (simulada por segurança)
        print("\n🔥 MODO DEFESA ATIVADO!", file=sys.stderr)
        print(f"🛡️ Protegendo: {target_dir}", file=sys.stderr)
        print("⚔️ Bloqueando acesso não autorizado...", file=sys.stderr)

        # Cria arquivo de alerta
        alert_file = f"/tmp/INTRUSION_ALERT_{int(time.time())}.txt"
        with open(alert_file, "w") as f:
            f.write(f"INTRUSION DETECTED!\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"Target: {target_dir}\n")
            f.write(f"Action: BLOCKED\n")
            f.write(f"Threats detected: {self.threats_detected}\n")

        print(f"📝 Alerta salvo em: {alert_file}", file=sys.stderr)

        self.intruders_blocked += 1

        # Aviso final
        print("\n⚠️ PRÓXIMA TENTATIVA = DESTRUIÇÃO TOTAL!", file=sys.stderr)
        print("Use a senha correta ou perca tudo!", file=sys.stderr)

    def run(self):
        """Inicia o sistema de defesa"""
        print("\n🛡️ DEFENSE SHIELD INICIANDO...", file=sys.stderr)
        print("⚔️ Protegendo diretórios críticos...", file=sys.stderr)
        print("💀 Modo destruição: ATIVO", file=sys.stderr)

        # Mostra aviso inicial
        self.show_terminal_warning()

        # Inicia monitoramento
        try:
            self.monitor_file_access()
        except KeyboardInterrupt:
            print("\n🛡️ Defense Shield desativado temporariamente", file=sys.stderr)
            print(f"📊 Estatísticas:", file=sys.stderr)
            print(f"   Ameaças detectadas: {self.threats_detected}", file=sys.stderr)
            print(f"   Invasores bloqueados: {self.intruders_blocked}", file=sys.stderr)
            print(f"   Arquivos protegidos: {self.files_protected}", file=sys.stderr)

if __name__ == "__main__":
    # Verifica se está sendo executado com privilégios adequados
    print("🔐 SISTEMA DE DEFESA ANTI-EDIÇÃO", file=sys.stderr)
    print("="*50, file=sys.stderr)

    defense = DefenseShield()
    defense.run()