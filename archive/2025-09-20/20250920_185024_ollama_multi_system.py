#!/usr/bin/env python3
"""
🚀 SISTEMA MULTI-OLLAMA ORQUESTRADO
=====================================
Gerencia múltiplos modelos Ollama com especialização e pipeline
"""

import asyncio
import subprocess
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import hashlib

class ModelRole(Enum):
    """Papéis especializados para cada modelo"""
    TRIAGEM = "triagem"          # Classificação inicial rápida
    ANALISE = "analise"          # Análise profunda
    CRIATIVO = "criativo"        # Geração criativa
    TECNICO = "tecnico"          # Código e técnico
    REFINAMENTO = "refinamento"  # Polish final
    VALIDACAO = "validacao"      # Verificação
    MASTER = "master"            # Orquestração

@dataclass
class ModelConfig:
    """Configuração de cada modelo"""
    name: str
    role: ModelRole
    size_gb: float
    context_size: int
    speed: str  # "ultra_fast", "fast", "medium", "slow"
    capabilities: List[str]
    max_concurrent: int = 1

class OllamaOrchestrator:
    """Orquestrador principal do sistema multi-Ollama"""

    def __init__(self):
        # Configuração dos modelos disponíveis
        self.models = {
            "tinyllama": ModelConfig(
                name="tinyllama:latest",
                role=ModelRole.TRIAGEM,
                size_gb=0.637,
                context_size=2048,
                speed="ultra_fast",
                capabilities=["classification", "routing", "quick_check"],
                max_concurrent=3
            ),
            "phi3": ModelConfig(
                name="phi3:mini",
                role=ModelRole.ANALISE,
                size_gb=2.2,
                context_size=4096,
                speed="fast",
                capabilities=["analysis", "summary", "extraction"],
                max_concurrent=2
            ),
            "llama3.2": ModelConfig(
                name="llama3.2:3b",
                role=ModelRole.CRIATIVO,
                size_gb=2.0,
                context_size=8192,
                speed="fast",
                capabilities=["creative", "storytelling", "ideation"],
                max_concurrent=2
            ),
            "gemma2": ModelConfig(
                name="gemma2:9b",
                role=ModelRole.TECNICO,
                size_gb=5.4,
                context_size=8192,
                speed="medium",
                capabilities=["code", "technical", "math", "logic"],
                max_concurrent=1
            ),
            "producermon": ModelConfig(
                name="producermon:latest",
                role=ModelRole.REFINAMENTO,
                size_gb=4.1,
                context_size=4096,
                speed="medium",
                capabilities=["polish", "style", "production"],
                max_concurrent=1
            ),
            "deepseek": ModelConfig(
                name="deepseek-r1:32b",
                role=ModelRole.VALIDACAO,
                size_gb=19,
                context_size=32768,
                speed="slow",
                capabilities=["deep_analysis", "verification", "research"],
                max_concurrent=1
            ),
            "mixtral": ModelConfig(
                name="mixtral-dedicated-q5:latest",
                role=ModelRole.MASTER,
                size_gb=33,
                context_size=128000,
                speed="slow",
                capabilities=["orchestration", "complex_reasoning", "synthesis"],
                max_concurrent=1
            )
        }

        # Estado do sistema
        self.active_instances: Dict[str, List[asyncio.Task]] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.results_cache: Dict[str, Any] = {}
        self.metrics = {
            "total_requests": 0,
            "by_model": {m: 0 for m in self.models},
            "avg_response_time": {},
            "errors": 0
        }

    async def call_ollama(self, model_name: str, prompt: str,
                         temperature: float = 0.7,
                         max_tokens: int = 1000) -> Dict[str, Any]:
        """Chama um modelo Ollama específico"""
        start_time = time.time()

        try:
            # Construir comando
            cmd = [
                "ollama", "run", model_name,
                "--verbose"
            ]

            # Criar processo
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Enviar prompt e receber resposta
            stdout, stderr = await proc.communicate(prompt.encode())

            response = stdout.decode().strip()
            elapsed = time.time() - start_time

            # Atualizar métricas
            self.metrics["by_model"][model_name.split(":")[0]] += 1

            return {
                "success": True,
                "response": response,
                "model": model_name,
                "time": elapsed,
                "tokens": len(response.split())
            }

        except Exception as e:
            self.metrics["errors"] += 1
            return {
                "success": False,
                "error": str(e),
                "model": model_name
            }

    async def route_task(self, task: str, context: Optional[str] = None) -> str:
        """Usa TinyLlama para rotear tarefa para modelo apropriado"""
        prompt = f"""Classify this task and select the best model:

Task: {task}

Available models and their specialties:
- phi3: Analysis, summaries, extraction
- llama3.2: Creative writing, stories, ideas
- gemma2: Code, technical, math, logic
- producermon: Polish, style, production quality
- deepseek: Deep research, verification, complex analysis
- mixtral: Complex reasoning, synthesis, orchestration

Output only the model name, nothing else."""

        result = await self.call_ollama("tinyllama:latest", prompt, temperature=0.1)

        if result["success"]:
            selected = result["response"].strip().lower()
            # Validar seleção
            for model in ["phi3", "llama3.2", "gemma2", "producermon", "deepseek", "mixtral"]:
                if model in selected:
                    return model

        # Default para phi3 se não conseguir rotear
        return "phi3"

    async def pipeline_process(self, task: str, stages: List[str]) -> Dict[str, Any]:
        """Processa tarefa através de pipeline de modelos"""
        results = []
        current_output = task

        for stage in stages:
            print(f"\n🔄 Pipeline Stage: {stage}")

            if stage == "triagem":
                model = "tinyllama"
                prompt = f"Classify and prepare: {current_output}"
            elif stage == "analise":
                model = "phi3"
                prompt = f"Analyze in detail: {current_output}"
            elif stage == "tecnico":
                model = "gemma2"
                prompt = f"Technical implementation: {current_output}"
            elif stage == "criativo":
                model = "llama3.2"
                prompt = f"Add creative elements: {current_output}"
            elif stage == "refinamento":
                model = "producermon"
                prompt = f"Polish and refine: {current_output}"
            elif stage == "validacao":
                model = "deepseek"
                prompt = f"Validate and verify: {current_output}"
            else:
                continue

            # Chamar modelo
            config = self.models[model]
            result = await self.call_ollama(config.name, prompt)

            if result["success"]:
                current_output = result["response"]
                results.append({
                    "stage": stage,
                    "model": model,
                    "output": current_output[:500],  # Preview
                    "time": result["time"]
                })
                print(f"   ✅ {stage} complete ({result['time']:.1f}s)")
            else:
                print(f"   ❌ {stage} failed: {result['error']}")

        return {
            "success": True,
            "pipeline": results,
            "final_output": current_output,
            "total_stages": len(results)
        }

    async def parallel_analysis(self, content: str, models: List[str]) -> Dict[str, Any]:
        """Análise paralela com múltiplos modelos"""
        tasks = []

        for model_key in models:
            if model_key in self.models:
                config = self.models[model_key]
                prompt = f"Analyze from {config.role.value} perspective:\n\n{content}"
                tasks.append(self.call_ollama(config.name, prompt))

        # Executar em paralelo
        results = await asyncio.gather(*tasks)

        # Combinar resultados
        analyses = {}
        for i, model_key in enumerate(models):
            if results[i]["success"]:
                analyses[model_key] = {
                    "perspective": self.models[model_key].role.value,
                    "analysis": results[i]["response"],
                    "time": results[i]["time"]
                }

        return {
            "success": True,
            "parallel_analyses": analyses,
            "models_used": len(analyses)
        }

    async def consensus_decision(self, question: str, models: List[str] = None) -> Dict[str, Any]:
        """Decisão por consenso entre múltiplos modelos"""
        if models is None:
            models = ["phi3", "gemma2", "llama3.2"]

        # Coletar votos
        votes = {}
        prompt = f"{question}\n\nAnswer with just YES or NO."

        tasks = []
        for model_key in models:
            if model_key in self.models:
                config = self.models[model_key]
                tasks.append(self.call_ollama(config.name, prompt, temperature=0.1))

        results = await asyncio.gather(*tasks)

        # Contar votos
        yes_votes = 0
        no_votes = 0

        for i, result in enumerate(results):
            if result["success"]:
                answer = result["response"].strip().upper()
                votes[models[i]] = answer
                if "YES" in answer:
                    yes_votes += 1
                elif "NO" in answer:
                    no_votes += 1

        consensus = "YES" if yes_votes > no_votes else "NO"
        confidence = max(yes_votes, no_votes) / len(models) * 100

        return {
            "success": True,
            "question": question,
            "consensus": consensus,
            "confidence": f"{confidence:.0f}%",
            "votes": votes,
            "yes_count": yes_votes,
            "no_count": no_votes
        }

    async def hierarchical_synthesis(self, topic: str) -> Dict[str, Any]:
        """Síntese hierárquica: modelos pequenos -> grandes"""
        synthesis = {}

        # Nível 1: Modelos ultra-rápidos
        print("📊 Level 1: Quick Assessment")
        tiny_result = await self.call_ollama(
            "tinyllama:latest",
            f"Quick summary of: {topic}"
        )
        synthesis["quick"] = tiny_result.get("response", "")[:200]

        # Nível 2: Modelos rápidos
        print("📊 Level 2: Detailed Analysis")
        tasks = [
            self.call_ollama("phi3:mini", f"Analyze: {topic}\nContext: {synthesis['quick']}"),
            self.call_ollama("llama3.2:3b", f"Creative perspective on: {topic}")
        ]
        level2 = await asyncio.gather(*tasks)
        synthesis["analysis"] = level2[0].get("response", "")[:500]
        synthesis["creative"] = level2[1].get("response", "")[:500]

        # Nível 3: Síntese final (modelo grande)
        print("📊 Level 3: Master Synthesis")
        final_prompt = f"""Synthesize these perspectives on '{topic}':

Quick Assessment: {synthesis['quick']}

Detailed Analysis: {synthesis['analysis']}

Creative View: {synthesis['creative']}

Provide a comprehensive synthesis."""

        # Usar modelo menor para síntese se Mixtral não estiver disponível
        master_result = await self.call_ollama(
            "gemma2:9b",  # Fallback para modelo menor
            final_prompt
        )

        synthesis["final"] = master_result.get("response", "")

        return {
            "success": True,
            "topic": topic,
            "synthesis": synthesis,
            "levels_completed": 3
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status do sistema"""
        status = {
            "models_available": len(self.models),
            "models": {},
            "metrics": self.metrics,
            "total_capacity_gb": sum(m.size_gb for m in self.models.values())
        }

        for name, config in self.models.items():
            status["models"][name] = {
                "role": config.role.value,
                "size_gb": config.size_gb,
                "context_size": config.context_size,
                "speed": config.speed,
                "capabilities": config.capabilities
            }

        return status

async def demo_multi_ollama():
    """Demonstração do sistema multi-Ollama"""
    orchestrator = OllamaOrchestrator()

    print("🚀 SISTEMA MULTI-OLLAMA ORQUESTRADO")
    print("=" * 60)

    # Status do sistema
    status = orchestrator.get_system_status()
    print(f"\n📊 Sistema com {status['models_available']} modelos")
    print(f"💾 Capacidade total: {status['total_capacity_gb']:.1f} GB\n")

    # Demo 1: Roteamento automático
    print("\n1️⃣ DEMO: Roteamento Automático")
    print("-" * 40)
    task = "Write a Python function to calculate fibonacci"
    best_model = await orchestrator.route_task(task)
    print(f"Tarefa: {task}")
    print(f"Modelo selecionado: {best_model}")

    # Demo 2: Pipeline de processamento
    print("\n2️⃣ DEMO: Pipeline de Processamento")
    print("-" * 40)
    pipeline_result = await orchestrator.pipeline_process(
        "Create a story about AI",
        ["triagem", "criativo", "refinamento"]
    )
    print(f"Pipeline completo: {pipeline_result['total_stages']} estágios")

    # Demo 3: Análise paralela
    print("\n3️⃣ DEMO: Análise Paralela")
    print("-" * 40)
    parallel_result = await orchestrator.parallel_analysis(
        "The future of artificial intelligence",
        ["phi3", "llama3.2", "gemma2"]
    )
    print(f"Análises paralelas: {parallel_result['models_used']} modelos")

    # Demo 4: Decisão por consenso
    print("\n4️⃣ DEMO: Decisão por Consenso")
    print("-" * 40)
    consensus = await orchestrator.consensus_decision(
        "Is Python the best language for AI development?"
    )
    print(f"Consenso: {consensus['consensus']} ({consensus['confidence']})")
    print(f"Votos: {consensus['votes']}")

    # Demo 5: Síntese hierárquica
    print("\n5️⃣ DEMO: Síntese Hierárquica")
    print("-" * 40)
    synthesis = await orchestrator.hierarchical_synthesis(
        "The impact of quantum computing"
    )
    print(f"Níveis completados: {synthesis['levels_completed']}")

    print("\n" + "=" * 60)
    print("✅ DEMONSTRAÇÃO COMPLETA")
    print(f"Total de requisições: {orchestrator.metrics['total_requests']}")
    print(f"Erros: {orchestrator.metrics['errors']}")

if __name__ == "__main__":
    asyncio.run(demo_multi_ollama())