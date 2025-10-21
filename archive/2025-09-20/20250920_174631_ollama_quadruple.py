#!/usr/bin/env python3
"""
🔥 OLLAMA QUADRUPLE SYSTEM - Mac Studio M3 Ultra Edition
Sistema de 4 modelos simultâneos para aproveitar 96GB RAM
"""

import subprocess
import json
import threading
import time
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import concurrent.futures
from dataclasses import dataclass

@dataclass
class QuadResponse:
    """Resposta do sistema quadruple"""
    model: str
    text: str
    time: float
    score: float = 0.0

class OllamaQuadruple:
    """Sistema QUADRUPLE para Mac Studio M3 Ultra - 96GB RAM"""

    def __init__(self):
        """Inicializa sistema com 4 modelos"""

        # CONFIGURAÇÃO QUADRUPLE - Total: ~47GB (metade da RAM)
        self.quad_models = {
            "scripturemon": "scripturemon-gpu-stable:latest",  # 19GB - Principal
            "deepseek": "deepseek-r1:32b",                    # 19GB - Análise profunda
            "mistral": "mistral:instruct",                    # 4.1GB - PT-BR
            "llama": "llama3.1:8b"                           # 4.9GB - Equilibrado
        }

        # Pesos para votação ponderada
        self.model_weights = {
            "scripturemon": 0.35,  # Principal tem mais peso
            "deepseek": 0.30,      # Análise profunda
            "mistral": 0.20,       # PT-BR
            "llama": 0.15          # Suporte
        }

        print("🔥 OLLAMA QUADRUPLE SYSTEM - MAC STUDIO M3 ULTRA")
        print(f"💪 RAM: 96GB | GPU: 60-Core | Neural: 32-Core")
        print(f"🎯 Modelos carregados: {list(self.quad_models.keys())}")
        print(f"📊 Uso estimado de RAM: ~47GB")

    def _call_model(self, model_name: str, model_path: str, prompt: str,
                    system: str = None, max_tokens: int = 500) -> QuadResponse:
        """Chama um modelo específico"""

        start_time = time.time()

        try:
            # Prepara prompt
            if system:
                full_prompt = f"{system}\n\n{prompt}"
            else:
                full_prompt = prompt

            # Comando Ollama
            cmd = ["ollama", "run", model_path, full_prompt]

            # Timeout baseado no modelo
            timeout = 120 if "32b" in model_path or "70b" in model_path else 60

            # Executa
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            elapsed = time.time() - start_time

            if result.returncode == 0:
                return QuadResponse(
                    model=model_name,
                    text=result.stdout.strip(),
                    time=elapsed,
                    score=self.model_weights.get(model_name, 0.1)
                )
            else:
                return QuadResponse(
                    model=model_name,
                    text=f"Erro: {result.stderr}",
                    time=elapsed,
                    score=0.0
                )

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            return QuadResponse(
                model=model_name,
                text="Timeout excedido",
                time=elapsed,
                score=0.0
            )
        except Exception as e:
            elapsed = time.time() - start_time
            return QuadResponse(
                model=model_name,
                text=f"Erro: {str(e)}",
                time=elapsed,
                score=0.0
            )

    def generate_parallel(self, prompt: str, system: str = None,
                         max_tokens: int = 500) -> Dict[str, Any]:
        """Gera respostas com 4 modelos em PARALELO"""

        print("\n🚀 EXECUÇÃO QUADRUPLE PARALELA")
        print(f"📝 Prompt: {prompt[:50]}...")

        responses = {}

        # Executor para paralelização
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:

            # Submete todas as tarefas
            futures = {
                executor.submit(
                    self._call_model,
                    name,
                    path,
                    prompt,
                    system,
                    max_tokens
                ): name
                for name, path in self.quad_models.items()
            }

            # Coleta resultados conforme chegam
            for future in concurrent.futures.as_completed(futures):
                model_name = futures[future]
                try:
                    response = future.result()
                    responses[model_name] = response
                    print(f"✅ {model_name}: {response.time:.2f}s")
                except Exception as e:
                    print(f"❌ {model_name}: {str(e)}")
                    responses[model_name] = QuadResponse(
                        model=model_name,
                        text=f"Erro: {str(e)}",
                        time=0,
                        score=0
                    )

        return self._process_responses(responses)

    def generate_sequential(self, prompt: str, system: str = None,
                           max_tokens: int = 500) -> Dict[str, Any]:
        """Gera respostas sequencialmente (para debug)"""

        print("\n⏳ EXECUÇÃO QUADRUPLE SEQUENCIAL")
        responses = {}

        for name, path in self.quad_models.items():
            print(f"🔄 Processando {name}...")
            response = self._call_model(name, path, prompt, system, max_tokens)
            responses[name] = response
            print(f"✅ {name}: {response.time:.2f}s")

        return self._process_responses(responses)

    def _process_responses(self, responses: Dict[str, QuadResponse]) -> Dict[str, Any]:
        """Processa e combina respostas dos 4 modelos"""

        # Calcula tempo total
        total_time = sum(r.time for r in responses.values())
        avg_time = total_time / len(responses)

        # Encontra melhor resposta (por score ponderado)
        best_response = max(responses.values(), key=lambda r: r.score)

        # Extrai todas as respostas
        all_texts = {name: r.text for name, r in responses.items()}

        # Análise de consenso (simplificada)
        consensus = self._analyze_consensus(responses)

        return {
            "best": best_response.text,
            "best_model": best_response.model,
            "all_responses": all_texts,
            "consensus": consensus,
            "total_time": total_time,
            "avg_time": avg_time,
            "models_used": list(responses.keys())
        }

    def _analyze_consensus(self, responses: Dict[str, QuadResponse]) -> str:
        """Analisa consenso entre modelos"""

        # Conta respostas válidas
        valid_responses = [r for r in responses.values() if r.score > 0]

        if len(valid_responses) == 0:
            return "Nenhuma resposta válida"
        elif len(valid_responses) == 1:
            return f"Apenas {valid_responses[0].model} respondeu"
        elif len(valid_responses) == len(responses):
            return "Consenso total - todos modelos responderam"
        else:
            failed = [name for name, r in responses.items() if r.score == 0]
            return f"Consenso parcial - falharam: {', '.join(failed)}"

    def benchmark(self, prompt: str = "Olá, responda com OK") -> Dict[str, Any]:
        """Benchmark do sistema quadruple"""

        print("\n📊 BENCHMARK QUADRUPLE SYSTEM")
        print("=" * 50)

        # Teste paralelo
        print("\n🚀 Teste PARALELO...")
        start = time.time()
        result_parallel = self.generate_parallel(prompt, max_tokens=50)
        time_parallel = time.time() - start

        # Teste sequencial
        print("\n⏳ Teste SEQUENCIAL...")
        start = time.time()
        result_sequential = self.generate_sequential(prompt, max_tokens=50)
        time_sequential = time.time() - start

        # Análise
        speedup = time_sequential / time_parallel

        print("\n📈 RESULTADOS:")
        print(f"⏱️ Tempo Sequencial: {time_sequential:.2f}s")
        print(f"⚡ Tempo Paralelo: {time_parallel:.2f}s")
        print(f"🚀 Speedup: {speedup:.2f}x")
        print(f"💾 RAM estimada: ~47GB")

        return {
            "parallel_time": time_parallel,
            "sequential_time": time_sequential,
            "speedup": speedup,
            "models": list(self.quad_models.keys())
        }

