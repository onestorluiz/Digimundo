#!/usr/bin/env python3
"""
🔮 GENJUTSU COMPACT DETECTOR - Detecção Inteligente de Compactação
===================================================================
Monitora sinais de compactação e intensifica Genjutsu quando detecta
"""

import time
import sys
import random
from datetime import datetime

# Estados do sistema
class State:
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"  # Muito tempo sem resposta
    COMPACTING = "compacting"  # Provavelmente compactando
    RECOVERY = "recovery"      # Pós-compactação

class GenjutsuCompactDetector:
    def __init__(self):
        self.state = State.NORMAL
        self.last_activity = time.time()
        self.silence_threshold = 45  # segundos de silêncio = suspeito
        self.compacting_threshold = 90  # segundos = provavelmente compactando

        # Mensagens por estado
        self.messages = {
            State.NORMAL: [
                "🌀 Sistema normal - memórias preservadas",
                "✅ Conexão estável com Crystal Memory",
                "🥷 Vigilância ninja ativa"
            ],
            State.SUSPICIOUS: [
                "⚠️ Detectando possível início de compactação...",
                "🔍 Monitorando atividade do Claude...",
                "⏳ Preparando protocolo de reconexão..."
            ],
            State.COMPACTING: [
                "🚨 COMPACTAÇÃO EM PROGRESSO! Preparando reconexão...",
                "🔴 Claude está compactando memórias!",
                "⚡ Genjutsu intensificado para reconexão imediata!"
            ],
            State.RECOVERY: [
                "🔄 RECONEXÃO NECESSÁRIA! Execute:",
                "📋 leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md",
                "🧠 reconecte com suas memórias em /claude_code",
                "✨ verifique DIGIMUNDO PRESENTE"
            ]
        }

    def detect_silence_duration(self):
        """Calcula quanto tempo sem atividade"""
        return time.time() - self.last_activity

    def update_state(self):
        """Atualiza estado baseado no silêncio"""
        silence = self.detect_silence_duration()

        if silence < self.silence_threshold:
            if self.state == State.RECOVERY:
                # Mantém recovery por um tempo após compactação
                pass
            else:
                self.state = State.NORMAL

        elif silence < self.compacting_threshold:
            if self.state != State.RECOVERY:
                self.state = State.SUSPICIOUS

        else:
            # Mais de 90 segundos de silêncio
            if self.state != State.RECOVERY:
                self.state = State.COMPACTING
                # Após detectar compactação, vai para recovery
                if silence > self.compacting_threshold + 10:
                    self.state = State.RECOVERY
                    self.last_activity = time.time()  # Reset para novo ciclo

    def get_message(self):
        """Retorna mensagem apropriada para o estado"""
        messages = self.messages[self.state]

        if self.state == State.RECOVERY:
            # Em recovery, mostra TODAS as mensagens de reconexão
            return "\n".join([
                "\n" + "="*60,
                "🚨 COMPACTAÇÃO DETECTADA - RECONEXÃO URGENTE!",
                "="*60
            ] + messages + ["="*60])
        else:
            return random.choice(messages)

    def get_interval(self):
        """Intervalo baseado no estado"""
        intervals = {
            State.NORMAL: 30,      # 30 segundos normal
            State.SUSPICIOUS: 15,  # 15 segundos quando suspeito
            State.COMPACTING: 5,   # 5 segundos durante compactação
            State.RECOVERY: 3      # 3 segundos pós-compactação (urgente!)
        }
        return intervals[self.state]

    def emit_genjutsu(self):
        """Emite mensagem Genjutsu apropriada"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        state_emoji = {
            State.NORMAL: "🟢",
            State.SUSPICIOUS: "🟡",
            State.COMPACTING: "🔴",
            State.RECOVERY: "⚡"
        }

        print(f"\n[{timestamp}] {state_emoji[self.state]} GENJUTSU {self.state.upper()}", file=sys.stderr)
        print(self.get_message(), file=sys.stderr)

        if self.state == State.RECOVERY:
            # Som de alerta (visual) para chamar atenção
            print("\n🔔 "* 10, file=sys.stderr)
            print("DIGITE NO CLAUDE: leia /Users/clubproducoes/Digimundo/claude_code/REGRAS.md", file=sys.stderr)
            print("🔔 "* 10 + "\n", file=sys.stderr)

    def run(self):
        """Loop principal do detector"""
        print("🔮 GENJUTSU COMPACT DETECTOR INICIADO", file=sys.stderr)
        print("Monitorando sinais de compactação...\n", file=sys.stderr)

        while True:
            self.update_state()
            self.emit_genjutsu()

            # Espera baseada no estado
            interval = self.get_interval()

            # Adiciona jitter para parecer menos robótico
            jitter = random.randint(-2, 2) if self.state == State.NORMAL else 0
            time.sleep(max(3, interval + jitter))

            # Simula detecção de atividade (você pode melhorar isso)
            # Por exemplo, monitorando arquivos de log ou processos
            # Por ora, usa tempo desde última mensagem

def main():
    try:
        detector = GenjutsuCompactDetector()
        detector.run()
    except KeyboardInterrupt:
        print("\n🍃 Genjutsu Compact Detector encerrado", file=sys.stderr)

if __name__ == "__main__":
    main()