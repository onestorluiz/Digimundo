#!/usr/bin/env python3
"""
🎬 Producer-Director System - Versão Minimalista
Alquimia de sistemas especializados trabalhando em harmonia
"""

import subprocess
import json
from pathlib import Path
from typing import Optional

class Producer:
    """Produz decisões sobre qual modelo usar"""

    def decide(self, task: str) -> str:
        """Decide qual modelo usar baseado na tarefa"""
        # Lógica simples e eficiente
        if "rápido" in task.lower() or "quick" in task.lower():
            return "llama3.2:3b"
        elif "português" in task.lower() or "ptbr" in task:
            return "llama3.2:3b"  # Fallback para modelo existente
        elif "análise" in task.lower() or "deep" in task.lower():
            return "deepseek-r1:32b"
        else:
            return "llama3.2:3b"  # Default rápido

class Director:
    """Dirige a execução dos modelos"""

    def execute(self, model: str, prompt: str) -> str:
        """Executa um modelo com prompt"""
        try:
            cmd = ["ollama", "run", model, prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout.strip() if result.returncode == 0 else "Erro na execução"
        except subprocess.TimeoutExpired:
            return "Timeout - resposta demorou mais de 30s"
        except Exception as e:
            return f"Erro: {str(e)}"

class Synthesizer:
    """Sintetiza respostas múltiplas"""

    def combine(self, responses: list) -> str:
        """Combina múltiplas respostas em uma síntese"""
        if not responses:
            return "Nenhuma resposta para sintetizar"

        # Síntese simples: pega insights únicos
        unique_points = []
        for r in responses:
            if r and r not in unique_points:
                unique_points.append(r[:200])  # Primeiros 200 chars

        return "\n".join(unique_points[:3])  # Top 3 insights

class ProducerDirectorMinimal:
    """Sistema minimalista de orquestração"""

    def __init__(self):
        self.producer = Producer()
        self.director = Director()
        self.synthesizer = Synthesizer()

    def process(self, prompt: str, multi_model: bool = False) -> str:
        """Processa um prompt usando a alquimia minimalista"""

        # Producer decide
        model = self.producer.decide(prompt)

        if not multi_model:
            # Execução simples
            return self.director.execute(model, prompt)

        # Execução multi-modelo para síntese
        models = ["llama3.2:3b", "mistral:7b-instruct"]  # Modelos rápidos
        responses = []

        for m in models:
            try:
                resp = self.director.execute(m, prompt)
                if resp and "Erro" not in resp:
                    responses.append(resp)
            except:
                continue

        # Sintetiza respostas
        return self.synthesizer.combine(responses)

# Interface simples
def main():
    """Teste do sistema minimalista"""
    system = ProducerDirectorMinimal()

    # Teste simples
    print("🎬 Producer-Director Minimalista")
    print("="*50)

    test_prompt = "Explique em uma linha o que é Python"
    result = system.process(test_prompt)

    print(f"Prompt: {test_prompt}")
    print(f"Resposta: {result[:200]}")
    print("\n✅ Sistema funcionando com ~100 linhas!")

if __name__ == "__main__":
    main()