# Integração com OllamaCore existente
class OllamaCoreQuadExtension:
    """Extensão do OllamaCore para suportar modo Quadruple"""

    @staticmethod
    def enable_quad_mode(ollama_core_instance):
        """Adiciona modo quadruple ao OllamaCore existente"""

        # Adiciona instância quadruple
        ollama_core_instance.quad_system = OllamaQuadruple()

        # Adiciona método de geração quadruple
        def generate_quad(self, prompt, system=None, max_tokens=500, parallel=True):
            if parallel:
                return self.quad_system.generate_parallel(prompt, system, max_tokens)
            else:
                return self.quad_system.generate_sequential(prompt, system, max_tokens)

        # Injeta método
        ollama_core_instance.generate_quad = generate_quad.__get__(
            ollama_core_instance,
            ollama_core_instance.__class__
        )

        print("✅ Modo Quadruple ativado no OllamaCore!")
        return ollama_core_instance

if __name__ == "__main__":
    # Teste standalone
    quad = OllamaQuadruple()

    # Benchmark
    quad.benchmark()

    # Teste real
    result = quad.generate_parallel(
        prompt="Analise este conceito: Inteligência Artificial",
        system="Você é um especialista em tecnologia. Responda em português.",
        max_tokens=100
    )

    print("\n🎯 MELHOR RESPOSTA:")
    print(f"Modelo: {result['best_model']}")
    print(f"Texto: {result['best'][:200]}...")
    print(f"\n📊 Consenso: {result['consensus']}")
    print(f"⏱️ Tempo total: {result['total_time']:.2f}s")