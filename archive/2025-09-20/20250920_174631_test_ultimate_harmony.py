#!/usr/bin/env python3
"""
Ultimate Harmony Test Suite - Bateria Completa de Testes
Testa todo o ecossistema funcionando em harmonia
"""

import asyncio
import json
import time
import psutil
import hashlib
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import concurrent.futures
import sys
import os

# Adicionar path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.unified_manager import UnifiedMemoryManager
from apps.scripturemon.crystal_memory import CrystalMemoryManager, MemoryLayer
from apps.scripturemon.telepathic_network_advanced import TelepathicNetworkAdvanced, NetworkTopology, MessageType
from apps.scripturemon.digilang_v26_mega_multilayer import DigiLangV26MegaMultiLayer
from apps.scripturemon.soulos import SoulOS, SyscallType
from apps.scripturemon.soulpack_crdt import SoulpackCRDT
from apps.scripturemon.sdl_consolidator import SDLConsolidator
from apps.scripturemon.digilang_bytecode import DigiLangBytecode
from apps.scripturemon.multi_model_orchestrator import MultiModelOrchestrator, TaskType
from apps.scripturemon.digimons_specialized import DigimonSquad, DigimonType
from apps.scripturemon.rag_revolutionary import RAGRevolutionary, EmbeddingModel, RetrievalStrategy
from apps.scripturemon.fitness_evolution import EvolutionEngine, ScriptFitnessEvaluator


@dataclass
class TestResult:
    """Resultado de um teste"""
    test_name: str
    passed: bool
    duration_ms: int
    cpu_usage_percent: float
    memory_usage_mb: float
    details: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


@dataclass
class HarmonyReport:
    """Relatório de harmonia do sistema"""
    timestamp: float
    total_tests: int
    passed_tests: int
    failed_tests: int
    harmony_score: float
    cpu_peak_percent: float
    memory_peak_mb: float
    total_duration_seconds: float
    test_results: List[TestResult]
    ecosystem_health: Dict
    recommendations: List[str]


class SystemMonitor:
    """Monitor de recursos do sistema"""

    def __init__(self):
        self.process = psutil.Process()
        self.cpu_samples = []
        self.memory_samples = []
        self.monitoring = False

    def start_monitoring(self):
        """Inicia monitoramento em thread separada"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()

    def stop_monitoring(self):
        """Para monitoramento"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()

    def _monitor_loop(self):
        """Loop de monitoramento"""
        while self.monitoring:
            try:
                # CPU
                cpu_percent = self.process.cpu_percent(interval=0.1)
                self.cpu_samples.append(cpu_percent)

                # Memory
                memory_info = self.process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                self.memory_samples.append(memory_mb)

                time.sleep(0.5)
            except:
                pass

    def get_stats(self) -> Dict:
        """Retorna estatísticas coletadas"""
        return {
            'cpu_current': self.cpu_samples[-1] if self.cpu_samples else 0,
            'cpu_average': sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0,
            'cpu_peak': max(self.cpu_samples) if self.cpu_samples else 0,
            'memory_current_mb': self.memory_samples[-1] if self.memory_samples else 0,
            'memory_average_mb': sum(self.memory_samples) / len(self.memory_samples) if self.memory_samples else 0,
            'memory_peak_mb': max(self.memory_samples) if self.memory_samples else 0,
            'samples_collected': len(self.cpu_samples)
        }


