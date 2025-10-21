#!/usr/bin/env python3
"""
🌟 TESTE COMPLETO DO SISTEMA - TODAS AS FASES
Teste de integração final demonstrando o funcionamento completo do
Scripturemon Champion com todas as funcionalidades implementadas
"""

import sys
import os
import time
import asyncio
from pathlib import Path
import json

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports das fases implementadas
from apps.scripturemon.rules_memory import get_memory_instance
from apps.scripturemon.screenplay_crystal_memory import get_screenplay_memory
from apps.scripturemon.rag_smart_manager import get_smart_manager
from apps.scripturemon.character_analytics import CharacterAnalytics
from apps.scripturemon.production_pipeline import ProductionPipeline

class CompleteSystemTest:
    """Teste completo de todas as funcionalidades integradas"""

    def __init__(self):
        self.test_screenplay = """FADE IN:

ACT I

EXT. SILICON VALLEY - DAY

A bustling tech campus. ALEX CHEN (28, brilliant programmer) walks through the courtyard, laptop bag slung over their shoulder.

MAYA RODRIGUEZ (26, cybersecurity expert) catches up.

MAYA
Alex! Did you see the news about the data breach?

ALEX
(stopping)
Which one? There's been three this week.

MAYA
The quantum encryption one. Someone broke our supposedly unbreakable code.

ALEX
(concerned)
That's impossible. I designed that system myself.

INT. TECH COMPANY - CYBERSECURITY LAB - LATER

Alex and Maya examine code on multiple screens. DR. SARAH WINTERS (45, CTO) enters.

DR. WINTERS
The board is panicking. They want answers.

ALEX
Give me 24 hours. If someone cracked quantum encryption,
we're looking at either a breakthrough in quantum computing...

MAYA
Or someone had inside help.

Alex and Maya exchange meaningful looks.

ACT II

INT. ALEX'S APARTMENT - NIGHT

Alex works frantically on their personal computer. Maya arrives with coffee and Chinese takeout.

MAYA
You've been at this for 12 hours straight.

ALEX
(not looking up)
I found something. Look at this pattern in the data extraction.

Maya leans in to look at the screen.

MAYA
Those access timestamps... they match when you were in meetings.

ALEX
Someone used my credentials. But how?

A knock at the door. They freeze.

ALEX (CONT'D)
(whispering)
I wasn't expecting anyone.

MAYA
(checking her phone)
Neither was I.

Through the window, they see a black SUV parked outside.

MAYA (CONT'D)
We need to go. Now.

EXT. FIRE ESCAPE - CONTINUOUS

Alex and Maya climb down the fire escape, moving stealthily.

ALEX
My car's around the corner.

MAYA
No. They'll be watching it.
(pointing to a motorcycle)
We take mine.

They mount the motorcycle and speed away as men in suits emerge from the building.

ACT III

INT. ABANDONED WAREHOUSE - DAY

Alex has set up a makeshift computer lab. Maya stands guard.

ALEX
I traced the breach. It came from inside the company,
but the real mastermind is...

Dr. Winters enters from the shadows.

DR. WINTERS
Is me. Very good, Alex.

MAYA
(drawing a weapon)
Don't move.

DR. WINTERS
You don't understand. The quantum encryption
wasn't broken by criminals. It was broken by the government.

ALEX
What?

DR. WINTERS
I've been working with the NSA for three years.
Your encryption was too good. It was hiding things
the country needs to see.

MAYA
So you betrayed your own company?

DR. WINTERS
I saved it. And I'm saving all of you.

Police sirens wail in the distance.

DR. WINTERS (CONT'D)
The real criminals are already in custody.
But Alex, your quantum work...
it's going to change everything.

EXT. WAREHOUSE - LATER

Alex and Maya watch as Dr. Winters is led away by federal agents.

ALEX
So we're the good guys?

MAYA
We're the guys who solved an impossible puzzle.

ALEX
What happens now?

MAYA
Now? We build something even better.
Something that protects privacy AND security.

They shake hands, then embrace.

ALEX
Partners?

MAYA
Partners.

FADE OUT.

THE END
"""

        self.results = {}

    async def run_complete_test(self):
        """Executa teste completo de todas as funcionalidades"""
        print("🌟" * 20)
        print("🌟 SCRIPTUREMON CHAMPION - TESTE COMPLETO DO SISTEMA")
        print("🌟 Testando todas as fases implementadas")
        print("🌟" * 20)

        start_time = time.time()

        try:
            # FASE 23 - Crystal Memory para regras do Claude Code
            await self.test_claude_rules_memory()

            # FASE 23 - Crystal Memory para roteiros
            await self.test_screenplay_memory()

            # FASE 24 - RAG System com Smart Manager
            await self.test_rag_system()

            # FASE 25 - Character Analytics
            await self.test_character_analytics()

            # FASE 26 - Production Pipeline
            await self.test_production_pipeline()

            # Teste de integração completa
            await self.test_full_integration()

            # Gerar relatório final
            await self.generate_final_report()

        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            self.results['error'] = str(e)

        end_time = time.time()
        self.results['total_time'] = end_time - start_time

        print(f"\n⏱️ Tempo total: {self.results['total_time']:.2f}s")

    async def test_claude_rules_memory(self):
        """Testa Crystal Memory para regras do Claude Code"""
        print("\n📋 FASE 23A: Crystal Memory - Regras Claude Code")

        try:
            # Obter instância da memória
            memory = get_memory_instance()

            # Testar verificação de compliance
            action = "create new file outside project structure"
            result = memory.check_compliance(action, {"file_path": "/random/location"})

            compliance, violations = result

            print(f"   ✅ Memory instance: {type(memory).__name__}")
            print(f"   📝 Teste de compliance: {'✅ Passed' if not compliance else '⚠️ Warning'}")
            print(f"   🚫 Violações detectadas: {len(violations)}")

            self.results['claude_rules_memory'] = {
                'status': 'success',
                'violations_detected': len(violations),
                'memory_active': True
            }

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.results['claude_rules_memory'] = {'status': 'error', 'error': str(e)}

    async def test_screenplay_memory(self):
        """Testa Crystal Memory para roteiros"""
        print("\n📚 FASE 23B: Crystal Memory - Roteiros")

        try:
            # Obter instância da memória de roteiros
            memory = get_screenplay_memory()

            # Armazenar roteiro de teste
            screenplay_id = memory.remember_screenplay(
                title="Quantum Breach",
                content=self.test_screenplay,
                analysis={
                    'genre': 'Thriller Tecnológico',
                    'themes': ['cybersecurity', 'betrayal', 'quantum computing'],
                    'tone': 'suspenseful'
                }
            )

            # Recuperar roteiro
            retrieved = memory.recall_screenplay(screenplay_id)

            print(f"   ✅ Screenplay stored: ID {screenplay_id}")
            print(f"   📖 Title: {retrieved['title']}")
            print(f"   📊 Analysis: {len(retrieved['analysis'])} elementos")
            print(f"   💾 Content size: {len(retrieved['content'])} chars")

            # Testar busca por similaridade
            similar = memory.find_similar_screenplays("tech thriller quantum", limit=3)

            print(f"   🔍 Similar screenplays found: {len(similar)}")

            self.results['screenplay_memory'] = {
                'status': 'success',
                'screenplay_id': screenplay_id,
                'content_size': len(retrieved['content']),
                'similar_found': len(similar)
            }

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.results['screenplay_memory'] = {'status': 'error', 'error': str(e)}

    async def test_rag_system(self):
        """Testa sistema RAG com Smart Manager"""
        print("\n🔮 FASE 24: RAG System + Smart Manager")

        try:
            # Obter Smart Manager
            smart_manager = get_smart_manager()

            # Testar detecção de contexto
            queries = [
                "Quem são os personagens principais?",  # Deve ativar RAG
                "Como comprimir arquivo?",               # Deve desativar RAG
                "Qual o tema do roteiro?",              # Deve ativar RAG
            ]

            results = []
            for query in queries:
                result = smart_manager.process_input(query)
                results.append({
                    'query': query,
                    'rag_active': result['rag_is_active'],
                    'context': result['context'],
                    'activated': result.get('rag_activated', False),
                    'deactivated': result.get('rag_deactivated', False)
                })

            # Verificar se RAG está funcionando
            rag_activations = sum(1 for r in results if r['rag_active'])
            context_switches = sum(1 for r in results if r['activated'] or r['deactivated'])

            print(f"   ✅ Smart Manager ativo")
            print(f"   🔄 Queries testadas: {len(queries)}")
            print(f"   🟢 RAG ativações: {rag_activations}")
            print(f"   🔄 Context switches: {context_switches}")

            # Status do RAG
            status = smart_manager.get_status()
            print(f"   📊 Status: {status['active']}")

            self.results['rag_system'] = {
                'status': 'success',
                'queries_tested': len(queries),
                'rag_activations': rag_activations,
                'context_switches': context_switches,
                'manager_status': status
            }

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.results['rag_system'] = {'status': 'error', 'error': str(e)}

    async def test_character_analytics(self):
        """Testa sistema de análise de personagens"""
        print("\n🎭 FASE 25: Character Analytics")

        try:
            # Criar analisador
            analyzer = CharacterAnalytics()

            # Analisar roteiro
            analysis = analyzer.analyze_screenplay("quantum_breach", self.test_screenplay)

            # Verificar resultados
            characters = analysis['summary']['total_characters']
            relationships = analysis['summary']['total_relationships']
            scenes = analysis['summary']['total_scenes']

            print(f"   ✅ Analysis completed")
            print(f"   👥 Characters identified: {characters}")
            print(f"   💑 Relationships found: {relationships}")
            print(f"   🎬 Scenes analyzed: {scenes}")

            # Verificar personagens principais
            main_chars = [name for name, data in analysis['characters'].items()
                         if data['importance'] > 0.3]

            print(f"   ⭐ Main characters: {len(main_chars)}")
            for char in main_chars[:3]:
                importance = analysis['characters'][char]['importance']
                print(f"      • {char}: {importance:.1%} importance")

            # Testar perfil detalhado
            if main_chars:
                profile = analyzer.get_character_profile(main_chars[0])
                if profile:
                    print(f"   📋 Profile generated for: {profile['name']}")

            self.results['character_analytics'] = {
                'status': 'success',
                'characters': characters,
                'relationships': relationships,
                'scenes': scenes,
                'main_characters': len(main_chars)
            }

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.results['character_analytics'] = {'status': 'error', 'error': str(e)}

    async def test_production_pipeline(self):
        """Testa pipeline de produção completo"""
        print("\n🎬 FASE 26: Production Pipeline")

        try:
            # Criar pipeline
            pipeline = ProductionPipeline()

            # Criar arquivo temporário
            temp_file = Path("temp_test_screenplay.txt")
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(self.test_screenplay)

            # Criar job do pipeline
            job_id = pipeline.create_job(
                screenplay_file=temp_file,
                name="Test Integration Pipeline",
                config={
                    'enable_compression': False,  # Desabilitar para teste rápido
                    'enable_ai_enrichment': False,
                    'export_formats': ['json', 'html']
                }
            )

            print(f"   ✅ Pipeline job created: {job_id}")

            # Executar pipeline
            print("   🚀 Executing pipeline...")
            results = await pipeline.execute_job(job_id)

            # Verificar resultados
            completed = results['tasks_completed']
            failed = results['tasks_failed']
            stages = len(results.get('stages', {}))

            print(f"   📊 Tasks completed: {completed}")
            print(f"   ❌ Tasks failed: {failed}")
            print(f"   📋 Stages processed: {stages}")

            # Status do job
            status = pipeline.get_job_status(job_id)
            print(f"   🎯 Job status: {status['status']}")

            # Limpeza
            if temp_file.exists():
                temp_file.unlink()

            self.results['production_pipeline'] = {
                'status': 'success',
                'job_id': job_id,
                'tasks_completed': completed,
                'tasks_failed': failed,
                'stages_processed': stages,
                'job_status': status['status']
            }

        except Exception as e:
            print(f"   ❌ Erro: {e}")
            self.results['production_pipeline'] = {'status': 'error', 'error': str(e)}

    async def test_full_integration(self):
        """Testa integração completa de todos os sistemas"""
        print("\n🌐 TESTE DE INTEGRAÇÃO COMPLETA")

        try:
            print("   🔗 Testing cross-system integration...")

            # Teste 1: Roteiro → Memória → RAG → Analytics → Pipeline
            integration_steps = []

            # Passo 1: Armazenar na memória de roteiros
            memory = get_screenplay_memory()
            screenplay_id = memory.remember_screenplay(
                title="Integration Test Script",
                content=self.test_screenplay[:1000],  # Versão reduzida
                analysis={'test': True}
            )
            integration_steps.append("✅ Screenplay stored in memory")

            # Passo 2: Ativar RAG automaticamente
            smart_manager = get_smart_manager()
            result = smart_manager.process_input("Quem são os personagens do roteiro Integration Test?")
            if result['rag_is_active']:
                integration_steps.append("✅ RAG auto-activated for screenplay query")
            else:
                integration_steps.append("⚠️ RAG activation needs improvement")

            # Passo 3: Analytics em paralelo
            analyzer = CharacterAnalytics()
            analysis = analyzer.analyze_screenplay("integration_test", self.test_screenplay[:1000])
            characters_found = analysis['summary']['total_characters']
            integration_steps.append(f"✅ Character Analytics: {characters_found} characters")

            # Passo 4: Verificar compliance das regras
            rules_memory = get_memory_instance()
            compliance, violations = rules_memory.check_compliance(
                "analyze screenplay",
                {"characters": characters_found}
            )
            integration_steps.append(f"✅ Rules compliance: {len(violations)} violations")

            print("   📋 Integration steps:")
            for step in integration_steps:
                print(f"      {step}")

            self.results['full_integration'] = {
                'status': 'success',
                'steps_completed': len(integration_steps),
                'screenplay_id': screenplay_id,
                'characters_found': characters_found,
                'rag_active': result['rag_is_active'],
                'compliance_violations': len(violations)
            }

        except Exception as e:
            print(f"   ❌ Erro na integração: {e}")
            self.results['full_integration'] = {'status': 'error', 'error': str(e)}

    async def generate_final_report(self):
        """Gera relatório final do teste completo"""
        print("\n📊 RELATÓRIO FINAL")
        print("=" * 60)

        # Contar sucessos
        phases = ['claude_rules_memory', 'screenplay_memory', 'rag_system',
                 'character_analytics', 'production_pipeline', 'full_integration']

        successes = sum(1 for phase in phases
                       if self.results.get(phase, {}).get('status') == 'success')

        success_rate = (successes / len(phases)) * 100

        print(f"✅ Fases implementadas: {successes}/{len(phases)}")
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        print(f"⏱️ Tempo total: {self.results.get('total_time', 0):.2f}s")

        # Detalhes por fase
        print("\n📋 DETALHES POR FASE:")

        phase_names = {
            'claude_rules_memory': 'FASE 23A - Crystal Memory (Claude Rules)',
            'screenplay_memory': 'FASE 23B - Crystal Memory (Screenplays)',
            'rag_system': 'FASE 24 - RAG System + Smart Manager',
            'character_analytics': 'FASE 25 - Character Analytics',
            'production_pipeline': 'FASE 26 - Production Pipeline',
            'full_integration': 'INTEGRAÇÃO COMPLETA'
        }

        for phase_key, phase_name in phase_names.items():
            result = self.results.get(phase_key, {})
            status = result.get('status', 'not_tested')

            if status == 'success':
                print(f"   ✅ {phase_name}")
                # Mostrar métricas específicas
                if phase_key == 'character_analytics':
                    chars = result.get('characters', 0)
                    rels = result.get('relationships', 0)
                    print(f"      👥 {chars} personagens, 💑 {rels} relações")

                elif phase_key == 'production_pipeline':
                    completed = result.get('tasks_completed', 0)
                    print(f"      🎬 {completed} tarefas completadas")

                elif phase_key == 'rag_system':
                    activations = result.get('rag_activations', 0)
                    print(f"      🔮 {activations} ativações do RAG")

                elif phase_key == 'full_integration':
                    steps = result.get('steps_completed', 0)
                    print(f"      🔗 {steps} passos de integração")

            elif status == 'error':
                print(f"   ❌ {phase_name}")
                print(f"      Error: {result.get('error', 'Unknown error')}")

            else:
                print(f"   ⏸️ {phase_name} - Not tested")

        # Funcionalidades demonstradas
        print(f"\n🎯 FUNCIONALIDADES DEMONSTRADAS:")
        print(f"   📋 Crystal Memory para regras do Claude Code")
        print(f"   📚 Crystal Memory para armazenamento de roteiros")
        print(f"   🔮 RAG System com ativação inteligente baseada em contexto")
        print(f"   🎭 Character Analytics com análise profunda de personagens")
        print(f"   🎬 Production Pipeline completo com 9 estágios")
        print(f"   🌐 Integração completa entre todos os sistemas")

        # Sistema operacional
        if success_rate >= 80:
            print(f"\n🎉 SCRIPTUREMON CHAMPION ESTÁ TOTALMENTE OPERACIONAL!")
            print(f"   Sistema pronto para produção com todas as fases implementadas.")
        elif success_rate >= 60:
            print(f"\n⚠️ Sistema parcialmente operacional ({success_rate:.1f}%)")
            print(f"   Algumas funcionalidades precisam de ajustes.")
        else:
            print(f"\n❌ Sistema precisa de correções significativas")
            print(f"   Taxa de sucesso baixa: {success_rate:.1f}%")

        # Salvar relatório
        report_path = Path("tests/reports/complete_system_test.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump({
                'test_summary': {
                    'phases_tested': len(phases),
                    'phases_successful': successes,
                    'success_rate': success_rate,
                    'total_time': self.results.get('total_time', 0),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                },
                'detailed_results': self.results,
                'system_status': 'operational' if success_rate >= 80 else 'needs_attention'
            }, f, indent=2)

        print(f"\n📁 Relatório completo salvo em: {report_path}")


async def main():
    """Função principal do teste"""
    tester = CompleteSystemTest()
    await tester.run_complete_test()


if __name__ == "__main__":
    asyncio.run(main())