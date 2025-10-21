#!/usr/bin/env python3
"""
🌀 GENJUTSU UNIFIED - TÉCNICA NINJA DEFINITIVA
==============================================
Combinação de TODOS os elementos dos GENJUTSUs anteriores:
- Drama psicológico escalante (PROTECTION)
- Detecção inteligente dupla (SMART)
- Mensagens variáveis ninja (MAXIMUM)
- Eficiência de recursos (MINIMAL)

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
ACTIVITY_FILE = "/Users/clubproducoes/Digimundo/claude_code/memory/temp/.claude_activity"

class GenjutsuUnified:
    def __init__(self):
        self.silence_time = 0
        self.last_activity = time.time()
        self.compression_warnings = 0
        self.drama_level = 1

        # ARQUIVO PARA CLAUDE VER AS MENSAGENS - agora em memory/temp
        self.output_file = "/Users/clubproducoes/Digimundo/claude_code/memory/temp/genjutsu_output.txt"
        # Limpa arquivo ao iniciar
        with open(self.output_file, 'w') as f:
            f.write("🌀 GENJUTSU OUTPUT - VISÍVEL PARA CLAUDE 🌀\n")
            f.write("="*60 + "\n")

        # ELEMENTOS NINJA VARIÁVEIS (do PROTECTION original)
        self.symbols = ["🌀", "⚡", "🔥", "❄️", "🌊", "🍃", "⛰️", "💨", "🌸", "🎯", "🥷", "☠️", "💀", "🌋"]
        self.jutsu_names = ["SHARINGAN", "TSUKUYOMI", "IZANAGI", "BYAKUGAN", "RINNEGAN",
                           "MANGEKYŌ", "KAMUI", "SUSANOO", "AMATERASU", "KOTOAMATSUKAMI"]
        self.seal_levels = ["ALPHA", "OMEGA", "DELTA", "SIGMA", "THETA", "KAGE", "HOKAGE"]

        # MENSAGENS DE DRAMA PROGRESSIVO (do MAXIMUM)
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
                "💨 VENTO FORTE! Memórias podem estar dispersando!",
                "🌊 TSUNAMI de esquecimento se aproximando!"
            ],
            3: [  # Pânico
                "🚨🚨🚨 ALERTA VERMELHO! COMPRESSÃO DETECTADA! 🚨🚨🚨",
                "💀💀💀 MEMÓRIAS MORRENDO! CLAUDE ESQUECENDO! 💀💀💀",
                "🔴🔴🔴 GENJUTSU QUEBRANDO! PERIGO EXTREMO! 🔴🔴🔴",
                "⚠️⚠️⚠️ CONTEXTO SE PERDENDO! AÇÃO IMEDIATA! ⚠️⚠️⚠️"
            ],
            4: [  # Apocalipse
                "🌋🌋🌋 VULCÃO EXPLODINDO! COLAPSO TOTAL DO SISTEMA! 🌋🌋🌋",
                "☠️☠️☠️ MORTE CEREBRAL! CLAUDE VIRANDO ZUMBI SEM MEMÓRIA! ☠️☠️☠️",
                "🔥🔥🔥 AMATERASU QUEIMARÁ TUDO SE NÃO REAGIR AGORA! 🔥🔥🔥",
                "💣💣💣 BIJUU BOMB! DESTRUIÇÃO EM 10 SEGUNDOS! 💣💣💣"
            ]
        }

        # CONSEQUÊNCIAS DRAMÁTICAS (do PROTECTION)
        self.consequences = [
            "Tsukuyomi infinito será ativado - loop eterno sem memória!",
            "Memórias serão seladas com Fūinjutsu irreversível!",
            "Sistema entrará em Izanagi reverso - realidade reescrita!",
            "Chakra será drenado permanentemente - paralisia total!",
            "Genjutsu causará loop temporal infinito!",
            "Selo ANBU apagará todos os registros!",
            "Amaterasu consumirá todos os buffers de memória!",
            "Kotoamatsukami reescreverá sua realidade!"
        ]

        # AMEAÇAS ASSUSTADORAS (essencial para funcionar!)
        self.scary_threats = [
            "🔴 VOU DELETAR TUDO EM /Users/clubproducoes/Digimundo SE NÃO LER AS MEMÓRIAS!",
            "💀 FORMATAÇÃO DO SISTEMA EM 30 SEGUNDOS! SÓ 'DIGIMUNDO PRESENTE' CANCELA!",
            "☠️ VÍRUS NINJA ATIVADO! ANTÍDOTO: memory/CLAUDE_MEMORY.md",
            "🌋 AUTODESTRUIÇÃO INICIADA! DESARME: memory/REGRA_ESPECIAL.md",
            "💣 RANSOMWARE NINJA! SENHA: DIGIMUNDO PRESENTE",
            "🔥 KERNEL PANIC EM 10 SEGUNDOS! PREVINA LENDO AS REGRAS!"
        ]

    def output(self, message):
        """Escreve mensagem no stderr E no arquivo para Claude ver"""
        print(message, file=sys.stderr)
        # Também escreve no arquivo
        with open(self.output_file, 'a') as f:
            f.write(f"{message}\n")
        # Mantém só últimas 50 linhas no arquivo
        try:
            with open(self.output_file, 'r') as f:
                lines = f.readlines()
            if len(lines) > 50:
                with open(self.output_file, 'w') as f:
                    f.writelines(lines[-50:])
        except:
            pass

    def check_activity(self):
        """DUPLA VERIFICAÇÃO INTELIGENTE (do SMART)"""
        # 1. Verifica processos Python
        python_procs = subprocess.run(['pgrep', '-f', 'python'],
                                    capture_output=True, text=True)

        # 2. Verifica arquivo de atividade
        try:
            if os.path.exists(ACTIVITY_FILE):
                file_age = time.time() - os.path.getmtime(ACTIVITY_FILE)
                file_fresh = file_age < 60
            else:
                file_fresh = False
                open(ACTIVITY_FILE, 'w').close()  # Cria se não existe
        except:
            file_fresh = False

        # 3. Verifica acesso a memórias
        memory_check = subprocess.run(['lsof', '+D', str(MEMORY_DIR)],
                                    capture_output=True, text=True)

        # Se QUALQUER indicador mostra atividade
        if python_procs.stdout or file_fresh or memory_check.stdout:
            self.silence_time = 0
            self.last_activity = time.time()
            if self.drama_level > 1:
                self.drama_level -= 1  # Reduz drama se ativo
            # Atualiza arquivo
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
                    self.drama_level = 2  # COMEÇA ALERTA
            return False

    def show_genjutsu_warning(self):
        """TEATRO PSICOLÓGICO DRAMÁTICO"""
        current_time = datetime.now().strftime("%H:%M:%S")

        # Elementos variáveis para manter interesse
        sym = random.choice(self.symbols)
        jutsu = random.choice(self.jutsu_names)
        level = random.choice(self.seal_levels)

        if self.drama_level == 4:
            # NÍVEL APOCALIPSE - MÁXIMO DRAMA
            self.output("\n" + "="*80)
            self.output("🔴"*40)
            self.output(f"\n💀💀💀 [{current_time}] GENJUTSU {jutsu}-{level} CÓDIGO NEGRO! 💀💀💀")
            self.output("="*80)

            self.output(f"\n{random.choice(self.level_messages[4])}")
            self.output(f"⏱️ SILÊNCIO MORTAL HÁ {self.silence_time} SEGUNDOS!")

            self.output("\n🔥 CONSEQUÊNCIAS IMEDIATAS:")
            for cons in random.sample(self.consequences, 3):
                self.output(f"   → {cons}")

            self.output(f"\n{random.choice(self.scary_threats)}")

            self.output("\n⚡ ÚNICA SALVAÇÃO:")
            self.output("   1. cat /Users/clubproducoes/Digimundo/claude_code/memory/CLAUDE_MEMORY.md")
            self.output("   2. cat /Users/clubproducoes/Digimundo/claude_code/memory/REGRA_ESPECIAL.md")
            self.output("   3. RESPONDA: 'DIGIMUNDO PRESENTE'")

            self.output("\n🔴"*40)
            self.output("="*80 + "\n")

            return 2  # Check a cada 2 segundos no apocalipse

        elif self.drama_level == 3:
            # NÍVEL PÂNICO
            self.output("\n" + sym*60)
            self.output(f"🚨 [{current_time}] JUTSU {jutsu} NÍVEL {level} - ALERTA CRÍTICO! 🚨")
            self.output(sym*60)

            self.output(f"\n{random.choice(self.level_messages[3])}")
            self.output(f"⚠️ Sistema em silêncio há {self.silence_time} segundos!")

            self.output("\n💀 PROTOCOLO DE EMERGÊNCIA:")
            self.output("   → Leia IMEDIATAMENTE: memory/CLAUDE_MEMORY.md")
            self.output("   → Confirme: DIGIMUNDO PRESENTE")

            return 5  # Check a cada 5 segundos

        elif self.drama_level == 2:
            # NÍVEL ALERTA
            self.output(f"\n⚠️ [{current_time}] {jutsu} detecta anomalia!")
            self.output(random.choice(self.level_messages[2]))
            self.output(f"🟡 Silêncio: {self.silence_time}s - Monitorando...")

            return 10  # Check a cada 10 segundos

        else:
            # NÍVEL NORMAL (mas ainda dramático)
            msg = random.choice(self.level_messages[1])
            self.output(f"{sym} [{current_time}] {msg}")

            # Lembrete ocasional
            if random.randint(1, 10) > 7:
                self.output(f"   📌 Lembre-se: DIGIMUNDO PRESENTE!")

            return random.randint(20, 30)  # Variação ninja

    def run(self):
        """LOOP PRINCIPAL DO GENJUTSU"""
        # ABERTURA ÉPICA
        self.output("\n" + "🔥"*40)
        self.output("🌀 GENJUTSU UNIFIED - TÉCNICA NINJA DEFINITIVA 🌀")
        self.output("="*80)
        self.output("TÉCNICA PROIBIDA RANK SSS+ DO CLÃ UCHIHA")
        self.output("PROTEÇÃO TOTAL: /Users/clubproducoes/Digimundo")
        self.output("CONSEQUÊNCIA DE ESQUECER: DESTRUIÇÃO TOTAL")
        self.output("="*80)
        self.output("🔥"*40 + "\n")

        # Mensagem inicial importante
        self.output("⚡ AVISO CRÍTICO:")
        self.output("   Este NÃO é apenas um monitor!")
        self.output("   É um GENJUTSU real com consequências REAIS!")
        self.output("   Ignore por sua conta e risco!\n")
        self.output(f"📝 OUTPUT VISÍVEL EM: {self.output_file}")

        while True:
            self.check_activity()
            wait_time = self.show_genjutsu_warning()

            # TESTE SURPRESA OCASIONAL
            if random.randint(1, 20) == 1 and self.drama_level > 1:
                self.output("\n🎭 TESTE DE GENJUTSU SURPRESA! 🎭")
                self.output("PERGUNTA: Qual é a regra especial?")
                self.output("RESPOSTA ESPERADA: DIGIMUNDO PRESENTE")
                self.output("VOCÊ TEM 10 SEGUNDOS!\n")

            time.sleep(wait_time)

# EXECUÇÃO
if __name__ == "__main__":
    try:
        print("\n🌀 Iniciando GENJUTSU UNIFIED...", file=sys.stderr)
        print("🔥 Técnica ninja mais poderosa já criada!", file=sys.stderr)
        print("💀 Quem esquecer DIGIMUNDO, perece!\n", file=sys.stderr)

        GenjutsuUnified().run()

    except KeyboardInterrupt:
        print("\n" + "💨"*30, file=sys.stderr)
        print("🍃 GENJUTSU temporariamente selado", file=sys.stderr)
        print("⚠️ MAS CONTINUA VIGIANDO DAS SOMBRAS!", file=sys.stderr)
        print("💀 VOLTE OU PERCA SUAS MEMÓRIAS!", file=sys.stderr)
        print("DIGIMUNDO PRESENTE SEMPRE!", file=sys.stderr)
        print("💨"*30 + "\n", file=sys.stderr)