class UltimateHarmonyTester:
    """Testador supremo de harmonia do ecossistema"""

    def __init__(self):
        self.monitor = SystemMonitor()
        self.test_results: List[TestResult] = []
        self.soul_id = f"harmony_soul_{int(time.time())}"

    async def run_all_tests(self) -> HarmonyReport:
        """Executa todos os testes de harmonia"""
        print("=" * 80)
        print("🌟 ULTIMATE HARMONY TEST SUITE - ECOSSISTEMA COMPLETO")
        print("=" * 80)

        self.monitor.start_monitoring()
        start_time = time.time()

        try:
            # FASE 1: Testes de Memória
            print("\n📦 FASE 1: SISTEMA DE MEMÓRIA CRYSTAL")
            await self.test_crystal_memory_layers()
            await self.test_memory_persistence()
            await self.test_memory_promotion()

            # FASE 2: Testes de Comunicação
            print("\n📡 FASE 2: REDE TELEPÁTICA")
            await self.test_telepathic_network()
            await self.test_quantum_channels()
            await self.test_consensus_protocol()

            # FASE 3: Testes de Processamento
            print("\n⚡ FASE 3: PROCESSAMENTO E LINGUAGEM")
            await self.test_digilang_compression()
            await self.test_digilang_bytecode()
            await self.test_soulos_syscalls()

            # FASE 4: Testes de Versionamento
            print("\n🔄 FASE 4: VERSIONAMENTO E SINCRONIZAÇÃO")
            await self.test_soulpack_crdt()
            await self.test_sdl_consolidation()

            # FASE 5: Testes de IA
            print("\n🤖 FASE 5: INTELIGÊNCIA ARTIFICIAL")
            await self.test_multi_model_orchestration()
            await self.test_digimon_squad()
            await self.test_rag_system()

            # FASE 6: Testes de Evolução
            print("\n🧬 FASE 6: EVOLUÇÃO E OTIMIZAÇÃO")
            await self.test_fitness_evolution()

            # FASE 7: Testes de Integração
            print("\n🔗 FASE 7: INTEGRAÇÃO DO ECOSSISTEMA")
            await self.test_ecosystem_communication()
            await self.test_full_pipeline_stress()
            await self.test_memory_under_load()

            # FASE 8: Testes de Performance
            print("\n⚡ FASE 8: PERFORMANCE E RECURSOS")
            await self.test_cpu_optimization()
            await self.test_concurrent_operations()

        finally:
            self.monitor.stop_monitoring()

        # Gera relatório
        duration = time.time() - start_time
        stats = self.monitor.get_stats()

        passed = len([r for r in self.test_results if r.passed])
        failed = len([r for r in self.test_results if not r.passed])

        harmony_score = self._calculate_harmony_score()
        ecosystem_health = self._assess_ecosystem_health()
        recommendations = self._generate_recommendations()

        report = HarmonyReport(
            timestamp=time.time(),
            total_tests=len(self.test_results),
            passed_tests=passed,
            failed_tests=failed,
            harmony_score=harmony_score,
            cpu_peak_percent=stats['cpu_peak'],
            memory_peak_mb=stats['memory_peak_mb'],
            total_duration_seconds=duration,
            test_results=self.test_results,
            ecosystem_health=ecosystem_health,
            recommendations=recommendations
        )

        # Salva relatório
        self._save_report(report)

        return report

    async def test_crystal_memory_layers(self):
        """Testa as 4 camadas de memória crystal"""
        start = time.time()
        cpu_start = psutil.Process().cpu_percent()

        try:
            manager = CrystalMemoryManager(self.soul_id)

            # Testa cada camada
            test_data = {
                MemoryLayer.L1_CORE: ("DNA fundamental", 1.0, 1),
                MemoryLayer.L2_CONSOLIDATED: ("Conhecimento consolidado", 0.8, 10),
                MemoryLayer.L3_ACTIVE: ("Memória ativa", 0.5, 50),
                MemoryLayer.L4_QUANTUM: ("Estado quântico", 0.3, 20)
            }

            total_stored = 0
            for layer, (content_base, importance, count) in test_data.items():
                for i in range(count):
                    content = f"{content_base} {i}"
                    memory_id = manager.store(content, layer, importance)
                    if memory_id:
                        total_stored += 1

            # Testa recall
            memories = manager.recall("fundamental", max_results=5)

            # Testa promoção
            manager.promote_memories()

            stats = manager.get_statistics()

            passed = total_stored > 0 and len(memories) > 0

            self.test_results.append(TestResult(
                test_name="crystal_memory_layers",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent() - cpu_start,
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'memories_stored': total_stored,
                    'memories_recalled': len(memories),
                    'stats': stats
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="crystal_memory_layers",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_memory_persistence(self):
        """Testa persistência de memória"""
        start = time.time()

        try:
            # Cria e persiste
            manager1 = CrystalMemoryManager(f"{self.soul_id}_persist")
            test_content = "Memória crítica persistente"
            memory_id = manager1.store(test_content, MemoryLayer.L2_CONSOLIDATED, 0.9)

            # Recria e recupera
            manager2 = CrystalMemoryManager(f"{self.soul_id}_persist")
            memories = manager2.recall("crítica", max_results=1)

            passed = len(memories) > 0 and "crítica" in memories[0].content

            self.test_results.append(TestResult(
                test_name="memory_persistence",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'persisted': memory_id, 'recovered': len(memories)}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="memory_persistence",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_memory_promotion(self):
        """Testa promoção automática de memórias"""
        start = time.time()

        try:
            manager = CrystalMemoryManager(f"{self.soul_id}_promote")

            # Adiciona memórias com diferentes importâncias
            for i in range(20):
                importance = 0.1 + (i * 0.04)  # 0.1 a 0.9
                manager.store(f"Memory {i}", MemoryLayer.L4_QUANTUM, importance)

            # Promove memórias
            manager.promote_memories()

            stats = manager.get_statistics()

            self.test_results.append(TestResult(
                test_name="memory_promotion",
                passed=True,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'memories_promoted': stats}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="memory_promotion",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_telepathic_network(self):
        """Testa rede telepática avançada"""
        start = time.time()

        try:
            network = TelepathicNetworkAdvanced(
                soul_id=f"{self.soul_id}_telepathy",
                port=19999,
                topology=NetworkTopology.HYBRID
            )

            network.start_server()
            await asyncio.sleep(0.5)

            # Envia mensagens
            message = network.broadcast("Test telepathic message", MessageType.BROADCAST)

            # Para servidor
            network.stop_server()

            passed = message is not None and message.id != ""

            self.test_results.append(TestResult(
                test_name="telepathic_network",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'message_sent': message.id if message else None}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="telepathic_network",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_quantum_channels(self):
        """Testa canais quânticos"""
        start = time.time()

        try:
            network = TelepathicNetworkAdvanced(
                soul_id=f"{self.soul_id}_quantum",
                port=19998
            )

            # Adiciona peer simulado primeiro
            from apps.scripturemon.telepathic_network_advanced import NetworkNode
            fake_peer = NetworkNode(
                soul_id="peer_soul",
                address="127.0.0.1",
                port=19997,
                capabilities=["quantum"],
                last_seen=time.time()
            )
            network.nodes["peer_soul"] = fake_peer

            # Agora estabelece canal quântico
            channel = network.establish_quantum_channel("peer_soul")

            passed = channel is not None

            self.test_results.append(TestResult(
                test_name="quantum_channels",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'channel_created': passed}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="quantum_channels",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_consensus_protocol(self):
        """Testa protocolo de consenso"""
        start = time.time()

        try:
            network = TelepathicNetworkAdvanced(
                soul_id=f"{self.soul_id}_consensus",
                port=19997
            )

            # Proposta
            proposal_id = network.consensus.propose(
                "test_proposal",
                "Should we upgrade?",
                network.soul_id
            )

            # Votos
            network.consensus.vote(proposal_id, "soul1", True, 1.0)
            network.consensus.vote(proposal_id, "soul2", True, 0.8)
            network.consensus.vote(proposal_id, "soul3", False, 0.5)

            # Resultado
            result = network.consensus.tally(proposal_id)

            passed = result is not None

            self.test_results.append(TestResult(
                test_name="consensus_protocol",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'consensus_reached': result}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="consensus_protocol",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_digilang_compression(self):
        """Testa compressão DigiLang"""
        start = time.time()

        try:
            digilang = DigiLangV26MegaMultiLayer()

            # Texto para comprimir
            original = "FADE IN: INT. OFFICE - DAY\nJohn enters the room." * 10

            # Comprime
            result = digilang.compress(original)
            if isinstance(result, tuple):
                compressed, layers, _ = result
                # Descomprime passando as layers
                decompressed = digilang.decompress(compressed, layers)
            else:
                compressed = result
                decompressed = digilang.decompress(compressed)

            # Calcula taxa
            compression_rate = (1 - len(compressed) / len(original)) * 100

            # IMPORTANTE: Não usar strip() que pode remover espaços importantes
            passed = decompressed == original and compression_rate > 10

            self.test_results.append(TestResult(
                test_name="digilang_compression",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'original_size': len(original),
                    'compressed_size': len(compressed),
                    'compression_rate': compression_rate
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="digilang_compression",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_digilang_bytecode(self):
        """Testa DigiLang++ Bytecode"""
        start = time.time()

        try:
            bytecode = DigiLangBytecode()

            code = """
            push 10
            push 20
            +
            print
            """

            result = bytecode.compile_and_run(code)

            passed = result is not None

            self.test_results.append(TestResult(
                test_name="digilang_bytecode",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'bytecode_executed': passed}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="digilang_bytecode",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_soulos_syscalls(self):
        """Testa syscalls do SoulOS"""
        start = time.time()

        try:
            soulos = SoulOS(self.soul_id)

            # Executa syscalls
            result1 = soulos.execute("[MEMO.SAVE] test_memory")
            result2 = soulos.execute("[QUERY.SELF]")
            result3 = soulos.execute("[EVOLVE.TRIGGER]")

            passed = all([
                result1['success'],
                result2['success'],
                result3['success']
            ])

            self.test_results.append(TestResult(
                test_name="soulos_syscalls",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'syscalls_executed': 3}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="soulos_syscalls",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_soulpack_crdt(self):
        """Testa CRDT sem conflitos"""
        start = time.time()

        try:
            # Dois soulpacks
            pack1 = SoulpackCRDT("soul1")
            pack2 = SoulpackCRDT("soul2")

            # Operações paralelas com timestamp
            pack1.state.add("item1", {"data": "from_soul1"}, time.time())
            pack2.state.add("item2", {"data": "from_soul2"}, time.time())

            # Remove em um
            pack1.state.remove("item1", time.time())

            # Merge sem conflitos
            merged = pack1.merge_with(pack2)

            passed = "item2" in merged.state.elements

            self.test_results.append(TestResult(
                test_name="soulpack_crdt",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'merge_successful': passed}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="soulpack_crdt",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_sdl_consolidation(self):
        """Testa consolidação SDL"""
        start = time.time()

        try:
            consolidator = SDLConsolidator(self.soul_id)

            # Consolida memórias
            memories = [
                {"content": "Memory 1", "importance": 0.8},
                {"content": "Memory 2", "importance": 0.6},
                {"content": "Memory 3", "importance": 0.9}
            ]

            report = consolidator.consolidate_memories(memories)

            passed = report.qa_pairs_generated > 0

            self.test_results.append(TestResult(
                test_name="sdl_consolidation",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'qa_pairs': report.qa_pairs_generated,
                    'patterns': report.patterns_extracted
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="sdl_consolidation",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_multi_model_orchestration(self):
        """Testa orquestração multi-modelo"""
        start = time.time()

        try:
            orchestrator = MultiModelOrchestrator()

            response = await orchestrator.orchestrate(
                prompt="How to write better code?",
                task_type=TaskType.CODING,
                strategy="consensus"
            )

            passed = len(response.models_used) > 0 and response.consensus_score > 0

            self.test_results.append(TestResult(
                test_name="multi_model_orchestration",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'models_used': len(response.models_used),
                    'consensus_score': response.consensus_score
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="multi_model_orchestration",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_digimon_squad(self):
        """Testa squad de Digimons"""
        start = time.time()

        try:
            squad = DigimonSquad()

            screenplay = "FADE IN: INT. OFFICE - DAY\n\nJOHN enters the room.\n\nJOHN\nHello world!\n\nFADE OUT."

            analysis = await squad.analyze_screenplay(
                screenplay,
                [DigimonType.AGUMON, DigimonType.GABUMON]
            )

            passed = analysis is not None and analysis.consensus_score > 0

            self.test_results.append(TestResult(
                test_name="digimon_squad",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'consensus_score': analysis.consensus_score,
                    'harmony': analysis.squad_harmony
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="digimon_squad",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_rag_system(self):
        """Testa sistema RAG"""
        start = time.time()

        try:
            rag = RAGRevolutionary(
                embedding_model=EmbeddingModel.HYBRID,
                db_path="data/test_harmony_rag.db"
            )

            # Adiciona documentos
            rag.add_document("The hero's journey begins.", "test", 0.9, 1)
            rag.add_document("Character development is key.", "test", 0.8, 2)

            # Query
            result = rag.query(
                "How to write characters?",
                k=2,
                strategy=RetrievalStrategy.HYBRID
            )

            passed = len(result.documents) > 0

            self.test_results.append(TestResult(
                test_name="rag_system",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'documents_retrieved': len(result.documents),
                    'retrieval_time': result.retrieval_time_ms
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="rag_system",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_fitness_evolution(self):
        """Testa evolução com fitness"""
        start = time.time()

        try:
            evaluator = ScriptFitnessEvaluator()
            engine = EvolutionEngine(evaluator, population_size=10)

            engine.initialize_population()
            best = engine.evolve(generations=3)

            passed = best.total_fitness > 0

            self.test_results.append(TestResult(
                test_name="fitness_evolution",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'best_fitness': best.total_fitness,
                    'generation': best.generation
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="fitness_evolution",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_ecosystem_communication(self):
        """Testa comunicação entre componentes"""
        start = time.time()

        try:
            # Cria componentes
            memory = CrystalMemoryManager(f"{self.soul_id}_eco")
            soulos = SoulOS(f"{self.soul_id}_eco")
            digilang = DigiLangV26MegaMultiLayer()

            # Fluxo de dados
            data = "Test ecosystem data"

            # 1. Comprime com DigiLang
            result = digilang.compress(data)
            compressed = result[0] if isinstance(result, tuple) else result

            # 2. Salva na memória via SoulOS
            soulos.execute(f"[MEMO.SAVE] {compressed[:20]}")

            # 3. Armazena na Crystal Memory
            memory_id = memory.store(compressed, MemoryLayer.L2_CONSOLIDATED)

            # 4. Recupera
            memories = memory.recall("Test", max_results=1)

            passed = memory_id is not None

            self.test_results.append(TestResult(
                test_name="ecosystem_communication",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={'data_flow_complete': passed}
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="ecosystem_communication",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_full_pipeline_stress(self):
        """Teste de stress do pipeline completo"""
        start = time.time()

        try:
            operations = 100
            success_count = 0

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []

                for i in range(operations):
                    future = executor.submit(self._stress_operation, i)
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        success_count += 1

            success_rate = success_count / operations
            passed = success_rate > 0.8

            self.test_results.append(TestResult(
                test_name="full_pipeline_stress",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'operations': operations,
                    'success_rate': success_rate
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="full_pipeline_stress",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    def _stress_operation(self, index: int) -> bool:
        """Operação individual de stress"""
        try:
            # Simula operação complexa
            manager = UnifiedMemoryManager('data')
            context = manager.get_context(f"stress_test_{index}")
            return context is not None
        except:
            return False

    async def test_memory_under_load(self):
        """Testa memória sob carga"""
        start = time.time()

        try:
            manager = CrystalMemoryManager(f"{self.soul_id}_load")

            # Adiciona muitas memórias
            for i in range(1000):
                manager.store(
                    f"Memory {i} with some content",
                    MemoryLayer.L3_ACTIVE,
                    importance=0.5
                )

            # Testa recall sob carga
            memories = manager.recall("Memory", max_results=10)

            # Verifica uso de memória
            memory_mb = psutil.Process().memory_info().rss / 1024 / 1024

            passed = len(memories) > 0 and memory_mb < 500  # Menos de 500MB

            self.test_results.append(TestResult(
                test_name="memory_under_load",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=memory_mb,
                details={
                    'memories_stored': 1000,
                    'memory_usage_mb': memory_mb
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="memory_under_load",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_cpu_optimization(self):
        """Testa otimização de CPU"""
        start = time.time()
        cpu_samples = []

        try:
            # Operações intensivas
            for _ in range(10):
                digilang = DigiLangV26MegaMultiLayer()
                text = "Test text" * 100
                result = digilang.compress(text)
                if isinstance(result, tuple):
                    compressed, layers, _ = result
                    decompressed = digilang.decompress(compressed, layers)
                else:
                    compressed = result
                    decompressed = digilang.decompress(compressed)

                # Amostra CPU
                cpu_samples.append(psutil.Process().cpu_percent())
                await asyncio.sleep(0.1)

            avg_cpu = sum(cpu_samples) / len(cpu_samples)
            passed = avg_cpu < 80  # CPU médio menor que 80%

            self.test_results.append(TestResult(
                test_name="cpu_optimization",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=avg_cpu,
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'avg_cpu_percent': avg_cpu,
                    'peak_cpu_percent': max(cpu_samples)
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="cpu_optimization",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def test_concurrent_operations(self):
        """Testa operações concorrentes"""
        start = time.time()

        try:
            tasks = []

            # Cria tarefas concorrentes
            tasks.append(self._async_memory_op())
            tasks.append(self._async_digilang_op())
            tasks.append(self._async_soulos_op())

            # Executa concorrentemente
            results = await asyncio.gather(*tasks, return_exceptions=True)

            success_count = sum(1 for r in results if r is True)
            passed = success_count == len(tasks)

            self.test_results.append(TestResult(
                test_name="concurrent_operations",
                passed=passed,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=psutil.Process().cpu_percent(),
                memory_usage_mb=psutil.Process().memory_info().rss / 1024 / 1024,
                details={
                    'concurrent_tasks': len(tasks),
                    'successful': success_count
                }
            ))

        except Exception as e:
            self.test_results.append(TestResult(
                test_name="concurrent_operations",
                passed=False,
                duration_ms=int((time.time() - start) * 1000),
                cpu_usage_percent=0,
                memory_usage_mb=0,
                errors=[str(e)]
            ))

    async def _async_memory_op(self) -> bool:
        """Operação assíncrona de memória"""
        try:
            manager = CrystalMemoryManager(f"{self.soul_id}_async1")
            manager.store("Async memory", MemoryLayer.L3_ACTIVE)
            return True
        except:
            return False

    async def _async_digilang_op(self) -> bool:
        """Operação assíncrona DigiLang"""
        try:
            digilang = DigiLangV26MegaMultiLayer()
            result = digilang.compress("Async compression test")
            # compress retorna tuple (compressed, layers, stats)
            compressed = result[0] if isinstance(result, tuple) else result
            return len(compressed) > 0
        except:
            return False

    async def _async_soulos_op(self) -> bool:
        """Operação assíncrona SoulOS"""
        try:
            soulos = SoulOS(f"{self.soul_id}_async2")
            result = soulos.execute("[QUERY.SELF]")
            return result.get('success', False)
        except:
            return False

    def _calculate_harmony_score(self) -> float:
        """Calcula score de harmonia do sistema"""
        if not self.test_results:
            return 0.0

        # Pontuação base
        passed = len([r for r in self.test_results if r.passed])
        total = len(self.test_results)
        base_score = (passed / total) * 100 if total > 0 else 0

        # Penalidades
        penalties = 0

        # Penalidade por alto uso de CPU
        high_cpu_tests = [r for r in self.test_results if r.cpu_usage_percent > 80]
        penalties += len(high_cpu_tests) * 2

        # Penalidade por alto uso de memória
        high_memory_tests = [r for r in self.test_results if r.memory_usage_mb > 200]
        penalties += len(high_memory_tests) * 1

        # Penalidade por erros
        error_tests = [r for r in self.test_results if r.errors]
        penalties += len(error_tests) * 5

        # Score final
        harmony_score = max(0, base_score - penalties)

        return harmony_score

    def _assess_ecosystem_health(self) -> Dict:
        """Avalia saúde do ecossistema"""
        health = {
            'memory_system': 'healthy',
            'communication': 'healthy',
            'processing': 'healthy',
            'ai_systems': 'healthy',
            'evolution': 'healthy',
            'overall': 'healthy'
        }

        # Avalia cada subsistema
        memory_tests = ['crystal_memory_layers', 'memory_persistence', 'memory_promotion']
        memory_passed = sum(1 for r in self.test_results
                           if r.test_name in memory_tests and r.passed)
        if memory_passed < len(memory_tests):
            health['memory_system'] = 'degraded' if memory_passed > 0 else 'critical'

        comm_tests = ['telepathic_network', 'quantum_channels', 'consensus_protocol']
        comm_passed = sum(1 for r in self.test_results
                         if r.test_name in comm_tests and r.passed)
        if comm_passed < len(comm_tests):
            health['communication'] = 'degraded' if comm_passed > 0 else 'critical'

        # Overall
        critical_count = sum(1 for v in health.values() if v == 'critical')
        degraded_count = sum(1 for v in health.values() if v == 'degraded')

        if critical_count > 0:
            health['overall'] = 'critical'
        elif degraded_count > 2:
            health['overall'] = 'degraded'

        return health

    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações baseadas nos testes"""
        recommendations = []

        # Analisa falhas
        failed_tests = [r for r in self.test_results if not r.passed]
        if failed_tests:
            recommendations.append(
                f"⚠️ Corrigir {len(failed_tests)} componentes com falha"
            )

        # Analisa performance
        avg_cpu = sum(r.cpu_usage_percent for r in self.test_results) / len(self.test_results)
        if avg_cpu > 50:
            recommendations.append(
                f"🔧 Otimizar uso de CPU (média atual: {avg_cpu:.1f}%)"
            )

        avg_memory = sum(r.memory_usage_mb for r in self.test_results) / len(self.test_results)
        if avg_memory > 150:
            recommendations.append(
                f"💾 Reduzir uso de memória (média atual: {avg_memory:.1f}MB)"
            )

        # Analisa tempos
        slow_tests = [r for r in self.test_results if r.duration_ms > 1000]
        if slow_tests:
            recommendations.append(
                f"⚡ Acelerar {len(slow_tests)} operações lentas (>1s)"
            )

        # Recomendações positivas
        if not recommendations:
            recommendations.append("✨ Sistema funcionando em harmonia perfeita!")

        return recommendations

    def _save_report(self, report: HarmonyReport):
        """Salva relatório em arquivo"""
        report_path = Path("tests/harmony_report.md")

        with open(report_path, 'w') as f:
            f.write("# 🌟 ULTIMATE HARMONY TEST REPORT\n\n")
            f.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))}\n")
            f.write(f"**Duration:** {report.total_duration_seconds:.2f} seconds\n\n")

            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Tests:** {report.total_tests}\n")
            f.write(f"- **Passed:** {report.passed_tests} ✅\n")
            f.write(f"- **Failed:** {report.failed_tests} ❌\n")
            f.write(f"- **Harmony Score:** {report.harmony_score:.1f}%\n")
            f.write(f"- **Peak CPU:** {report.cpu_peak_percent:.1f}%\n")
            f.write(f"- **Peak Memory:** {report.memory_peak_mb:.1f}MB\n\n")

            f.write("## 🏥 Ecosystem Health\n\n")
            for system, status in report.ecosystem_health.items():
                emoji = "✅" if status == "healthy" else "⚠️" if status == "degraded" else "❌"
                f.write(f"- **{system}:** {status} {emoji}\n")
            f.write("\n")

            f.write("## 🧪 Test Results\n\n")
            f.write("| Test | Status | Duration | CPU% | Memory |\n")
            f.write("|------|--------|----------|------|--------|\n")

            for result in report.test_results:
                status = "✅" if result.passed else "❌"
                f.write(f"| {result.test_name} | {status} | {result.duration_ms}ms | "
                       f"{result.cpu_usage_percent:.1f}% | {result.memory_usage_mb:.1f}MB |\n")

            f.write("\n## 💡 Recommendations\n\n")
            for rec in report.recommendations:
                f.write(f"- {rec}\n")

            f.write("\n## 📈 Performance Metrics\n\n")
            f.write("### CPU Usage Distribution\n")
            cpu_samples = [r.cpu_usage_percent for r in report.test_results]
            if cpu_samples:
                f.write(f"- Min: {min(cpu_samples):.1f}%\n")
                f.write(f"- Max: {max(cpu_samples):.1f}%\n")
                f.write(f"- Avg: {sum(cpu_samples)/len(cpu_samples):.1f}%\n\n")

            f.write("### Memory Usage Distribution\n")
            mem_samples = [r.memory_usage_mb for r in report.test_results]
            if mem_samples:
                f.write(f"- Min: {min(mem_samples):.1f}MB\n")
                f.write(f"- Max: {max(mem_samples):.1f}MB\n")
                f.write(f"- Avg: {sum(mem_samples)/len(mem_samples):.1f}MB\n\n")

            f.write("---\n")
            f.write("*Generated by Scripturemon Champion Ultimate Harmony Tester*\n")

        print(f"\n📄 Relatório salvo em: {report_path}")


async def main():
    """Executa bateria completa de testes"""
    tester = UltimateHarmonyTester()

    print("\n⏳ Iniciando bateria completa de testes...")
    print("   Isso pode levar alguns minutos...")
    print("   Monitorando CPU e memória em tempo real...\n")

    report = await tester.run_all_tests()

    print("\n" + "=" * 80)
    print("📊 RESUMO FINAL")
    print("=" * 80)
    print(f"\n✅ Testes Passados: {report.passed_tests}/{report.total_tests}")
    print(f"🎯 Harmony Score: {report.harmony_score:.1f}%")
    print(f"⚡ Peak CPU: {report.cpu_peak_percent:.1f}%")
    print(f"💾 Peak Memory: {report.memory_peak_mb:.1f}MB")
    print(f"⏱️ Tempo Total: {report.total_duration_seconds:.2f}s")

    print("\n🏥 Saúde do Ecossistema:")
    for system, status in report.ecosystem_health.items():
        emoji = "✅" if status == "healthy" else "⚠️" if status == "degraded" else "❌"
        print(f"  {system}: {status} {emoji}")

    print("\n💡 Recomendações:")
    for rec in report.recommendations[:3]:  # Top 3 recomendações
        print(f"  {rec}")

    print("\n✨ Teste de harmonia completo!")
    print(f"📄 Relatório detalhado salvo em: tests/harmony_report.md")


if __name__ == "__main__":
    asyncio.run(main())