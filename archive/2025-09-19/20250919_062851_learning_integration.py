"""
🎯 Learning Integration - Integração com Sistema Principal
Conecta sistemas de ML/Evolução ao ScriptDoctorSystem
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import asyncio
from dataclasses import dataclass
from src.core.unified_memory_system import get_unified_memory, MemoryType
# Auto-unified: Este arquivo foi automaticamente integrado ao sistema unificado


@dataclass
class LearningConfig:
    """Configuração do sistema de aprendizado"""
    enable_continuous_learning: bool = True
    learning_interval_minutes: int = 30
    min_confidence_threshold: float = 0.7
    max_concepts_per_model: int = 50
    evolution_generations: int = 3

class LearningIntegration:
    """
    Integra sistemas de aprendizado ao sistema principal
    Permite que ScriptDoctorSystem use conhecimento acumulado
    """

    def __init__(self):
        self.trainer = None
        self.knowledge_cache = []
        self.evolved_models = {}
        self.learning_config = LearningConfig()

    def initialize(self):
        """Inicializa sistemas de learning se disponíveis"""
        try:
            from .ollama_cinema_trainer import OllamaCinemaTrainer
            self.trainer = OllamaCinemaTrainer()
            print("✅ Cinema Trainer initialized")
            return True
        except Exception as e:
            print(f"⚠️ Learning systems not available: {e}")
            return False

    async def get_enriched_prompt(self, base_prompt: str, topic: str = None) -> str:
        """
        Enriquece prompt com conhecimento acumulado
        Usado pelo ScriptDoctorSystem para análises melhores
        """
        if not self.trainer:
            return base_prompt

        try:
            # Recuperar conhecimento relevante
            knowledge = self.trainer.get_accumulated_knowledge(
                min_confidence=self.learning_config.min_confidence_threshold
            )

            if not knowledge:
                return base_prompt

            # Filtrar por tópico se especificado
            if topic:
                relevant = [k for k in knowledge if topic.lower() in k.source.lower()]
                knowledge = relevant[:10] if relevant else knowledge[:10]
            else:
                knowledge = knowledge[:10]

            # Criar seção de conhecimento
            knowledge_section = "\n\nApply these learned concepts:\n"
            for item in knowledge:
                knowledge_section += f"- {item.concept}\n"
                if item.examples:
                    knowledge_section += f"  Example: {item.examples[0][:100]}\n"

            # Enriquecer prompt
            enriched = base_prompt + knowledge_section
            return enriched

        except Exception as e:
            print(f"⚠️ Could not enrich prompt: {e}")
            return base_prompt

    async def learn_from_analysis(self, analysis_result: Dict, screenplay_text: str):
        """
        Aprende com os resultados de uma análise
        Feedback loop para melhoria contínua
        """
        if not self.trainer or not self.learning_config.enable_continuous_learning:
            return

        try:
            # Extrair insights da análise
            insights = []

            # Extrair de debates se disponível
            if 'debates' in analysis_result:
                for debate in analysis_result['debates']:
                    if 'consensus' in debate:
                        insights.append(debate['consensus'])

            # Extrair de insights finais
            if 'final_insights' in analysis_result:
                if 'strengths' in analysis_result['final_insights']:
                    insights.extend(analysis_result['final_insights']['strengths'])
                if 'recommendations' in analysis_result['final_insights']:
                    insights.extend(analysis_result['final_insights']['recommendations'])

            # Converter insights em conhecimento
            from .ollama_cinema_trainer import CinemaKnowledge

            for insight in insights:
                if insight and len(insight) > 10:
                    knowledge = CinemaKnowledge(
                        concept=insight[:200],  # Limitar tamanho
                        source="analysis_feedback",
                        confidence=0.75,
                        examples=[screenplay_text[:500]]
                    )
                    self.knowledge_cache.append(knowledge)

            # Salvar periodicamente
            if len(self.knowledge_cache) >= 10:
                self.trainer.save_knowledge_to_memory(self.knowledge_cache)
                self.knowledge_cache = []
                print("💾 Saved learned insights to knowledge base")

        except Exception as e:
            print(f"⚠️ Could not learn from analysis: {e}")

    async def evolve_models_if_needed(self):
        """
        Evolui modelos se houver conhecimento suficiente acumulado
        """
        if not self.trainer:
            return

        try:
            knowledge = self.trainer.get_accumulated_knowledge()

            # Evoluir se tiver conhecimento suficiente
            if len(knowledge) >= self.learning_config.max_concepts_per_model:
                print("🧬 Sufficient knowledge accumulated, evolving models...")

                models_to_evolve = [
                    "scripturemon-cpu-themes",
                    "scripturemon-cpu-structure",
                    "scripturemon-cpu-dialogue"
                ]

                for model in models_to_evolve:
                    evolved = await self.trainer.evolve_model(model)
                    self.evolved_models[model] = evolved
                    print(f"  ✅ Evolved: {model}")

                return True

        except Exception as e:
            print(f"⚠️ Could not evolve models: {e}")

        return False

    def get_best_model_for_task(self, task: str) -> str:
        """
        Retorna melhor modelo para uma tarefa
        Pode ser modelo evoluído se disponível
        """
        # Mapear tarefas para modelos
        task_model_map = {
            "themes": "scripturemon-cpu-themes",
            "structure": "scripturemon-cpu-structure",
            "dialogue": "scripturemon-cpu-dialogue",
            "character": "scripturemon-cpu-dialogue",
            "pacing": "scripturemon-cpu-structure"
        }

        base_model = task_model_map.get(task.lower(), "llama3.2:3b")

        # Verificar se existe versão evoluída
        if base_model in self.evolved_models:
            return f"{base_model}_evolved"

        return base_model

    async def start_background_learning(self):
        """
        Inicia aprendizado em background
        Roda periodicamente para acumular conhecimento
        """
        if not self.trainer or not self.learning_config.enable_continuous_learning:
            return

        print("🎓 Starting background learning process...")

        while True:
            try:
                # Esperar intervalo
                await asyncio.sleep(
                    self.learning_config.learning_interval_minutes * 60
                )

                # Verificar se há documentos para aprender
                screenplays_dir = Path("data/screenplays")
                if screenplays_dir.exists():
                    txt_files = list(screenplays_dir.glob("*.txt"))

                    if txt_files:
                        # Aprender de um documento aleatório
                        import random
                        doc = random.choice(txt_files)

                        print(f"📖 Background learning from: {doc.name}")
                        await self.trainer.train_on_document(doc)

                        # Verificar se deve evoluir modelos
                        await self.evolve_models_if_needed()

            except Exception as e:
                print(f"⚠️ Background learning error: {e}")
                await asyncio.sleep(60)  # Esperar 1 min em caso de erro

# Singleton para uso global
learning_integration = LearningIntegration()

# ============================================================
# AUTO-UNIFIED MEMORY HELPER
# ============================================================
def _get_memory():
    """Helper para acesso rápido à memória unificada"""
    return get_unified_memory()

# Atalhos para compatibilidade
unified_memory = _get_memory()
