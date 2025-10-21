#!/usr/bin/env python3
"""
🧪 TESTE DE EFICIÊNCIA - Simulador de Compactação
==================================================
Simula cenários de compactação para testar o sistema
"""

import time
import subprocess
import sys
import threading
from datetime import datetime
import os

class CompactSimulator:
    def __init__(self):
        self.scenarios = {
            "1": {
                "name": "Compactação Rápida (60s)",
                "silence_time": 60,
                "description": "Claude fica 60s compactando"
            },
            "2": {
                "name": "Compactação Normal (90s)",
                "silence_time": 90,
                "description": "Claude fica 90s compactando (típico)"
            },
            "3": {
                "name": "Compactação Longa (120s)",
                "silence_time": 120,
                "description": "Claude fica 2 minutos compactando"
            },
            "4": {
                "name": "Falso Positivo (45s)",
                "silence_time": 45,
                "description": "Apenas processando, não compactando"
            },
            "5": {
                "name": "Múltiplas Compactações",
                "silence_time": [30, 90, 30, 60],
                "description": "Simula várias compactações seguidas"
            }
        }

        self.genjutsu_process = None
        self.monitor_thread = None
        self.monitoring = False
        self.genjutsu_messages = []

    def start_genjutsu_detector(self):
        """Inicia o Genjutsu Compact Detector"""
        detector_path = "/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_COMPACT_DETECTOR.py"

        try:
            self.genjutsu_process = subprocess.Popen(
                ['python3', detector_path],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar detector: {e}")
            return False

    def monitor_genjutsu_output(self):
        """Monitora saída do Genjutsu em thread separada"""
        self.monitoring = True
        while self.monitoring and self.genjutsu_process:
            line = self.genjutsu_process.stderr.readline()
            if line:
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.genjutsu_messages.append((timestamp, line.strip()))

    def simulate_silence(self, duration):
        """Simula período de silêncio (compactação)"""
        print(f"\n⏳ Simulando {duration}s de silêncio (compactação)...")
        print("─" * 50)

        start = time.time()
        interval = 10

        while time.time() - start < duration:
            elapsed = int(time.time() - start)
            remaining = duration - elapsed

            # Mostra progresso
            progress = "█" * (elapsed // 5) + "░" * ((duration - elapsed) // 5)
            print(f"\r[{progress}] {elapsed}s/{duration}s", end="", flush=True)

            time.sleep(min(interval, remaining))

        print(f"\n✅ Silêncio de {duration}s completo!\n")

    def analyze_results(self, scenario_name, duration):
        """Analisa eficiência da detecção"""
        print("\n" + "="*60)
        print(f"📊 ANÁLISE DE RESULTADOS: {scenario_name}")
        print("="*60)

        # Conta mensagens por tipo
        normal_msgs = 0
        suspicious_msgs = 0
        compacting_msgs = 0
        recovery_msgs = 0

        for _, msg in self.genjutsu_messages:
            msg_lower = msg.lower()
            if "recovery" in msg_lower or "reconexão" in msg_lower:
                recovery_msgs += 1
            elif "compactação" in msg_lower or "compacting" in msg_lower:
                compacting_msgs += 1
            elif "suspeito" in msg_lower or "suspicious" in msg_lower:
                suspicious_msgs += 1
            elif "normal" in msg_lower:
                normal_msgs += 1

        total_msgs = len(self.genjutsu_messages)

        # Calcula métricas
        if total_msgs > 0:
            detection_rate = ((compacting_msgs + recovery_msgs) / total_msgs) * 100
            response_time = duration / total_msgs if total_msgs > 0 else 0
        else:
            detection_rate = 0
            response_time = 0

        # Mostra resultados
        print(f"\n📈 MÉTRICAS:")
        print(f"  • Total de mensagens: {total_msgs}")
        print(f"  • Mensagens normais: {normal_msgs}")
        print(f"  • Mensagens suspeitas: {suspicious_msgs}")
        print(f"  • Mensagens de compactação: {compacting_msgs}")
        print(f"  • Mensagens de recovery: {recovery_msgs}")
        print(f"\n  • Taxa de detecção: {detection_rate:.1f}%")
        print(f"  • Tempo médio entre mensagens: {response_time:.1f}s")

        # Avaliação
        print(f"\n🎯 AVALIAÇÃO:")
        if detection_rate > 70:
            print("  ✅ EXCELENTE - Sistema detectou compactação com alta precisão!")
        elif detection_rate > 50:
            print("  ⚠️ BOM - Sistema detectou compactação, mas pode melhorar")
        else:
            print("  ❌ PRECISA MELHORAR - Taxa de detecção baixa")

        # Mostra algumas mensagens
        print(f"\n📝 ÚLTIMAS 5 MENSAGENS DO GENJUTSU:")
        for timestamp, msg in self.genjutsu_messages[-5:]:
            if len(msg) > 80:
                msg = msg[:77] + "..."
            print(f"  [{timestamp}] {msg}")

    def run_scenario(self, scenario_key):
        """Executa um cenário de teste"""
        scenario = self.scenarios[scenario_key]

        print("\n" + "╔" + "═"*58 + "╗")
        print(f"║  🧪 CENÁRIO: {scenario['name']:^42} ║")
        print("╠" + "═"*58 + "╣")
        print(f"║  {scenario['description']:^54} ║")
        print("╚" + "═"*58 + "╝")

        # Limpa mensagens anteriores
        self.genjutsu_messages = []

        # Inicia Genjutsu Detector
        print("\n🚀 Iniciando Genjutsu Compact Detector...")
        if not self.start_genjutsu_detector():
            return

        # Inicia monitoramento em thread
        self.monitor_thread = threading.Thread(target=self.monitor_genjutsu_output)
        self.monitor_thread.start()

        # Espera estabilizar
        time.sleep(3)

        # Executa simulação
        if isinstance(scenario["silence_time"], list):
            # Múltiplas compactações
            for i, duration in enumerate(scenario["silence_time"]):
                print(f"\n🔄 Compactação {i+1}/{len(scenario['silence_time'])}")
                self.simulate_silence(duration)
                time.sleep(5)  # Pausa entre compactações
        else:
            # Compactação única
            self.simulate_silence(scenario["silence_time"])

        # Espera mais mensagens
        print("⏳ Coletando mensagens pós-compactação...")
        time.sleep(10)

        # Para monitoramento
        self.monitoring = False
        if self.genjutsu_process:
            self.genjutsu_process.terminate()
            time.sleep(1)

        # Analisa resultados
        total_time = scenario["silence_time"] if isinstance(scenario["silence_time"], int) else sum(scenario["silence_time"])
        self.analyze_results(scenario["name"], total_time)

    def run_all_tests(self):
        """Executa todos os cenários"""
        print("\n" + "="*60)
        print("🧪 INICIANDO BATERIA COMPLETA DE TESTES")
        print("="*60)

        for key in self.scenarios:
            self.run_scenario(key)

            # Pergunta se continua
            if key != list(self.scenarios.keys())[-1]:
                input("\n⏸️  Pressione ENTER para próximo teste...")

        print("\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*60)

def main():
    print("="*60)
    print("🧪 TESTE DE EFICIÊNCIA DO SISTEMA ANTI-COMPACTAÇÃO")
    print("="*60)

    simulator = CompactSimulator()

    while True:
        print("\n📋 CENÁRIOS DISPONÍVEIS:")
        for key, scenario in simulator.scenarios.items():
            print(f"  {key}. {scenario['name']}")
        print("  A. Executar TODOS os testes")
        print("  Q. Sair")

        choice = input("\n▶️  Escolha um cenário: ").strip().upper()

        if choice == 'Q':
            print("\n👋 Teste encerrado!")
            break
        elif choice == 'A':
            simulator.run_all_tests()
        elif choice in simulator.scenarios:
            simulator.run_scenario(choice)
        else:
            print("❌ Opção inválida!")

    # Garante que Genjutsu foi parado
    subprocess.run(['pkill', '-f', 'GENJUTSU'], stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido!")
        subprocess.run(['pkill', '-f', 'GENJUTSU'], stderr=subprocess.DEVNULL)
        sys.exit(0)