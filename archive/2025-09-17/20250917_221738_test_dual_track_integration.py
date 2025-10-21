#!/usr/bin/env python3
"""
🎯 TESTE DE INTEGRAÇÃO DUAL-TRACK
Valida execução paralela GPU+CPU sem conflitos
Mac Studio M3 Ultra - 96GB RAM - 28 cores
"""

import asyncio
import time
import psutil
import threading
from typing import Dict, List
import json
from datetime import datetime

# Adiciona path do projeto
import sys
sys.path.insert(0, '/Users/clubproducoes/Digimundo/scripturemon-champion')

from apps.scripturemon.dual_track_orchestrator import (
    DualTrackOrchestrator,
    MultiPerspectiveOrchestrator,
    CoreAllocation
)

class DualTrackTester:
    """Testa integração e paralelismo do sistema dual-track"""

    def __init__(self):
        self.orchestrator = DualTrackOrchestrator()
        self.multi_orchestrator = MultiPerspectiveOrchestrator()
        self.results = []

    async def test_parallel_execution(self):
        """Testa se GPU e CPU rodam realmente em paralelo"""

        print("\n🔬 TESTE 1: Execução Paralela GPU + CPU")
        print("-" * 50)

        test_text = """
        The story begins in a small town where nothing ever happens,
        until a mysterious stranger arrives with a secret that will
        change everything. The townspeople are skeptical at first,
        but soon realize that their quiet lives are about to be
        transformed forever. This is a tale of redemption, courage,
        and the power of community in the face of adversity.
        """

        # Monitora recursos antes
        cpu_before = psutil.cpu_percent(interval=0.1)
        mem_before = psutil.virtual_memory().percent

        print(f"📊 Recursos antes:")
        print(f"   CPU: {cpu_before:.1f}%")
        print(f"   RAM: {mem_before:.1f}%")

        # Executa análise dual-track
        start = time.time()
        result = await self.orchestrator.analyze_screenplay(test_text, mode='dual')
        total_time = time.time() - start

        # Monitora recursos depois
        cpu_after = psutil.cpu_percent(interval=0.1)
        mem_after = psutil.virtual_memory().percent

        print(f"\n📊 Recursos durante:")
        print(f"   CPU: {cpu_after:.1f}%")
        print(f"   RAM: {mem_after:.1f}%")

        # Valida paralelismo
        gpu_time = result['tracks']['gpu'].time_taken if 'gpu' in result['tracks'] else 0
        cpu_time = result['tracks']['cpu'].time_taken if 'cpu' in result['tracks'] else 0
        sequential_time = gpu_time + cpu_time

        print(f"\n⏱️  Tempos de execução:")
        print(f"   GPU track: {gpu_time:.1f}s")
        print(f"   CPU track: {cpu_time:.1f}s")
        print(f"   Total real: {total_time:.1f}s")
        print(f"   Sequential seria: {sequential_time:.1f}s")
        print(f"   Economia: {sequential_time - total_time:.1f}s")

        # Verifica se realmente rodou em paralelo
        parallelism_ratio = total_time / sequential_time if sequential_time > 0 else 1
        is_parallel = parallelism_ratio < 0.8  # 80% do tempo sequential = paralelo

        if is_parallel:
            print("✅ PARALELO CONFIRMADO!")
        else:
            print("⚠️  Execução não foi totalmente paralela")

        self.results.append({
            'test': 'parallel_execution',
            'passed': is_parallel,
            'parallelism_ratio': parallelism_ratio,
            'time_saved': sequential_time - total_time
        })

        return is_parallel

    async def test_resource_allocation(self):
        """Testa se alocação de cores funciona corretamente"""

        print("\n🔬 TESTE 2: Alocação de Cores")
        print("-" * 50)

        allocator = CoreAllocation()

        # Testa alocação básica
        cores_gpu = allocator.allocate('llama3.2:3b')
        print(f"✓ Alocou {cores_gpu} cores para llama3.2:3b")

        cores_cpu = allocator.allocate('scripturemon-cpu')
        print(f"✓ Alocou {cores_cpu} cores para scripturemon-cpu")

        # Verifica cores disponíveis
        print(f"📊 Cores disponíveis: {allocator.available_cores}/{allocator.TOTAL_CORES}")

        # Tenta alocar mais do que disponível
        can_allocate_more = allocator.can_allocate('qwen2.5:14b')
        print(f"🔍 Pode alocar qwen2.5:14b? {can_allocate_more}")

        # Libera recursos
        allocator.release('llama3.2:3b')
        allocator.release('scripturemon-cpu')
        print(f"✓ Recursos liberados")
        print(f"📊 Cores disponíveis: {allocator.available_cores}/{allocator.TOTAL_CORES}")

        self.results.append({
            'test': 'resource_allocation',
            'passed': cores_gpu and cores_cpu and allocator.available_cores > 0
        })

        return True

    async def test_mode_variations(self):
        """Testa diferentes modos de execução"""

        print("\n🔬 TESTE 3: Modos de Execução")
        print("-" * 50)

        test_text = "A simple test scene for mode validation."
        modes_tested = []

        # Teste modo fast (só GPU)
        print("\n📌 Modo FAST:")
        start = time.time()
        result = await self.orchestrator.analyze_screenplay(test_text, mode='fast')
        fast_time = time.time() - start
        print(f"   Tempo: {fast_time:.1f}s")
        print(f"   Tracks: {list(result['tracks'].keys())}")
        modes_tested.append(('fast', fast_time, 'gpu' in result['tracks']))

        # Teste modo dual (GPU + CPU)
        print("\n📌 Modo DUAL:")
        start = time.time()
        result = await self.orchestrator.analyze_screenplay(test_text, mode='dual')
        dual_time = time.time() - start
        print(f"   Tempo: {dual_time:.1f}s")
        print(f"   Tracks: {list(result['tracks'].keys())}")
        has_both = 'gpu' in result['tracks'] and 'cpu' in result['tracks']
        modes_tested.append(('dual', dual_time, has_both))

        # Teste modo deep (foco em CPU)
        print("\n📌 Modo DEEP:")
        start = time.time()
        result = await self.orchestrator.analyze_screenplay(test_text, mode='deep')
        deep_time = time.time() - start
        print(f"   Tempo: {deep_time:.1f}s")
        print(f"   Tracks: {list(result['tracks'].keys())}")
        modes_tested.append(('deep', deep_time, 'cpu' in result['tracks']))

        # Valida todos os modos
        all_passed = all(passed for _, _, passed in modes_tested)

        self.results.append({
            'test': 'mode_variations',
            'passed': all_passed,
            'modes': modes_tested
        })

        return all_passed

    async def test_multi_perspective(self):
        """Testa análise multi-perspectiva com variantes CPU"""

        print("\n🔬 TESTE 4: Multi-Perspectiva CPU")
        print("-" * 50)

        test_text = """
        The mirror shattered into a thousand pieces, each reflecting
        a different version of herself. Which one was real? Which one
        was the lie she'd been living all these years?
        """

        print("🎭 Iniciando análise multi-perspectiva...")
        start = time.time()

        try:
            result = await self.multi_orchestrator.analyze_multi_perspective(test_text)
            total_time = time.time() - start

            print(f"\n📊 Resultados:")
            print(f"   Tempo total: {total_time:.1f}s")
            print(f"   GPU context: {result['gpu_context'].time_taken:.1f}s")

            if 'perspectives' in result:
                print(f"   Perspectivas CPU: {len(result['perspectives'])}")
                for p in result['perspectives']:
                    print(f"      • {p.model}: {p.time_taken:.1f}s")

            passed = 'synthesis' in result and result['synthesis']
            print(f"\n{'✅' if passed else '❌'} Multi-perspectiva concluída")

        except Exception as e:
            print(f"❌ Erro: {e}")
            passed = False

        self.results.append({
            'test': 'multi_perspective',
            'passed': passed,
            'time': total_time if 'total_time' in locals() else 0
        })

        return passed

    async def test_stress_parallel(self):
        """Teste de stress com múltiplas análises paralelas"""

        print("\n🔬 TESTE 5: Stress Test Paralelo")
        print("-" * 50)

        # Múltiplos textos para análise
        test_texts = [
            "Scene 1: A dark alley at midnight.",
            "Scene 2: The protagonist faces their fears.",
            "Scene 3: A revelation changes everything.",
        ]

        print(f"🚀 Analisando {len(test_texts)} cenas em paralelo...")

        # Monitora recursos
        cpu_start = psutil.cpu_percent(interval=0.1)
        mem_start = psutil.virtual_memory().percent

        # Executa todas em paralelo
        start = time.time()
        tasks = [
            self.orchestrator.analyze_screenplay(text, mode='fast')
            for text in test_texts
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start

        # Monitora recursos finais
        cpu_end = psutil.cpu_percent(interval=0.1)
        mem_end = psutil.virtual_memory().percent

        # Conta sucessos
        successes = sum(1 for r in results if not isinstance(r, Exception))

        print(f"\n📊 Resultados:")
        print(f"   Análises bem-sucedidas: {successes}/{len(test_texts)}")
        print(f"   Tempo total: {total_time:.1f}s")
        print(f"   Tempo médio: {total_time/len(test_texts):.1f}s por análise")
        print(f"   CPU: {cpu_start:.1f}% → {cpu_end:.1f}%")
        print(f"   RAM: {mem_start:.1f}% → {mem_end:.1f}%")

        passed = successes == len(test_texts)

        self.results.append({
            'test': 'stress_parallel',
            'passed': passed,
            'successes': successes,
            'total': len(test_texts)
        })

        return passed

    def generate_report(self):
        """Gera relatório final dos testes"""

        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL - TESTES DUAL-TRACK")
        print("=" * 60)

        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['passed'])

        for result in self.results:
            status = "✅" if result['passed'] else "❌"
            print(f"{status} {result['test']}")

            # Detalhes específicos por teste
            if 'parallelism_ratio' in result:
                print(f"   Paralelismo: {result['parallelism_ratio']:.2f}")
                print(f"   Tempo economizado: {result['time_saved']:.1f}s")
            elif 'modes' in result:
                for mode, time, ok in result['modes']:
                    print(f"   {mode}: {time:.1f}s {'✓' if ok else '✗'}")
            elif 'successes' in result:
                print(f"   Taxa sucesso: {result['successes']}/{result['total']}")

        print("\n" + "-" * 60)
        print(f"📈 RESULTADO GERAL: {passed_tests}/{total_tests} testes passaram")

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        if success_rate == 100:
            print("🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Sistema dual-track funcionando perfeitamente!")
        elif success_rate >= 80:
            print("🟢 Sistema funcional com pequenos ajustes necessários")
        elif success_rate >= 60:
            print("🟡 Sistema parcialmente funcional, requer atenção")
        else:
            print("🔴 Sistema precisa de correções significativas")

        # Salva relatório
        report_file = f"/tmp/dual_track_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results,
                'summary': {
                    'total': total_tests,
                    'passed': passed_tests,
                    'success_rate': success_rate
                }
            }, f, indent=2, default=str)

        print(f"\n📁 Relatório salvo em: {report_file}")

async def main():
    """Executa suite completa de testes"""

    print("🚀 INICIANDO TESTES DE INTEGRAÇÃO DUAL-TRACK")
    print("Mac Studio M3 Ultra - 96GB RAM - 28 cores")
    print("=" * 60)

    tester = DualTrackTester()

    # Executa todos os testes
    tests = [
        tester.test_resource_allocation(),
        tester.test_mode_variations(),
        tester.test_parallel_execution(),
        tester.test_multi_perspective(),
        tester.test_stress_parallel(),
    ]

    # Executa sequencialmente para não sobrecarregar
    for test in tests:
        try:
            await test
        except Exception as e:
            print(f"❌ Erro no teste: {e}")

    # Gera relatório
    tester.generate_report()

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("DIGIMUNDO PRESENTE")

if __name__ == "__main__":
    asyncio.run(main())