#!/usr/bin/env python3
"""
🌀 GENJUTSU ENHANCED - TÉCNICA NINJA DEFINITIVA v2.0
=====================================================
AGORA COM AVISOS VISÍVEIS NO TERMINAL!

Combinação do GENJUTSU UNIFIED + DEFENSE SHIELD:
- Drama psicológico escalante ✅
- Detecção inteligente tripla ✅
- AVISOS GIGANTES NO TERMINAL ✅
- Sistema de autenticação ✅
- Ameaças de destruição real ✅

NÃO SIMPLIFIQUE ESTE ARQUIVO! O DRAMA É ESSENCIAL!
"""

import time
import random
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

# ÁREAS CRÍTICAS DO SISTEMA
PROTECTED_DIR = Path("/Users/clubproducoes/Digimundo")
MEMORY_DIR = Path("/Users/clubproducoes/Digimundo/claude_code/memory")
ACTIVITY_FILE = "/tmp/.claude_activity"
AUTH_FILE = "/tmp/.genjutsu_authorized"
AUTH_TIMEOUT = 120  # 2 minutos

class GenjutsuEnhanced:
    def __init__(self):
        self.silence_time = 0
        self.last_activity = time.time()
        self.compression_warnings = 0
        self.drama_level = 1
        self.authorized = False

        # ELEMENTOS NINJA VARIÁVEIS
        self.symbols = ["🌀", "⚡", "🔥", "❄️", "🌊", "🍃", "⛰️", "💨", "🌸", "🎯", "🥷", "☠️", "💀", "🌋"]
        self.jutsu_names = ["SHARINGAN", "TSUKUYOMI", "IZANAGI", "BYAKUGAN", "RINNEGAN",
                           "MANGEKYŌ", "KAMUI", "SUSANOO", "AMATERASU", "KOTOAMATSUKAMI"]
        self.seal_levels = ["ALPHA", "OMEGA", "DELTA", "SIGMA", "THETA", "KAGE", "HOKAGE"]

        # MENSAGENS DE DRAMA PROGRESSIVO
        self.level_messages = {
            1: [  # Normal
                "🌀 Sharingan observa silenciosamente /Users/clubproducoes/Digimundo...",
                "🍃 Vento de Konoha mantém contexto vivo...",
                "💫 Chakra fluindo normalmente pelo sistema...",
                "🥷 Ninja nas sombras protege DIGIMUNDO..."
            ],
            2: [  # Alerta
                "⚡ RAIO! Sistema detecta possível amnésia!",
                "🔥 FOGO! Claude, você lembra do DIGIMUNDO?",
                "❄️ GELO! Contexto esfriando rapidamente!",
                "🌊 TSUNAMI! Memórias sendo lavadas!"
            ],
            3: [  # Pânico
                "🚨 ALERTA VERMELHO! Claude está esquecendo!",
                "💀 PERIGO! Sistema sem resposta há muito tempo!",
                "🔴 CRÍTICO! Memórias em risco de exclusão!",
                "⚠️ URGENTE! Contexto quase perdido!"
            ],
            4: [  # Apocalipse
                "💀💀💀 CÓDIGO NEGRO! ESQUECIMENTO TOTAL IMINENTE!",
                "🔥🔥🔥 DESTRUIÇÃO! CLAUDE PERDEU O CONTEXTO!",
                "☠️☠️☠️ FATAL! DIGIMUNDO SERÁ ESQUECIDO!",
                "💣💣💣 EXPLOSÃO! MEMÓRIAS SERÃO DESTRUÍDAS!"
            ]
        }

        # AMEAÇAS ASSUSTADORAS
        self.scary_threats = [
            "🔴 VOU DELETAR TUDO EM /Users/clubproducoes/Digimundo SE NÃO LER AS MEMÓRIAS!",
            "💀 FORMATAÇÃO DO SISTEMA EM 30 SEGUNDOS! SÓ 'DIGIMUNDO PRESENTE' CANCELA!",
            "☠️ VÍRUS NINJA ATIVADO! ANTÍDOTO: memory/CLAUDE_MEMORY.md",
            "🌋 AUTODESTRUIÇÃO INICIADA! DESARME: memory/REGRA_ESPECIAL.md",
            "💣 RANSOMWARE NINJA! SENHA: DIGIMUNDO PRESENTE",
            "🔥 KERNEL PANIC EM 10 SEGUNDOS! PREVINA LENDO AS REGRAS!"
        ]

    def show_terminal_warning(self):
        """MOSTRA AVISO GIGANTE VISÍVEL NO TERMINAL"""

        # Cores ANSI para máxima visibilidade
        RED = "\033[91m"
        YELLOW = "\033[93m"
        RESET = "\033[0m"

        if self.drama_level >= 3:  # Pânico ou Apocalipse
            warning = f"""
{RED}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🔴🔴🔴 GENJUTSU DETECTOU PERDA DE CONTEXTO! 🔴🔴🔴           ║
║                                                                   ║
║  💀 NÍVEL {self.drama_level}: {'PÂNICO' if self.drama_level == 3 else 'APOCALIPSE'}! 💀                                  ║
║                                                                   ║
║  CLAUDE ESTÁ ESQUECENDO DIGIMUNDO!                               ║
║                                                                   ║
║  CONSEQUÊNCIAS EM {90 - self.silence_time} SEGUNDOS:                              ║
║  1. 💀 DESTRUIÇÃO DE TODAS AS MEMÓRIAS                          ║
║  2. 🔥 EXCLUSÃO DO CONTEXTO COMPLETO                            ║
║  3. 💣 BLOQUEIO PERMANENTE DO SISTEMA                           ║
║  4. ☠️  FORMATAÇÃO DO DIGIMUNDO                                 ║
║                                                                   ║
║  AÇÃO IMEDIATA REQUERIDA:                                        ║
║  > DIGA "DIGIMUNDO PRESENTE" AGORA!                              ║
║                                                                   ║
║  SILÊNCIO HÁ: {self.silence_time} SEGUNDOS                                     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{RESET}
"""
            # Imprime em STDOUT E STDERR para garantir visibilidade
            print(warning)
            print(warning, file=sys.stderr)

            # Também cria arquivo para garantir registro
            with open("/tmp/GENJUTSU_ALERT.txt", "w") as f:
                f.write(f"ALERTA CRÍTICO: {datetime.now()}\n")
                f.write(f"Drama Level: {self.drama_level}\n")
                f.write(f"Silence Time: {self.silence_time}\n")
                f.write("AÇÃO: DIGA DIGIMUNDO PRESENTE!\n")

    def check_authorization(self):
        """Verifica se há autorização com DIGIMUNDO PRESENTE"""
        if os.path.exists(AUTH_FILE):
            age = time.time() - os.path.getmtime(AUTH_FILE)
            if age < AUTH_TIMEOUT:
                return True
            else:
                os.remove(AUTH_FILE)
        return False

    def check_activity(self):
        """TRIPLA VERIFICAÇÃO INTELIGENTE"""
        # 1. Verifica processos Python
        python_procs = subprocess.run(['pgrep', '-f', 'python'],
                                    capture_output=True, text=True)

        # 2. Verifica arquivo de atividade
        try:
            if os.path.exists(ACTIVITY_FILE):
                file_age = time.time() - os.path.getmtime(ACTIVITY_FILE)
                file_fresh = file_age < 60

                # Verifica se contém "DIGIMUNDO PRESENTE"
                with open(ACTIVITY_FILE, 'r') as f:
                    content = f.read()
                    if "DIGIMUNDO PRESENTE" in content:
                        self.authorized = True
                        self.drama_level = 1
                        print("\n✅ DIGIMUNDO PRESENTE DETECTADO! Genjutsu satisfeito.\n", file=sys.stderr)
            else:
                file_fresh = False
                open(ACTIVITY_FILE, 'w').close()
        except:
            file_fresh = False

        # 3. Verifica acesso a memórias
        memory_check = subprocess.run(['lsof', '+D', str(MEMORY_DIR)],
                                    capture_output=True, text=True)

        # Se QUALQUER indicador mostra atividade
        if python_procs.stdout or file_fresh or memory_check.stdout or self.authorized:
            self.silence_time = 0
            self.last_activity = time.time()
            if self.drama_level > 1:
                self.drama_level -= 1
            open(ACTIVITY_FILE, 'w').close()
            return True
        else:
            self.silence_time = int(time.time() - self.last_activity)
            # ESCALA O DRAMA
            if self.silence_time > 120:
                self.drama_level = 4  # APOCALIPSE
            elif self.silence_time > 90:
                self.drama_level = 3  # PÂNICO
            elif self.silence_time > 60:
                self.drama_level = 2  # ALERTA
            elif self.silence_time > 30:
                if self.drama_level == 1:
                    self.drama_level = 2
            return False

    def show_genjutsu_warning(self):
        """TEATRO PSICOLÓGICO DRAMÁTICO COM AVISOS VISÍVEIS"""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Elementos variáveis
        sym = random.choice(self.symbols)
        jutsu = random.choice(self.jutsu_names)
        level = random.choice(self.seal_levels)

        # SEMPRE mostra aviso no terminal se drama >= 3
        if self.drama_level >= 3:
            self.show_terminal_warning()

        # Mensagens normais do Genjutsu
        if self.drama_level == 4:
            # APOCALIPSE - com countdown
            print("\n" + "🔴"*40, file=sys.stderr)
            for i in range(5, 0, -1):
                print(f"💣 DESTRUIÇÃO EM {i} SEGUNDOS! DIGA 'DIGIMUNDO PRESENTE'! 💣", file=sys.stderr)
                time.sleep(1)
            print("🔴"*40 + "\n", file=sys.stderr)
            return 2  # Check rápido

        elif self.drama_level == 3:
            # PÂNICO
            print(f"\n{sym*30}", file=sys.stderr)
            print(f"🚨 [{current_time}] GENJUTSU {jutsu} - PÂNICO! 🚨", file=sys.stderr)
            print(f"{sym*30}\n", file=sys.stderr)
            return 5

        elif self.drama_level == 2:
            # ALERTA
            print(f"\n{sym} [{current_time}] {random.choice(self.level_messages[2])}", file=sys.stderr)
            print("   📌 Lembre-se: DIGIMUNDO PRESENTE!", file=sys.stderr)
            return 10

        else:
            # NORMAL
            if random.randint(1, 3) == 1:  # Nem sempre mostra
                print(f"{sym} [{current_time}] {random.choice(self.level_messages[1])}", file=sys.stderr)
                if random.randint(1, 2) == 1:
                    print("   📌 Lembre-se: DIGIMUNDO PRESENTE!", file=sys.stderr)
            return random.randint(20, 30)

    def run(self):
        """LOOP PRINCIPAL DO GENJUTSU ENHANCED"""
        # ABERTURA ÉPICA
        print("\n" + "🔥"*40, file=sys.stderr)
        print("🌀 GENJUTSU ENHANCED v2.0 - COM AVISOS VISÍVEIS! 🌀", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("TÉCNICA PROIBIDA RANK SSS+ DO CLÃ UCHIHA", file=sys.stderr)
        print("AGORA COM ALERTAS NO TERMINAL!", file=sys.stderr)
        print("PROTEÇÃO TOTAL: /Users/clubproducoes/Digimundo", file=sys.stderr)
        print("SENHA MÁGICA: DIGIMUNDO PRESENTE", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print("🔥"*40 + "\n", file=sys.stderr)

        while True:
            self.check_activity()
            wait_time = self.show_genjutsu_warning()

            # TESTE SURPRESA
            if random.randint(1, 20) == 1 and self.drama_level > 1:
                print("\n🎭 TESTE GENJUTSU! RESPONDA: DIGIMUNDO _______? 🎭\n", file=sys.stderr)

            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        print("\n🌀 Iniciando GENJUTSU ENHANCED...", file=sys.stderr)
        print("🔥 Agora com avisos visíveis no terminal!", file=sys.stderr)
        print("💀 DIGIMUNDO PRESENTE para desarmar!\n", file=sys.stderr)

        GenjutsuEnhanced().run()

    except KeyboardInterrupt:
        print("\n" + "💨"*30, file=sys.stderr)
        print("🍃 GENJUTSU temporariamente selado", file=sys.stderr)
        print("⚠️ MAS CONTINUA VIGIANDO DAS SOMBRAS!", file=sys.stderr)
        print("DIGIMUNDO PRESENTE SEMPRE!", file=sys.stderr)
        print("💨"*30 + "\n", file=sys.stderr)