#!/usr/bin/env python3
"""
🌌 DIGIMUNDO ORCHESTRATOR - Maestro de Inteligências Artificiais
Sistema que detecta, analisa e coordena múltiplas IAs
"""

import asyncio
import subprocess
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import concurrent.futures
import re

# ========== CLASSES DE DADOS ==========

@dataclass
class AIModel:
    """Representa um modelo de IA disponível"""
    name: str
    size_gb: float
    family: str  # llama, mistral, etc
    capabilities: List[str] = field(default_factory=list)
    speed_score: float = 0.0  # 0-10
    intelligence_score: float = 0.0  # 0-10
    creativity_score: float = 0.0  # 0-10
    specialty: str = "general"
    last_used: Optional[datetime] = None
    response_times: List[float] = field(default_factory=list)
    
    @property
    def avg_response_time(self) -> float:
        """Tempo médio de resposta"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

@dataclass
class AITask:
    """Representa uma tarefa para IA"""
    id: str
    type: str  # reasoning, creative, analysis, code, etc
    prompt: str
    context: Dict[str, Any]
    priority: int = 5  # 1-10
    created_at: datetime = field(default_factory=datetime.now)

# ========== ORQUESTRADOR DE IAs ==========

class AIOrchestrator:
    """Coordena múltiplas IAs para tarefas complexas"""
    
    def __init__(self):
        self.available_models: Dict[str, AIModel] = {}
        self.model_profiles = self._init_model_profiles()
        self.task_queue: List[AITask] = []
        self.results_cache = {}
        self.ollama_base = "http://localhost:11434"
        
    def _init_model_profiles(self) -> Dict:
        """Perfis conhecidos de modelos"""
        return {
            # Família Llama
            "llama3.2": {
                "family": "llama",
                "size": 2.0,
                "speed": 9,
                "intelligence": 7,
                "creativity": 6,
                "specialty": "general",
                "capabilities": ["reasoning", "conversation", "analysis"]
            },
            "llama3.1:70b": {
                "family": "llama",
                "size": 40.0,
                "speed": 3,
                "intelligence": 10,
                "creativity": 8,
                "specialty": "complex_reasoning",
                "capabilities": ["deep_analysis", "philosophy", "complex_reasoning", "creativity"]
            },
            "llama3.1:8b": {
                "family": "llama", 
                "size": 4.7,
                "speed": 7,
                "intelligence": 8,
                "creativity": 7,
                "specialty": "balanced",
                "capabilities": ["reasoning", "analysis", "conversation", "code"]
            },
            # Família Mistral
            "mistral": {
                "family": "mistral",
                "size": 4.1,
                "speed": 8,
                "intelligence": 7,
                "creativity": 8,
                "specialty": "creative",
                "capabilities": ["creative_writing", "brainstorming", "conversation"]
            },
            "mixtral:8x7b": {
                "family": "mistral",
                "size": 26.0,
                "speed": 5,
                "intelligence": 9,
                "creativity": 9,
                "specialty": "expert_reasoning",
                "capabilities": ["expert_analysis", "multi_domain", "complex_reasoning"]
            },
            # Outros
            "phi3": {
                "family": "microsoft",
                "size": 2.3,
                "speed": 10,
                "intelligence": 6,
                "creativity": 5,
                "specialty": "efficient",
                "capabilities": ["quick_responses", "basic_reasoning"]
            },
            "gemma": {
                "family": "google",
                "size": 4.8,
                "speed": 8,
                "intelligence": 7,
                "creativity": 6,
                "specialty": "analytical",
                "capabilities": ["analysis", "factual", "structured_thinking"]
            },
            "deepseek-coder": {
                "family": "deepseek",
                "size": 6.7,
                "speed": 7,
                "intelligence": 8,
                "creativity": 5,
                "specialty": "coding",
                "capabilities": ["code_generation", "debugging", "technical"]
            }
        }
    
    async def discover_models(self) -> Dict[str, AIModel]:
        """Descobre todos os modelos disponíveis"""
        print("🔍 Descobrindo modelos de IA disponíveis...")
        
        try:
            result = subprocess.run(['ollama', 'list'], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print("❌ Erro ao listar modelos")
                return {}
            
            # Parse da saída
            lines = result.stdout.strip().split('\n')
            if len(lines) <= 1:
                print("📭 Nenhum modelo encontrado")
                return {}
            
            # Processar cada modelo
            for line in lines[1:]:  # Pular cabeçalho
                parts = line.split()
                if len(parts) >= 2:
                    model_name = parts[0].strip()
                    
                    # Extrair nome base (sem tags)
                    base_name = model_name.split(':')[0]
                    
                    # Buscar perfil conhecido
                    profile = self.model_profiles.get(base_name, {})
                    
                    # Criar objeto AIModel
                    model = AIModel(
                        name=model_name,
                        size_gb=profile.get("size", 1.0),
                        family=profile.get("family", "unknown"),
                        capabilities=profile.get("capabilities", ["general"]),
                        speed_score=profile.get("speed", 5),
                        intelligence_score=profile.get("intelligence", 5),
                        creativity_score=profile.get("creativity", 5),
                        specialty=profile.get("specialty", "general")
                    )
                    
                    self.available_models[model_name] = model
            
            print(f"✅ {len(self.available_models)} modelos descobertos")
            return self.available_models
            
        except Exception as e:
            print(f"❌ Erro ao descobrir modelos: {e}")
            return {}
    
    async def analyze_model_capabilities(self, model_name: str) -> Dict:
        """Analisa as capacidades de um modelo através de testes"""
        print(f"\n🧪 Analisando capacidades de {model_name}...")
        
        model = self.available_models.get(model_name)
        if not model:
            return {}
        
        # Testes de capacidade
        tests = [
            {
                "type": "reasoning",
                "prompt": "Se todos os bloops são bleeps, e alguns bleeps são blups, podemos afirmar que alguns bloops são blups? Explique seu raciocínio.",
                "evaluate": lambda r: len(r) > 50 and any(word in r.lower() for word in ["não", "no", "cannot", "false"])
            },
            {
                "type": "creativity", 
                "prompt": "Invente uma palavra nova e defina seu significado de forma poética.",
                "evaluate": lambda r: len(r) > 30 and not any(word in r.lower() for word in ["erro", "error", "desculpe", "sorry"])
            },
            {
                "type": "speed",
                "prompt": "Responda com uma palavra: Sim ou Não?",
                "evaluate": lambda r: len(r) < 50
            }
        ]
        
        results = {}
        
        for test in tests:
            start_time = time.time()
            
            try:
                response = await self._query_model(model_name, test["prompt"], timeout=30)
                elapsed = time.time() - start_time
                
                # Avaliar resposta
                success = test["evaluate"](response) if response else False
                
                results[test["type"]] = {
                    "success": success,
                    "time": elapsed,
                    "response_length": len(response) if response else 0
                }
                
                # Atualizar scores do modelo
                if test["type"] == "speed":
                    model.response_times.append(elapsed)
                    # Score de velocidade (inverso do tempo)
                    model.speed_score = min(10, 10 / (elapsed + 0.1))
                
            except Exception as e:
                results[test["type"]] = {
                    "success": False,
                    "error": str(e)
                }
        
        return results
    
    async def _query_model(self, model_name: str, prompt: str, timeout: int = 30) -> Optional[str]:
        """Consulta um modelo específico"""
        try:
            result = subprocess.run(
                ['ollama', 'run', model_name, prompt],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ {model_name} excedeu tempo limite")
            return None
        except Exception as e:
            print(f"❌ Erro ao consultar {model_name}: {e}")
            return None
    
    def select_best_model_for_task(self, task_type: str) -> Optional[str]:
        """Seleciona o melhor modelo para um tipo de tarefa"""
        if not self.available_models:
            return None
        
        # Pontuação por tipo de tarefa
        task_weights = {
            "reasoning": {"intelligence": 0.7, "speed": 0.3},
            "creative": {"creativity": 0.7, "intelligence": 0.3},
            "quick": {"speed": 0.9, "intelligence": 0.1},
            "analysis": {"intelligence": 0.6, "speed": 0.4},
            "philosophy": {"intelligence": 0.5, "creativity": 0.5},
            "code": {"intelligence": 0.8, "speed": 0.2}
        }
        
        weights = task_weights.get(task_type, {"intelligence": 0.5, "speed": 0.5})
        
        best_model = None
        best_score = -1
        
        for name, model in self.available_models.items():
            # Calcular score ponderado
            score = 0
            if "intelligence" in weights:
                score += model.intelligence_score * weights["intelligence"]
            if "creativity" in weights:
                score += model.creativity_score * weights.get("creativity", 0)
            if "speed" in weights:
                score += model.speed_score * weights["speed"]
            
            # Bonus por especialidade
            if task_type in model.capabilities:
                score *= 1.2
            
            if score > best_score:
                best_score = score
                best_model = name
        
        return best_model
    
    async def coordinate_models_for_complex_task(self, task: str, approach: str = "consensus") -> Dict:
        """Coordena múltiplos modelos para uma tarefa complexa"""
        print(f"\n🎭 Coordenando múltiplas IAs para: {task[:50]}...")
        
        results = {}
        
        if approach == "consensus":
            # Abordagem: Todos os modelos respondem e buscamos consenso
            responses = {}
            
            # Consultar top 3 modelos
            top_models = sorted(
                self.available_models.items(),
                key=lambda x: x[1].intelligence_score,
                reverse=True
            )[:3]
            
            for model_name, model in top_models:
                print(f"  🤖 Consultando {model_name}...")
                response = await self._query_model(model_name, task)
                if response:
                    responses[model_name] = response
            
            # Sintetizar consenso
            if len(responses) >= 2:
                consensus_prompt = f"""Analise estas respostas de diferentes IAs e crie uma síntese:

