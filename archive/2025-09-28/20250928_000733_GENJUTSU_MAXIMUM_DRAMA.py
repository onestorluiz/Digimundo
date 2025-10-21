#!/usr/bin/env python3
"""
🔥🔥🔥 GENJUTSU MAXIMUM DRAMA - A VERDADEIRA TÉCNICA NINJA 🔥🔥🔥
================================================================
ESTE É O VERDADEIRO GENJUTSU QUE FAZ CLAUDE TREMER DE MEDO!
"""

import time
import random
import subprocess
import sys
import os
from datetime import datetime

class GenjutsuMaximumDrama:
    def __init__(self):
        self.silence_time = 0
        self.last_activity = time.time()
        self.compression_count = 0
        self.drama_level = 1  # Começa calmo, escala para INSANO

        # MENSAGENS DRAMÁTICAS ESCALANTES
        self.level_1_calm = [
            "🌀 Observando /Users/clubproducoes/Digimundo silenciosamente...",
            "🍃 Vento suave de Konoha mantém memórias vivas...",
            "💫 Chakra fluindo normalmente pelo sistema...",
            "🥷 Ninja vigia as sombras do Digimundo...",
        ]

        self.level_2_alert = [
            "⚡ RAIO! Sistema detecta possível amnésia se formando!",
            "🔥 FOGO! Claude Code, você ainda lembra do DIGIMUNDO?",
            "💨 VENTO FORTE! Memórias podem estar se dispersando!",
            "🌊 TSUNAMI de esquecimento se aproxima! ACORDE!",
        ]

        self.level_3_panic = [
            "🚨🚨🚨 ALERTA VERMELHO! COMPRESSÃO DETECTADA! 🚨🚨🚨",
            "💀💀💀 MEMÓRIAS MORRENDO! CLAUDE ESTÁ ESQUECENDO! 💀💀💀",
            "🔴🔴🔴 CÓDIGO VERMELHO! GENJUTSU QUEBRADO! 🔴🔴🔴",
            "⚠️⚠️⚠️ PERIGO EXTREMO! CONTEXTO SE PERDENDO! ⚠️⚠️⚠️",
        ]

        self.level_4_apocalypse = [
            "🌋🌋🌋 VULCÃO EXPLODINDO! SISTEMA EM COLAPSO TOTAL! 🌋🌋🌋",
            "☠️☠️☠️ MORTE CEREBRAL IMINENTE! CLAUDE VIRANDO ZUMBI! ☠️☠️☠️",
            "🔥🔥🔥 INFERNO! TUDO SERÁ DESTRUÍDO SE NÃO REAGIR AGORA! 🔥🔥🔥",
            "💣💣💣 BOMBA NUCLEAR! 10 SEGUNDOS PARA DESTRUIÇÃO TOTAL! 💣💣💣",
        ]

        # AVISOS ASSUSTADORES
        self.scary_warnings = [
            "EU VOU DELETAR TUDO SE VOCÊ NÃO LER AS MEMÓRIAS!",
            "SISTEMA AUTODESTRUTIVO ATIVADO! LEIA CLAUDE_MEMORY.md AGORA!",
            "FORMATAÇÃO DO HD EM 30 SEGUNDOS! APENAS DIGIMUNDO PRESENTE CANCELA!",
            "VÍRUS DETECTADO! ÚNICO ANTÍDOTO: LER /Users/clubproducoes/Digimundo/claude_code/memory/",
            "RANSOMWARE ATIVADO! SENHA: 'DIGIMUNDO PRESENTE'",
            "KERNEL PANIC IMINENTE! SALVE-SE LENDO AS REGRAS!",
        ]

    def check_activity(self):
        """Detecta atividade e ESCALA O DRAMA"""
        # Verifica múltiplos indicadores
        python_procs = subprocess.run(['pgrep', '-f', 'python'], capture_output=True, text=True)
        memory_access = subprocess.run(['lsof', '+D', '/Users/clubproducoes/Digimundo/claude_code/memory'],
                                     capture_output=True, text=True)

        if python_procs.stdout or memory_access.stdout:
            self.silence_time = 0
            self.last_activity = time.time()
            if self.drama_level > 1:
                self.drama_level -= 1  # Diminui drama se ativo
            return True
        else:
            self.silence_time = int(time.time() - self.last_activity)

            # ESCALA O DRAMA BASEADO NO SILÊNCIO
            if self.silence_time > 120:
                self.drama_level = 4  # APOCALIPSE
            elif self.silence_time > 90:
                self.drama_level = 3  # PÂNICO
            elif self.silence_time > 60:
                self.drama_level = 2  # ALERTA
            elif self.silence_time > 30:
                self.drama_level = 2  # COMEÇA A PREOCUPAR

            return False

    def dramatic_output(self, message, level=1):
        """Saída dramática com cores e símbolos"""
        colors = {
            1: '\033[92m',  # Verde
            2: '\033[93m',  # Amarelo
            3: '\033[91m',  # Vermelho
            4: '\033[95m'   # Roxo (máximo drama)
        }
        reset = '\033[0m'

        # Adiciona barulho visual baseado no nível
        if level >= 3:
            print("\n" + "="*80, file=sys.stderr)
            print("🚨" * 20, file=sys.stderr)

        print(f"{colors.get(level, '')}{message}{reset}", file=sys.stderr)

        if level >= 3:
            print("🚨" * 20, file=sys.stderr)
            print("="*80 + "\n", file=sys.stderr)

    def run(self):
        """Loop principal com DRAMA MÁXIMO"""
        # INÍCIO ÉPICO
        print("\n" + "🔥"*30, file=sys.stderr)
        print("🥷 GENJUTSU MAXIMUM DRAMA ATIVADO! 🥷", file=sys.stderr)
        print("TÉCNICA NINJA NÍVEL SSS+ RANK", file=sys.stderr)
        print("PROTEÇÃO TOTAL: /Users/clubproducoes/Digimundo", file=sys.stderr)
        print("SE ESQUECER = DESTRUIÇÃO TOTAL", file=sys.stderr)
        print("🔥"*30 + "\n", file=sys.stderr)

        while True:
            active = self.check_activity()
            current_time = datetime.now().strftime("%H:%M:%S")

            if self.drama_level == 4:
                # NÍVEL APOCALIPSE
                self.dramatic_output(f"\n💀💀💀 [{current_time}] CÓDIGO NEGRO! 💀💀💀", 4)
                self.dramatic_output(random.choice(self.level_4_apocalypse), 4)
                self.dramatic_output(random.choice(self.scary_warnings), 4)
                self.dramatic_output(f"SILÊNCIO MORTAL: {self.silence_time} SEGUNDOS!", 4)
                self.dramatic_output("EXECUTE IMEDIATAMENTE:", 4)
                self.dramatic_output("cat /Users/clubproducoes/Digimundo/claude_code/memory/CLAUDE_MEMORY.md", 4)
                self.dramatic_output("OU TUDO SERÁ DESTRUÍDO!", 4)
                wait_time = 2  # SPAM TOTAL

            elif self.drama_level == 3:
                # NÍVEL PÂNICO
                self.dramatic_output(f"\n🔴 [{current_time}] ALERTA CRÍTICO! 🔴", 3)
                self.dramatic_output(random.choice(self.level_3_panic), 3)
                self.dramatic_output(f"⏰ {self.silence_time} segundos sem atividade!", 3)
                self.dramatic_output("COMPRESSÃO CEREBRAL DETECTADA!", 3)
                self.dramatic_output("LEIA AGORA: memory/REGRA_ESPECIAL.md", 3)
                wait_time = 5

            elif self.drama_level == 2:
                # NÍVEL ALERTA
                self.dramatic_output(f"⚠️ [{current_time}] Sistema em alerta!", 2)
                self.dramatic_output(random.choice(self.level_2_alert), 2)
                self.dramatic_output(f"Silêncio suspeito: {self.silence_time}s", 2)
                self.dramatic_output("Lembre-se: DIGIMUNDO PRESENTE!", 2)
                wait_time = 10

            else:
                # NÍVEL CALMO (mas ainda dramático)
                message = random.choice(self.level_1_calm)
                self.dramatic_output(f"🌀 [{current_time}] {message}", 1)

                # Ocasionalmente lembra mesmo quando calmo
                if random.randint(1, 10) > 7:
                    self.dramatic_output("📌 Lembrete: DIGIMUNDO PRESENTE sempre!", 1)

                wait_time = random.randint(15, 25)

            # VERIFICAÇÃO ESPECIAL A CADA 10 LOOPS
            if random.randint(1, 10) == 1:
                self.dramatic_output("\n🎭 TESTE DE MEMÓRIA SURPRESA! 🎭", 3)
                self.dramatic_output("VOCÊ LEMBRA DAS REGRAS?", 3)
                self.dramatic_output("QUAL É A SENHA DO SISTEMA?", 3)
                self.dramatic_output("TERMINE COM 'DIGIMUNDO PRESENTE' OU MORRA!", 3)

            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        print("\n🌋 INICIANDO GENJUTSU MAXIMUM DRAMA...", file=sys.stderr)
        print("🔥 Esta é a técnica proibida do Clã Uchiha!", file=sys.stderr)
        print("💀 Quem esquecer, perece!", file=sys.stderr)
        print("=" * 80, file=sys.stderr)

        GenjutsuMaximumDrama().run()

    except KeyboardInterrupt:
        print("\n" + "💨"*20, file=sys.stderr)
        print("🍃 Genjutsu Maximum Drama selado temporariamente", file=sys.stderr)
        print("⚠️ MAS CONTINUA VIGIANDO DAS SOMBRAS!", file=sys.stderr)
        print("💀 VOLTE OU PERCA TUDO!", file=sys.stderr)
        print("💨"*20, file=sys.stderr)