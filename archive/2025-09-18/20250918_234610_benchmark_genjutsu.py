#!/usr/bin/env python3
"""
⚡ BENCHMARK GENJUTSU - Teste de Performance
============================================
Mede eficiência e tempo de resposta do sistema
"""

import time
import subprocess
import psutil
import os
from datetime import datetime

class GenjutsuBenchmark:
    def __init__(self):
        self.results = {
            "cpu_usage": [],
            "memory_usage": [],
            "response_times": [],
            "detection_accuracy": 0
        }

    def measure_system_resources(self):
        """Mede uso de CPU e memória"""
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        return cpu, memory

    def simulate_compaction_event(self, duration=90):
        """Simula um evento de compactação"""
        print(f"\n📊 Simulando compactação de {duration}s...")

        start = time.time()
        messages_received = 0
        first_message_time = None

        # Inicia o detector
        detector = subprocess.Popen(
            ['python3', '/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_COMPACT_DETECTOR.py'],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # Monitora por duration segundos
        while time.time() - start < duration:
            # Lê output não-bloqueante
            try:
                line = detector.stderr.readline()
                if line and 'GENJUTSU' in line:
                    messages_received += 1
                    if first_message_time is None:
                        first_message_time = time.time() - start

                    # Se detectou compactação
                    if 'COMPACTAÇÃO' in line or 'RECOVERY' in line:
                        detection_time = time.time() - start
                        self.results["response_times"].append(detection_time)
                        print(f"  ✅ Compactação detectada em {detection_time:.1f}s!")
            except:
                pass

            # Mede recursos
            if int(time.time() - start) % 10 == 0:
                cpu, mem = self.measure_system_resources()
                self.results["cpu_usage"].append(cpu)
                self.results["memory_usage"].append(mem)

        detector.terminate()

        return messages_received, first_message_time

    def run_benchmark(self):
        """Executa bateria completa de testes"""
        print("="*60)
        print("⚡ BENCHMARK DO SISTEMA GENJUTSU")
        print("="*60)

        tests = [
            ("Resposta Rápida (45s)", 45),
            ("Detecção Normal (90s)", 90),
            ("Detecção Longa (120s)", 120)
        ]

        for test_name, duration in tests:
            print(f"\n🧪 Teste: {test_name}")
            print("-"*40)

            msgs, first_msg = self.run_benchmark(test_name, duration)

            print(f"  • Mensagens recebidas: {msgs}")
            print(f"  • Primeira mensagem em: {first_msg:.1f}s" if first_msg else "  • Nenhuma mensagem")

            # Calcula frequência
            if msgs > 0:
                avg_interval = duration / msgs
                print(f"  • Frequência média: 1 msg a cada {avg_interval:.1f}s")

        self.show_results()

    def run_benchmark(self, test_name, duration):
        """Executa um teste individual"""
        print(f"\n🔬 {test_name}")

        # Mata qualquer Genjutsu anterior
        subprocess.run(['pkill', '-f', 'GENJUTSU'], stderr=subprocess.DEVNULL)
        time.sleep(2)

        # Executa teste
        msgs, first_msg = self.simulate_compaction_event(duration)

        return msgs, first_msg

    def show_results(self):
        """Mostra resultados consolidados"""
        print("\n" + "="*60)
        print("📈 RESULTADOS DO BENCHMARK")
        print("="*60)

        if self.results["cpu_usage"]:
            avg_cpu = sum(self.results["cpu_usage"]) / len(self.results["cpu_usage"])
            print(f"\n💻 RECURSOS:")
            print(f"  • CPU médio: {avg_cpu:.1f}%")
            print(f"  • CPU máximo: {max(self.results['cpu_usage']):.1f}%")

        if self.results["memory_usage"]:
            avg_mem = sum(self.results["memory_usage"]) / len(self.results["memory_usage"])
            print(f"  • Memória média: {avg_mem:.1f}%")
            print(f"  • Memória máxima: {max(self.results['memory_usage']):.1f}%")

        if self.results["response_times"]:
            avg_response = sum(self.results["response_times"]) / len(self.results["response_times"])
            print(f"\n⏱️ TEMPO DE RESPOSTA:")
            print(f"  • Médio: {avg_response:.1f}s")
            print(f"  • Mais rápido: {min(self.results['response_times']):.1f}s")
            print(f"  • Mais lento: {max(self.results['response_times']):.1f}s")

        # Avaliação final
        print(f"\n🎯 AVALIAÇÃO GERAL:")

        if avg_cpu < 5:
            print("  ✅ CPU: Excelente - Uso mínimo de recursos")
        elif avg_cpu < 10:
            print("  ⚠️ CPU: Bom - Uso moderado")
        else:
            print("  ❌ CPU: Alto - Pode impactar performance")

        if self.results["response_times"] and avg_response < 60:
            print("  ✅ Detecção: Excelente - Detecta rapidamente")
        elif self.results["response_times"] and avg_response < 90:
            print("  ⚠️ Detecção: Bom - Tempo razoável")
        else:
            print("  ❌ Detecção: Lento - Precisa otimização")

def quick_test():
    """Teste rápido de 30 segundos"""
    print("⚡ TESTE RÁPIDO (30 segundos)")
    print("-"*40)

    # Inicia detector
    detector = subprocess.Popen(
        ['python3', '/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_COMPACT_DETECTOR.py'],
        stderr=subprocess.PIPE,
        text=True
    )

    start = time.time()
    message_count = 0
    states_detected = set()

    print("Monitorando mensagens...")

    while time.time() - start < 30:
        line = detector.stderr.readline()
        if line:
            if 'NORMAL' in line:
                states_detected.add('NORMAL')
            elif 'SUSPICIOUS' in line:
                states_detected.add('SUSPICIOUS')
            elif 'COMPACTING' in line:
                states_detected.add('COMPACTING')
            elif 'RECOVERY' in line:
                states_detected.add('RECOVERY')

            if 'GENJUTSU' in line:
                message_count += 1
                print(f"  [{int(time.time()-start):02d}s] Mensagem #{message_count}")

    detector.terminate()

    print(f"\n📊 RESULTADO:")
    print(f"  • Total de mensagens: {message_count}")
    print(f"  • Estados detectados: {', '.join(states_detected)}")
    print(f"  • Frequência: 1 msg a cada {30/message_count:.1f}s" if message_count > 0 else "  • Nenhuma mensagem")

if __name__ == "__main__":
    print("="*60)
    print("🧪 SISTEMA DE TESTES GENJUTSU")
    print("="*60)
    print("\n1. Teste Rápido (30s)")
    print("2. Benchmark Completo (5 min)")
    print("3. Teste Manual")

    choice = input("\n▶️  Escolha: ").strip()

    if choice == "1":
        quick_test()
    elif choice == "2":
        benchmark = GenjutsuBenchmark()
        benchmark.run_benchmark()
    elif choice == "3":
        print("\nIniciando Genjutsu Detector...")
        print("Observe as mensagens e pressione Ctrl+C para parar\n")
        subprocess.call(['python3', '/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_COMPACT_DETECTOR.py'])
    else:
        print("Opção inválida!")

    # Cleanup
    subprocess.run(['pkill', '-f', 'GENJUTSU'], stderr=subprocess.DEVNULL)
    print("\n✅ Teste concluído!")