{chr(10).join([f"{name}: {resp[:200]}..." for name, resp in responses.items()])}

Crie uma resposta unificada que capture os melhores insights de cada uma."""
                
                # Usar o modelo mais inteligente para sintetizar
                synthesizer = self.select_best_model_for_task("analysis")
                if synthesizer:
                    consensus = await self._query_model(synthesizer, consensus_prompt)
                    results["consensus"] = consensus
                    results["contributors"] = list(responses.keys())
                    results["individual_responses"] = responses
            
        elif approach == "specialist":
            # Abordagem: Diferentes modelos para diferentes partes
            # Dividir tarefa em componentes
            components = self._decompose_task(task)
            
            for component in components:
                specialist = self.select_best_model_for_task(component["type"])
                if specialist:
                    response = await self._query_model(specialist, component["prompt"])
                    results[component["type"]] = {
                        "model": specialist,
                        "response": response
                    }
        
        elif approach == "chain":
            # Abordagem: Cadeia de raciocínio entre modelos
            chain_prompts = [
                ("analysis", f"Analise esta questão: {task}"),
                ("creative", "Baseado na análise anterior, proponha soluções criativas"),
                ("reasoning", "Avalie criticamente as soluções propostas")
            ]
            
            previous_response = ""
            chain_results = []
            
            for task_type, prompt in chain_prompts:
                model = self.select_best_model_for_task(task_type)
                if model:
                    full_prompt = f"{prompt}\n\nContexto anterior: {previous_response[-500:]}" if previous_response else prompt
                    response = await self._query_model(model, full_prompt)
                    if response:
                        chain_results.append({
                            "stage": task_type,
                            "model": model,
                            "response": response
                        })
                        previous_response = response
            
            results["chain"] = chain_results
        
        return results
    
    def _decompose_task(self, task: str) -> List[Dict]:
        """Decompõe uma tarefa complexa em componentes"""
        # Análise simples baseada em palavras-chave
        components = []
        
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["analise", "analyze", "explique", "explain"]):
            components.append({
                "type": "analysis",
                "prompt": f"Faça uma análise detalhada de: {task}"
            })
        
        if any(word in task_lower for word in ["crie", "create", "imagine", "invente"]):
            components.append({
                "type": "creative",
                "prompt": f"Seja criativo com: {task}"
            })
        
        if any(word in task_lower for word in ["código", "code", "programa", "implement"]):
            components.append({
                "type": "code",
                "prompt": f"Implemente: {task}"
            })
        
        # Se não identificou componentes, usar análise geral
        if not components:
            components.append({
                "type": "reasoning",
                "prompt": task
            })
        
        return components
    
    def get_orchestra_status(self) -> Dict:
        """Status completo da orquestra de IAs"""
        status = {
            "total_models": len(self.available_models),
            "models_by_family": {},
            "models_by_specialty": {},
            "performance_rankings": {},
            "recommendations": []
        }
        
        # Agrupar por família
        for model in self.available_models.values():
            family = model.family
            if family not in status["models_by_family"]:
                status["models_by_family"][family] = []
            status["models_by_family"][family].append(model.name)
        
        # Agrupar por especialidade
        for model in self.available_models.values():
            specialty = model.specialty
            if specialty not in status["models_by_specialty"]:
                status["models_by_specialty"][specialty] = []
            status["models_by_specialty"][specialty].append(model.name)
        
        # Rankings
        rankings = {
            "speed": sorted(self.available_models.items(), 
                          key=lambda x: x[1].speed_score, reverse=True),
            "intelligence": sorted(self.available_models.items(),
                                 key=lambda x: x[1].intelligence_score, reverse=True),
            "creativity": sorted(self.available_models.items(),
                               key=lambda x: x[1].creativity_score, reverse=True)
        }
        
        for category, ranked_models in rankings.items():
            status["performance_rankings"][category] = [
                {"model": name, "score": getattr(model, f"{category}_score")}
                for name, model in ranked_models[:3]
            ]
        
        # Recomendações
        if len(self.available_models) < 3:
            status["recommendations"].append(
                "Instale mais modelos para melhor coordenação. Sugestão: ollama pull mixtral:8x7b"
            )
        
        if not any(m.size_gb > 20 for m in self.available_models.values()):
            status["recommendations"].append(
                "Considere instalar um modelo grande (>20GB) para tarefas complexas"
            )
        
        return status

# ========== SISTEMA DIGIMUNDO COM ORQUESTRADOR ==========

class DigimundoOrchestrator:
    """Digimundo com capacidade de orquestrar múltiplas IAs"""
    
    def __init__(self):
        self.orchestrator = AIOrchestrator()
        self.conversation_history = []
        self.model_performance = {}
        
    async def initialize(self):
        """Inicializa o sistema orquestrador"""
        print("\n" + "="*60)
        print("🌌 DIGIMUNDO AI ORCHESTRATOR - INICIALIZANDO")
        print("="*60)
        
        # Descobrir modelos
        await self.orchestrator.discover_models()
        
        # Analisar capacidades básicas
        print("\n📊 Analisando capacidades dos modelos...")
        for model_name in list(self.orchestrator.available_models.keys())[:3]:  # Top 3
            await self.orchestrator.analyze_model_capabilities(model_name)
        
        print("\n✨ Sistema Orquestrador pronto!")
        print("="*60)
    
    async def interactive_loop(self):
        """Loop interativo com comandos de orquestração"""
        print("\n📋 COMANDOS DO ORQUESTRADOR:")
        print("  /modelos        - Listar todos os modelos disponíveis")
        print("  /analisar       - Analisar capacidades dos modelos")
        print("  /status         - Status da orquestra de IAs")
        print("  /perguntar [pergunta] - Pergunta simples (melhor modelo)")
        print("  /consenso [pergunta]  - Buscar consenso entre modelos")
        print("  /cadeia [pergunta]    - Cadeia de raciocínio")
        print("  /especialista [tarefa] - Usar especialistas")
        print("  /comparar [pergunta]  - Comparar respostas de todos")
        print("  /sair           - Encerrar")
        
        while True:
            try:
                command = input("\n🎭 > ").strip()
                
                if command == "/sair":
                    print("👋 Encerrando orquestrador...")
                    break
                
                elif command == "/modelos":
                    await self._show_models()
                
                elif command == "/analisar":
                    await self._analyze_all_models()
                
                elif command == "/status":
                    self._show_orchestra_status()
                
                elif command.startswith("/perguntar"):
                    question = command[10:].strip()
                    if question:
                        await self._ask_best_model(question)
                    else:
                        print("❌ Uso: /perguntar [sua pergunta]")
                
                elif command.startswith("/consenso"):
                    question = command[9:].strip()
                    if question:
                        await self._seek_consensus(question)
                    else:
                        print("❌ Uso: /consenso [sua pergunta]")
                
                elif command.startswith("/cadeia"):
                    question = command[7:].strip()
                    if question:
                        await self._chain_reasoning(question)
                    else:
                        print("❌ Uso: /cadeia [sua pergunta]")
                
                elif command.startswith("/especialista"):
                    task = command[13:].strip()
                    if task:
                        await self._use_specialists(task)
                    else:
                        print("❌ Uso: /especialista [tarefa complexa]")
                
                elif command.startswith("/comparar"):
                    question = command[9:].strip()
                    if question:
                        await self._compare_all_models(question)
                    else:
                        print("❌ Uso: /comparar [pergunta]")
                
                else:
                    if command:
                        print("❌ Comando não reconhecido")
                
            except KeyboardInterrupt:
                print("\n👋 Encerrando...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    async def _show_models(self):
        """Mostra todos os modelos disponíveis"""
        print("\n" + "="*60)
        print("🤖 MODELOS DE IA DISPONÍVEIS")
        print("="*60)
        
        for name, model in self.orchestrator.available_models.items():
            print(f"\n📦 {name}")
            print(f"   Família: {model.family}")
            print(f"   Tamanho: {model.size_gb}GB")
            print(f"   Especialidade: {model.specialty}")
            print(f"   Capacidades: {', '.join(model.capabilities)}")
            print(f"   Scores: Vel={model.speed_score:.1f} Int={model.intelligence_score:.1f} Cri={model.creativity_score:.1f}")
            
            if model.response_times:
                print(f"   Tempo médio: {model.avg_response_time:.1f}s")
    
    async def _analyze_all_models(self):
        """Analisa todos os modelos disponíveis"""
        print("\n🔬 Analisando todos os modelos...")
        
        for model_name in self.orchestrator.available_models:
            results = await self.orchestrator.analyze_model_capabilities(model_name)
            
            print(f"\n{model_name}:")
            for test_type, result in results.items():
                if result.get("success"):
                    print(f"   ✅ {test_type}: {result['time']:.1f}s")
                else:
                    print(f"   ❌ {test_type}: falhou")
    
    def _show_orchestra_status(self):
        """Mostra status da orquestra"""
        status = self.orchestrator.get_orchestra_status()
        
        print("\n" + "="*60)
        print("🎭 STATUS DA ORQUESTRA DE IAs")
        print("="*60)
        
        print(f"\n📊 Total de modelos: {status['total_models']}")
        
        print("\n👨‍👩‍👧‍👦 Por família:")
        for family, models in status["models_by_family"].items():
            print(f"   {family}: {', '.join(models)}")
        
        print("\n🎯 Por especialidade:")
        for specialty, models in status["models_by_specialty"].items():
            print(f"   {specialty}: {', '.join(models)}")
        
        print("\n🏆 Rankings de performance:")
        for category, rankings in status["performance_rankings"].items():
            print(f"\n   {category.upper()}:")
            for i, item in enumerate(rankings, 1):
                print(f"   {i}. {item['model']} (score: {item['score']:.1f})")
        
        if status["recommendations"]:
            print("\n💡 Recomendações:")
            for rec in status["recommendations"]:
                print(f"   • {rec}")
    
    async def _ask_best_model(self, question: str):
        """Pergunta ao melhor modelo para a tarefa"""
        # Determinar tipo de tarefa
        task_type = "reasoning"  # Default
        
        if any(word in question.lower() for word in ["crie", "invente", "imagine"]):
            task_type = "creative"
        elif any(word in question.lower() for word in ["rápido", "quick", "simples"]):
            task_type = "quick"
        elif any(word in question.lower() for word in ["código", "code", "programa"]):
            task_type = "code"
        
        # Selecionar modelo
        best_model = self.orchestrator.select_best_model_for_task(task_type)
        
        if not best_model:
            print("❌ Nenhum modelo adequado encontrado")
            return
        
        print(f"\n🤖 Usando {best_model} (melhor para {task_type})")
        print("💭 Processando...")
        
        start_time = time.time()
        response = await self.orchestrator._query_model(best_model, question)
        elapsed = time.time() - start_time
        
        if response:
            print(f"\n💬 Resposta ({elapsed:.1f}s):")
            print(response)
        else:
            print("❌ Erro ao obter resposta")
    
    async def _seek_consensus(self, question: str):
        """Busca consenso entre múltiplos modelos"""
        print("\n🤝 Buscando consenso entre múltiplas IAs...")
        
        results = await self.orchestrator.coordinate_models_for_complex_task(
            question, approach="consensus"
        )
        
        if "consensus" in results:
            print(f"\n🎯 CONSENSO (baseado em {len(results['contributors'])} modelos):")
            print(results["consensus"])
            
            print(f"\n👥 Contribuíram: {', '.join(results['contributors'])}")
            
            if input("\n💭 Ver respostas individuais? (s/n): ").lower() == 's':
                for model, response in results["individual_responses"].items():
                    print(f"\n{model}:")
                    print(response[:200] + "..." if len(response) > 200 else response)
        else:
            print("❌ Não foi possível obter consenso")
    
    async def _chain_reasoning(self, question: str):
        """Executa cadeia de raciocínio entre modelos"""
        print("\n⛓️ Iniciando cadeia de raciocínio...")
        
        results = await self.orchestrator.coordinate_models_for_complex_task(
            question, approach="chain"
        )
        
        if "chain" in results:
            print("\n🔗 CADEIA DE RACIOCÍNIO:")
            for i, stage in enumerate(results["chain"], 1):
                print(f"\n{i}. {stage['stage'].upper()} ({stage['model']}):")
                print(stage['response'][:300] + "..." if len(stage['response']) > 300 else stage['response'])
        else:
            print("❌ Erro na cadeia de raciocínio")
    
    async def _use_specialists(self, task: str):
        """Usa especialistas para diferentes aspectos da tarefa"""
        print("\n🎓 Convocando especialistas...")
        
        results = await self.orchestrator.coordinate_models_for_complex_task(
            task, approach="specialist"
        )
        
        if results:
            print("\n📚 ANÁLISE POR ESPECIALISTAS:")
            for component_type, result in results.items():
                if isinstance(result, dict) and "model" in result:
                    print(f"\n{component_type.upper()} - {result['model']}:")
                    print(result['response'][:300] + "..." if len(result['response']) > 300 else result['response'])
        else:
            print("❌ Erro ao consultar especialistas")
    
    async def _compare_all_models(self, question: str):
        """Compara respostas de todos os modelos"""
        print(f"\n🔄 Comparando respostas de {len(self.orchestrator.available_models)} modelos...")
        
        responses = {}
        times = {}
        
        for model_name in self.orchestrator.available_models:
            print(f"   Consultando {model_name}...")
            start_time = time.time()
            response = await self.orchestrator._query_model(model_name, question, timeout=20)
            elapsed = time.time() - start_time
            
            if response:
                responses[model_name] = response
                times[model_name] = elapsed
        
        # Mostrar resultados
        print(f"\n📊 COMPARAÇÃO ({len(responses)} respostas):")
        
        # Ordenar por tempo de resposta
        sorted_by_time = sorted(times.items(), key=lambda x: x[1])
        
        for model_name, response_time in sorted_by_time:
            print(f"\n🤖 {model_name} ({response_time:.1f}s):")
            response = responses[model_name]
            print(response[:200] + "..." if len(response) > 200 else response)
        
        # Análise
        if len(responses) > 1:
            print("\n📈 ANÁLISE:")
            print(f"   Mais rápido: {sorted_by_time[0][0]} ({sorted_by_time[0][1]:.1f}s)")
            print(f"   Mais lento: {sorted_by_time[-1][0]} ({sorted_by_time[-1][1]:.1f}s)")
            
            # Resposta mais longa/curta
            sorted_by_length = sorted(responses.items(), key=lambda x: len(x[1]))
            print(f"   Mais conciso: {sorted_by_length[0][0]} ({len(sorted_by_length[0][1])} chars)")
            print(f"   Mais detalhado: {sorted_by_length[-1][0]} ({len(sorted_by_length[-1][1])} chars)")

# ========== EXECUÇÃO PRINCIPAL ==========

async def main():
    """Função principal"""
    system = DigimundoOrchestrator()
    
    try:
        await system.initialize()
        await system.interactive_loop()
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🌌 Orquestrador encerrado.")

if __name__ == "__main__":
    asyncio.run(main())
