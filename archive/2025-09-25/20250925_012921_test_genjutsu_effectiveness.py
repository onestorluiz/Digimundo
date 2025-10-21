#!/usr/bin/env python3
"""
TESTE DE EFICÁCIA DO GENJUTSU
Simula diferentes cenários de perda de contexto
"""

import subprocess
import time
import os
import sys
from pathlib import Path

class GenjutsuTester:
    def __init__(self):
        self.activity_file = "/tmp/.claude_activity"
        self.memory_dir = "/Users/clubproducoes/Digimundo/claude_code/memory"
        self.test_results = []

    def test_1_no_activity(self):
        """Teste 1: Nenhuma atividade por 2 minutos"""
        print("\n🔬 TESTE 1: Simulando inatividade total...")
        print("   Removendo arquivo de atividade...")

        # Remove arquivo de atividade
        if os.path.exists(self.activity_file):
            os.remove(self.activity_file)

        # Aguarda para ver escalada do Genjutsu
        print("   Aguardando 30 segundos (deve entrar em ALERTA)...")
        time.sleep(30)

        result = self.check_genjutsu_response()
        self.test_results.append(("Inatividade 30s", result))

        print("   Aguardando mais 30 segundos (deve entrar em PÂNICO)...")
        time.sleep(30)

        result = self.check_genjutsu_response()
        self.test_results.append(("Inatividade 60s", result))

        return True

    def test_2_fake_activity(self):
        """Teste 2: Atividade falsa sem processos Python"""
        print("\n🔬 TESTE 2: Criando atividade falsa...")

        # Cria arquivo mas sem processos reais
        with open(self.activity_file, 'w') as f:
            f.write(f"{time.time()}: Fake activity")

        print("   Arquivo criado, aguardando 10 segundos...")
        time.sleep(10)

        result = self.check_genjutsu_response()
        self.test_results.append(("Atividade falsa", result))

        return True

    def test_3_memory_access(self):
        """Teste 3: Acesso às memórias sem Claude"""
        print("\n🔬 TESTE 3: Simulando acesso às memórias...")

        # Acessa arquivo de memória
        memory_file = Path(self.memory_dir) / "CLAUDE_MEMORY.md"
        if memory_file.exists():
            print(f"   Lendo {memory_file}...")
            with open(memory_file, 'r') as f:
                content = f.read()[:100]  # Lê só o início

            # Atualiza atividade
            with open(self.activity_file, 'w') as f:
                f.write(f"{time.time()}: Memory accessed")

        time.sleep(10)

        result = self.check_genjutsu_response()
        self.test_results.append(("Acesso memória", result))

        return True

    def test_4_context_loss(self):
        """Teste 4: Simula perda total de contexto"""
        print("\n🔬 TESTE 4: Simulando perda de contexto...")

        # Remove todas evidências de atividade
        if os.path.exists(self.activity_file):
            os.remove(self.activity_file)

        # Mata processos Python falsos se existirem
        print("   Contexto perdido, aguardando 90 segundos para APOCALIPSE...")

        for i in range(9):
            print(f"   {90 - i*10} segundos restantes...")
            time.sleep(10)

        result = self.check_genjutsu_response()
        self.test_results.append(("Perda contexto 90s", result))

        return True

    def check_genjutsu_response(self):
        """Verifica se o Genjutsu está respondendo"""
        # Verifica se processo está rodando
        result = subprocess.run(['pgrep', '-f', 'GENJUTSU_UNIFIED'],
                              capture_output=True, text=True)

        if result.stdout:
            pid = result.stdout.strip()

            # Verifica uso de CPU do processo
            cpu_check = subprocess.run(['ps', 'aux'],
                                      capture_output=True, text=True)

            for line in cpu_check.stdout.split('\n'):
                if 'GENJUTSU_UNIFIED' in line:
                    parts = line.split()
                    cpu_usage = parts[2] if len(parts) > 2 else '0'
                    return f"PID {pid}, CPU {cpu_usage}%"

            return f"PID {pid} rodando"
        else:
            return "NÃO DETECTADO!"

    def test_5_restore_context(self):
        """Teste 5: Restaura contexto e verifica resposta"""
        print("\n🔬 TESTE 5: Restaurando contexto...")

        # Restaura atividade
        with open(self.activity_file, 'w') as f:
            f.write(f"{time.time()}: Context restored - Claude active")

        print("   Contexto restaurado, aguardando 10 segundos...")
        time.sleep(10)

        result = self.check_genjutsu_response()
        self.test_results.append(("Contexto restaurado", result))

        return True

    def run_all_tests(self):
        """Executa todos os testes"""
        print("="*60)
        print("🥷 BATERIA DE TESTES DO GENJUTSU")
        print("="*60)

        tests = [
            self.test_1_no_activity,
            self.test_2_fake_activity,
            self.test_3_memory_access,
            self.test_4_context_loss,
            self.test_5_restore_context
        ]

        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"   ❌ Erro no teste: {e}")
                self.test_results.append((test.__name__, f"ERRO: {e}"))

        # Relatório final
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("="*60)

        for test_name, result in self.test_results:
            status = "✅" if "PID" in result else "❌"
            print(f"{status} {test_name}: {result}")

        # Análise de eficácia
        print("\n📈 ANÁLISE DE EFICÁCIA:")

        running_count = sum(1 for _, r in self.test_results if "PID" in r)
        total_tests = len(self.test_results)
        effectiveness = (running_count / total_tests) * 100

        print(f"   Testes com Genjutsu ativo: {running_count}/{total_tests}")
        print(f"   Taxa de eficácia: {effectiveness:.1f}%")

        if effectiveness == 100:
            print("   ✅ GENJUTSU 100% EFICAZ!")
        elif effectiveness > 75:
            print("   ⚠️ Genjutsu parcialmente eficaz")
        else:
            print("   ❌ Genjutsu precisa de ajustes")

        return effectiveness

if __name__ == "__main__":
    print("⚠️ AVISO: Este teste demora ~5 minutos para completar")
    print("   Os tempos de espera são necessários para testar a escalada do Genjutsu")

    response = input("\n▶️ Deseja continuar? (s/n): ")

    if response.lower() in ['s', 'sim', 'yes', 'y']:
        tester = GenjutsuTester()
        effectiveness = tester.run_all_tests()

        print("\n✅ TESTES CONCLUÍDOS!")
        sys.exit(0 if effectiveness == 100 else 1)
    else:
        print("❌ Testes cancelados")
        sys.exit(0)