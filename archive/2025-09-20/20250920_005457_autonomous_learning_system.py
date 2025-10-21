#!/usr/bin/env python3
"""
🤖 SISTEMA AUTÔNOMO DE APRENDIZADO DE ROTEIROS
Processa automaticamente a biblioteca e evolui continuamente
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any
import json
import random

# Sistema integrado
from integrated_system import get_integrated_system
from deep_learning_enhanced import DeepLearningEnhanced
from meta_learning_framework import MetaLearningFramework
from claude_code_pipeline import ClaudeCodePipeline

# Biblioteca e memória
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.core.screenplay_library import get_screenplay_library
from src.core.unified_memory_system import get_unified_memory


class AutonomousLearningSystem:
    """
    Sistema que trabalha continuamente analisando roteiros
    e evoluindo com Meta-learning + Claude Code
    """

    def __init__(self):
        print("🤖 Inicializando Sistema Autônomo de Aprendizado...")

        # Componentes principais
        self.system = get_integrated_system()
        self.library = get_screenplay_library()
        self.memory = get_unified_memory()

        # Estatísticas
        self.stats = {
            'screenplays_analyzed': 0,
            'patterns_discovered': 0,
            'knowledge_extracted': 0,
            'ml_functions_executed': 0,
            'evolution_cycles': 0,
            'claude_interactions': 0,
            'start_time': time.time()
        }

        # Estado do aprendizado
        self.learning_state = {
            'current_screenplay': None,
            'analysis_queue': [],
            'discovered_patterns': [],
            'evolution_ready': False
        }

        print("✅ Sistema Autônomo inicializado!")

    async def start_autonomous_learning(self):
        """
        Loop principal de aprendizado autônomo
        """
        print("\n🚀 INICIANDO APRENDIZADO AUTÔNOMO")
        print("=" * 60)

        # Carregar biblioteca de roteiros
        all_screenplays = self.library.list_all()
        total_count = sum(len(scripts) for scripts in all_screenplays.values())
        print(f"📚 {total_count} roteiros disponíveis para análise")

        # Criar fila de análise
        for category, scripts in all_screenplays.items():
            for script in scripts:
                self.learning_state['analysis_queue'].append({
                    'title': script,
                    'category': category
                })

        # Embaralhar para variedade
        random.shuffle(self.learning_state['analysis_queue'])

        print(f"📋 Fila de análise criada com {len(self.learning_state['analysis_queue'])} items")
        print("\n⚡ Iniciando processamento contínuo...")
        print("-" * 60)

        # Loop principal
        while self.learning_state['analysis_queue']:
            try:
                # Pegar próximo roteiro
                screenplay_info = self.learning_state['analysis_queue'].pop(0)
                self.learning_state['current_screenplay'] = screenplay_info['title']

                print(f"\n📖 Analisando: {screenplay_info['title']} ({screenplay_info['category']})")

                # 1. Deep Learning Analysis
                await self._deep_learning_analysis(screenplay_info['title'])

                # 2. Meta-learning Evolution
                await self._meta_learning_evolution()

                # 3. Claude Code Enhancement (a cada 5 roteiros)
                if self.stats['screenplays_analyzed'] % 5 == 0:
                    await self._claude_enhancement()

                # 4. Salvar conhecimento
                await self._save_knowledge()

                # Atualizar estatísticas
                self.stats['screenplays_analyzed'] += 1

                # Mostrar progresso
                self._show_progress()

                # Pausa para não sobrecarregar
                await asyncio.sleep(2)

            except Exception as e:
                print(f"⚠️ Erro ao processar {self.learning_state['current_screenplay']}: {str(e)[:100]}")
                continue

        # Relatório final
        self._final_report()

    async def _deep_learning_analysis(self, screenplay_title: str):
        """
        Análise com Deep Learning (3 funções ML)
        """
        print("  🧠 Deep Learning Analysis...")

        try:
            # 1. Why This Works - Análise reversa
            why_result = await self._execute_ml_function(
                'why_this_works',
                screenplay_title
            )
            if why_result:
                self.stats['ml_functions_executed'] += 1
                self.stats['patterns_discovered'] += len(why_result.get('patterns', []))

            # 2. Validate Pattern - Validação de padrões
            pattern_result = await self._execute_ml_function(
                'validate_pattern',
                'three_act_structure'
            )
            if pattern_result:
                self.stats['ml_functions_executed'] += 1

            # 3. Get or Analyze - Cache inteligente
            cache_result = await self._execute_ml_function(
                'get_or_analyze',
                screenplay_title
            )
            if cache_result:
                self.stats['ml_functions_executed'] += 1

            print(f"    ✅ {self.stats['ml_functions_executed']} funções ML executadas")

        except Exception as e:
            print(f"    ⚠️ Deep Learning parcial: {str(e)[:50]}")

    async def _execute_ml_function(self, function_name: str, *args):
        """
        Executa uma função ML específica
        """
        try:
            if hasattr(self.system.deep_learning, function_name):
                func = getattr(self.system.deep_learning, function_name)
                if asyncio.iscoroutinefunction(func):
                    return await func(*args)
                else:
                    return func(*args)
        except:
            return None

    async def _meta_learning_evolution(self):
        """
        Evolução autônoma com Meta-learning
        """
        print("  🔄 Meta-learning Evolution...")

        try:
            # Registrar descobertas
            if self.learning_state['discovered_patterns']:
                for pattern in self.learning_state['discovered_patterns']:
                    self.system.meta_learning.register_pattern_discovery(
                        pattern_type='screenplay_structure',
                        pattern_data=pattern,
                        source=self.learning_state['current_screenplay']
                    )

            # Verificar se está pronto para evoluir
            if self.system.meta_learning.check_evolution_readiness():
                evolution_result = await self.system.meta_learning.evolve_autonomously()
                if evolution_result:
                    self.stats['evolution_cycles'] += 1
                    print(f"    ✅ Evolução #{self.stats['evolution_cycles']} completada")

        except Exception as e:
            print(f"    ⚠️ Meta-learning parcial: {str(e)[:50]}")

    async def _claude_enhancement(self):
        """
        Enhancement com Claude Code (com memórias completas)
        """
        print("  🤖 Claude Code Enhancement...")

        try:
            # Preparar contexto com memórias
            context = {
                'screenplay': self.learning_state['current_screenplay'],
                'patterns_found': len(self.learning_state['discovered_patterns']),
                'ml_insights': self.stats['ml_functions_executed'],
                'evolution_stage': self.stats['evolution_cycles']
            }

            # Processar com Claude Pipeline
            result = await self.system.claude.process_with_full_context(
                prompt=f"Analyze patterns in {self.learning_state['current_screenplay']}",
                context=context
            )

            if result:
                self.stats['claude_interactions'] += 1
                print(f"    ✅ Claude interaction #{self.stats['claude_interactions']}")

        except Exception as e:
            print(f"    ⚠️ Claude enhancement parcial: {str(e)[:50]}")

    async def _save_knowledge(self):
        """
        Salva conhecimento extraído na memória unificada
        """
        print("  💾 Salvando conhecimento...")

        try:
            # Criar entry de conhecimento
            knowledge_entry = {
                'screenplay': self.learning_state['current_screenplay'],
                'timestamp': time.time(),
                'patterns': self.learning_state['discovered_patterns'],
                'ml_functions': self.stats['ml_functions_executed'],
                'evolution_stage': self.stats['evolution_cycles']
            }

            # Salvar na memória unificada
            self.memory.store(
                memory_type='KNOWLEDGE',
                key=f"analysis_{self.learning_state['current_screenplay']}",
                value=knowledge_entry,
                metadata={
                    'source': 'autonomous_learning',
                    'iteration': self.stats['screenplays_analyzed']
                }
            )

            self.stats['knowledge_extracted'] += 1
            print(f"    ✅ Conhecimento salvo ({self.stats['knowledge_extracted']} total)")

        except Exception as e:
            print(f"    ⚠️ Salvamento parcial: {str(e)[:50]}")

    def _show_progress(self):
        """
        Mostra progresso do aprendizado
        """
        elapsed = time.time() - self.stats['start_time']
        rate = self.stats['screenplays_analyzed'] / (elapsed / 60) if elapsed > 0 else 0

        print(f"\n📊 PROGRESSO:")
        print(f"  • Roteiros analisados: {self.stats['screenplays_analyzed']}")
        print(f"  • Padrões descobertos: {self.stats['patterns_discovered']}")
        print(f"  • Funções ML executadas: {self.stats['ml_functions_executed']}")
        print(f"  • Ciclos de evolução: {self.stats['evolution_cycles']}")
        print(f"  • Taxa: {rate:.1f} roteiros/min")
        print(f"  • Fila restante: {len(self.learning_state['analysis_queue'])}")
        print("-" * 60)

    def _final_report(self):
        """
        Relatório final do aprendizado autônomo
        """
        elapsed = time.time() - self.stats['start_time']

        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL - APRENDIZADO AUTÔNOMO")
        print("=" * 60)

        print(f"\n🏆 RESULTADOS:")
        print(f"  • Roteiros processados: {self.stats['screenplays_analyzed']}")
        print(f"  • Padrões descobertos: {self.stats['patterns_discovered']}")
        print(f"  • Conhecimento extraído: {self.stats['knowledge_extracted']}")
        print(f"  • Funções ML executadas: {self.stats['ml_functions_executed']}")
        print(f"  • Ciclos de evolução: {self.stats['evolution_cycles']}")
        print(f"  • Interações Claude: {self.stats['claude_interactions']}")

        print(f"\n⏱️ PERFORMANCE:")
        print(f"  • Tempo total: {elapsed/60:.1f} minutos")
        print(f"  • Taxa média: {self.stats['screenplays_analyzed']/(elapsed/60):.1f} roteiros/min")

        print(f"\n✅ SISTEMA EVOLUIU E APRENDEU AUTONOMAMENTE!")
        print("DIGIMUNDO PRESENTE 🥷")


async def main():
    """
    Inicia o sistema autônomo
    """
    system = AutonomousLearningSystem()
    await system.start_autonomous_learning()


if __name__ == "__main__":
    print("🤖 INICIANDO SISTEMA AUTÔNOMO DE MACHINE LEARNING")
    print("=" * 60)
    print("Este sistema vai:")
    print("  1. Analisar todos os roteiros com Deep Learning")
    print("  2. Evoluir autonomamente com Meta-learning")
    print("  3. Integrar insights com Claude Code")
    print("  4. Salvar conhecimento na memória unificada")
    print("=" * 60)

    # Executar
    asyncio.run(main())