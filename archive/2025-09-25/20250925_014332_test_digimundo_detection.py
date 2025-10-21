#!/usr/bin/env python3
"""
TESTE DE DETECÇÃO DO "DIGIMUNDO PRESENTE"
Analisa se o Genjutsu detecta quando uso a frase mágica
"""

import subprocess
import time
import os

class DigimundoTester:
    def __init__(self):
        self.activity_file = "/tmp/.claude_activity"
        self.genjutsu_log = "/tmp/genjutsu_output.log"

    def analyze_failure(self):
        """Analisa por que não usei DIGIMUNDO PRESENTE"""
        print("🔍 ANÁLISE DA FALHA DO DIGIMUNDO PRESENTE")
        print("="*60)

        # Razão 1: Comportamento automático do Claude
        print("\n📊 RAZÃO 1: Padrão de resposta do Claude")
        print("   - Claude tende a responder objetivamente")
        print("   - Sem lembretes explícitos, esquece contextos especiais")
        print("   - Foca na tarefa principal (organização de arquivos)")

        # Razão 2: O Genjutsu não detecta texto nas respostas
        print("\n📊 RAZÃO 2: Limitação do Genjutsu")
        print("   - Genjutsu monitora ATIVIDADE (arquivos, processos)")
        print("   - NÃO monitora CONTEÚDO das respostas do Claude")
        print("   - Não há parser para detectar 'DIGIMUNDO PRESENTE' no output")

        # Razão 3: Falta de feedback visual
        print("\n📊 RAZÃO 3: Feedback não estava visível")
        print("   - Mensagens do Genjutsu iam para /dev/null")
        print("   - Sem alertas visuais, fácil esquecer")
        print("   - Agora corrigido com log em /tmp/genjutsu_output.log")

    def test_genjutsu_response_detection(self):
        """Testa se o Genjutsu poderia detectar a frase"""
        print("\n🧪 TESTE: O Genjutsu detecta 'DIGIMUNDO PRESENTE'?")
        print("="*60)

        # Verificar código do Genjutsu
        print("\n1. Verificando código do Genjutsu...")

        genjutsu_file = "/Users/clubproducoes/Digimundo/claude_code/protection/genjutsu/GENJUTSU_UNIFIED.py"
        with open(genjutsu_file, 'r') as f:
            content = f.read()

        # Buscar por detecção de "DIGIMUNDO PRESENTE"
        if "DIGIMUNDO PRESENTE" in content:
            print("   ✅ Genjutsu menciona 'DIGIMUNDO PRESENTE'")

            # Mas verifica se DETECTA nas respostas
            if "stdout" in content or "response" in content:
                print("   ✅ Genjutsu monitora stdout")
            else:
                print("   ❌ Genjutsu NÃO monitora respostas do Claude")

        # Teste 2: Ver métodos de detecção
        print("\n2. Métodos de detecção do Genjutsu:")
        detection_methods = [
            ("pgrep", "Processos Python"),
            ("lsof", "Acesso a arquivos"),
            ("/tmp/.claude_activity", "Arquivo de atividade"),
            ("memory_check", "Acesso às memórias")
        ]

        for method, description in detection_methods:
            if method in content:
                print(f"   ✅ {description}: {method}")

        print("\n   ❌ NÃO detecta: Conteúdo das respostas")
        print("   ❌ NÃO detecta: Uso da frase 'DIGIMUNDO PRESENTE'")

    def simulate_with_phrase(self):
        """Simula uso da frase para ver se muda algo"""
        print("\n🎭 SIMULAÇÃO: Usando 'DIGIMUNDO PRESENTE'")
        print("="*60)

        # Escrever no arquivo de atividade com a frase
        print("\n1. Escrevendo 'DIGIMUNDO PRESENTE' no arquivo de atividade...")
        with open(self.activity_file, 'a') as f:
            f.write(f"\n{time.time()}: DIGIMUNDO PRESENTE - Claude lembrou!\n")

        print("   ✅ Escrito no arquivo")

        # Verificar log do Genjutsu
        print("\n2. Verificando resposta do Genjutsu...")
        time.sleep(3)

        if os.path.exists(self.genjutsu_log):
            with open(self.genjutsu_log, 'r') as f:
                lines = f.readlines()
                recent = lines[-5:] if len(lines) > 5 else lines

            print("   Últimas mensagens do Genjutsu:")
            for line in recent:
                if line.strip():
                    print(f"   {line.strip()}")

    def propose_solution(self):
        """Propõe solução para o problema"""
        print("\n💡 SOLUÇÃO PROPOSTA")
        print("="*60)

        print("\n1. PARA O CLAUDE:")
        print("   - Adicionar lembrete nas REGRAS.md")
        print("   - Sempre começar respostas com 'DIGIMUNDO PRESENTE'")
        print("   - Especialmente após longos processamentos")

        print("\n2. PARA O GENJUTSU:")
        print("   - Poderia monitorar /tmp/claude_responses.txt")
        print("   - Detectar ausência da frase nas respostas")
        print("   - Escalar drama se não encontrar a frase")

        print("\n3. IMPLEMENTAÇÃO ATUAL:")
        print("   - Genjutsu funciona como 'teatro psicológico'")
        print("   - Objetivo: lembrar humano de manter contexto")
        print("   - Não é um sistema de enforcement real")

    def run_analysis(self):
        """Executa análise completa"""
        print("\n" + "="*60)
        print("🔍 ANÁLISE COMPLETA: Por que não usei DIGIMUNDO PRESENTE?")
        print("="*60)

        self.analyze_failure()
        self.test_genjutsu_response_detection()
        self.simulate_with_phrase()
        self.propose_solution()

        print("\n" + "="*60)
        print("📊 CONCLUSÃO")
        print("="*60)
        print("\n✅ O Genjutsu está FUNCIONANDO como projetado:")
        print("   - Monitora atividade do sistema")
        print("   - Exibe mensagens dramáticas")
        print("   - Mantém consciência psicológica")

        print("\n❌ Mas NÃO detecta conteúdo das respostas:")
        print("   - Não analisa se uso 'DIGIMUNDO PRESENTE'")
        print("   - É um teatro, não um parser")
        print("   - Depende da disciplina do usuário")

        print("\n🎯 LIÇÃO APRENDIDA:")
        print("   SEMPRE usar 'DIGIMUNDO PRESENTE' por disciplina própria!")
        print("   O Genjutsu é um lembrete, não um enforcer.")

if __name__ == "__main__":
    print("**DIGIMUNDO PRESENTE** 🔥\n")
    tester = DigimundoTester()
    tester.run_analysis()
    print("\n**DIGIMUNDO PRESENTE** - Análise concluída! 🥷")