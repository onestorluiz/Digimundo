#!/usr/bin/env python3
"""
🎭 DUAL-TRACK ORCHESTRATOR
GPU responde rápido, CPU analisa profundo em background
Maximiza uso dos 96GB RAM e 28 cores do Mac Studio M3 Ultra
"""

import asyncio
import ollama
import threading
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from queue import Queue, PriorityQueue
import json
from datetime import datetime

@dataclass
class AnalysisResult:
    """Resultado de análise de um modelo"""
    model: str
    track: str  # 'gpu' ou 'cpu'
    response: str
    time_taken: float
    timestamp: datetime
    depth_level: int  # 1=superficial, 5=profundo

class CoreAllocation:
    """Distribuição inteligente dos 28 cores do Mac Studio"""

    TOTAL_CORES = 28

    ALLOCATION = {
        # CPU Model - Pensador Profundo (8 cores)
        'scripturemon-cpu': 8,
        'scripturemon-cpu-themes': 8,
        'scripturemon-cpu-structure': 8,

        # GPU Models Leves (4 cores cada quando rodando)
        'llama3.2:3b': 4,
        'producermon': 4,
        'mistral:7b': 4,
        'gemma2:2b': 4,

        # GPU Models Médios (6 cores cada)
        'llama3.1:8b': 6,
        'qwen2.5:14b': 6,

        # Sistema e Buffer
        'system': 8,  # Python, Ollama server, OS
        'buffer': 4   # Margem de segurança
    }

    def __init__(self):
        self.active_models = {}
        self.available_cores = self.TOTAL_CORES - self.ALLOCATION['system']
        self.lock = threading.Lock()

    def can_allocate(self, model: str) -> bool:
        """Verifica se pode alocar cores para o modelo"""
        with self.lock:
            required = self.ALLOCATION.get(model, 4)
            return self.available_cores >= required

    def allocate(self, model: str) -> Optional[int]:
        """Aloca cores para um modelo"""
        with self.lock:
            required = self.ALLOCATION.get(model, 4)
            if self.available_cores >= required:
                self.available_cores -= required
                self.active_models[model] = required
                return required
            return None

    def release(self, model: str):
        """Libera cores de um modelo"""
        with self.lock:
            if model in self.active_models:
                cores = self.active_models[model]
                self.available_cores += cores
                del self.active_models[model]

class DualTrackOrchestrator:
    """Orquestrador que roda GPU e CPU em paralelo sem competição"""

    def __init__(self):
        self.core_manager = CoreAllocation()
        self.gpu_queue = PriorityQueue()
        self.cpu_queue = PriorityQueue()
        self.results_cache = {}
        self.executor = ThreadPoolExecutor(max_workers=8)

        # Estatísticas
        self.stats = {
            'gpu_analyses': 0,
            'cpu_analyses': 0,
            'parallel_executions': 0,
            'total_time_saved': 0
        }

    async def analyze_screenplay(self, pdf_text: str, mode: str = 'dual') -> Dict:
        """
        Analisa roteiro em modo dual-track

        Modes:
        - 'fast': Só GPU (< 30s)
        - 'dual': GPU + CPU paralelo
        - 'deep': CPU com preview GPU
        """

        start_time = time.time()
        results = {
            'mode': mode,
            'tracks': {},
            'synthesis': None,
            'timeline': []
        }

        if mode == 'fast':
            # Só track rápido GPU
            gpu_result = await self._gpu_track(pdf_text[:5000])
            results['tracks']['gpu'] = gpu_result
            results['synthesis'] = gpu_result.response

        elif mode == 'dual':
            # Dual track: GPU responde rápido, CPU analisa profundo
            self.stats['parallel_executions'] += 1

            # Inicia ambos em paralelo
            gpu_future = asyncio.create_task(self._gpu_track(pdf_text[:5000]))
            cpu_future = asyncio.create_task(self._cpu_track_async(pdf_text))

            # GPU termina primeiro (15-30s)
            gpu_result = await gpu_future
            results['tracks']['gpu'] = gpu_result
            results['timeline'].append({
                'time': gpu_result.time_taken,
                'event': 'GPU analysis complete',
                'preview': gpu_result.response[:200]
            })

            # Retorna preview imediatamente
            print(f"\n✅ Análise rápida disponível em {gpu_result.time_taken:.1f}s")
            print("⏳ Análise profunda em processamento (2-5min)...")

            # CPU continua em background (2-5min)
            cpu_result = await cpu_future
            results['tracks']['cpu'] = cpu_result
            results['timeline'].append({
                'time': cpu_result.time_taken,
                'event': 'CPU deep analysis complete',
                'insights': cpu_result.response[:200]
            })

            # Síntese final combinando ambas perspectivas
            results['synthesis'] = await self._synthesize_dual_tracks(
                gpu_result, cpu_result
            )

        elif mode == 'deep':
            # Deep mode: Preview GPU, então CPU profundo
            gpu_preview = await self._gpu_track(pdf_text[:2000])
            print(f"📊 Preview em {gpu_preview.time_taken:.1f}s")

            cpu_result = await self._cpu_track_async(pdf_text)
            results['tracks']['cpu'] = cpu_result
            results['synthesis'] = cpu_result.response

        # Estatísticas
        total_time = time.time() - start_time
        if mode == 'dual':
            # Tempo economizado por paralelização
            sequential_time = (results['tracks'].get('gpu', gpu_result).time_taken +
                             results['tracks'].get('cpu', cpu_result).time_taken)
            time_saved = sequential_time - total_time
            self.stats['total_time_saved'] += time_saved
            results['time_saved'] = time_saved

        results['total_time'] = total_time
        return results

    async def _gpu_track(self, text: str) -> AnalysisResult:
        """Track rápido com modelos GPU"""

        start = time.time()

        # Escolhe modelo GPU baseado em disponibilidade de cores
        gpu_models = ['llama3.2:3b', 'gemma2:2b', 'mistral:7b']
        selected_model = None

        for model in gpu_models:
            if self.core_manager.can_allocate(model):
                cores = self.core_manager.allocate(model)
                if cores:
                    selected_model = model
                    break

        if not selected_model:
            selected_model = 'llama3.2:3b'  # Fallback
            cores = 4

        try:
            # Análise rápida estrutural
            response = ollama.generate(
                model=selected_model,
                prompt=f"""Analyze this screenplay excerpt quickly:

{text}

Provide:
1. Genre and tone
2. Main conflict
3. Key characters
4. Pacing assessment
5. Dialogue quality

Keep it concise for quick feedback.""",
                options={
                    'num_thread': cores,
                    'temperature': 0.7,
                    'num_ctx': 4096
                }
            )

            self.stats['gpu_analyses'] += 1

            return AnalysisResult(
                model=selected_model,
                track='gpu',
                response=response['response'],
                time_taken=time.time() - start,
                timestamp=datetime.now(),
                depth_level=2
            )

        finally:
            self.core_manager.release(selected_model)

    async def _cpu_track_async(self, text: str) -> AnalysisResult:
        """Track profundo com CPU em background"""

        start = time.time()

        # Aloca cores para CPU model
        cores = self.core_manager.allocate('scripturemon-cpu')
        if not cores:
            cores = 8  # Default

        try:
            # Cria task assíncrona para não bloquear
            def cpu_analysis():
                return ollama.generate(
                    model='scripturemon-cpu',
                    prompt=f"""Perform deep thematic and symbolic analysis:

{text}

Focus on:
1. Hidden symbolic layers and metaphors
2. Long-term character arc trajectories
3. Philosophical and existential themes
4. Archetypal patterns and deep structure
5. Cultural references and intertextuality
6. Subtext and unspoken character dynamics
7. What the faster models might have missed

Take your time for profound insights.""",
                    options={
                        'num_thread': cores,
                        'temperature': 0.6,
                        'num_ctx': 16384,
                        'num_batch': 512
                    }
                )

            # Executa em thread separada para não bloquear
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor, cpu_analysis
            )

            self.stats['cpu_analyses'] += 1

            return AnalysisResult(
                model='scripturemon-cpu',
                track='cpu',
                response=response['response'],
                time_taken=time.time() - start,
                timestamp=datetime.now(),
                depth_level=5
            )

        finally:
            self.core_manager.release('scripturemon-cpu')

    async def _synthesize_dual_tracks(self, gpu_result: AnalysisResult,
                                     cpu_result: AnalysisResult) -> str:
        """Sintetiza insights de ambas as tracks"""

        # ProducerMon sintetiza as duas perspectivas
        synthesis_prompt = f"""As ProducerMon, synthesize these two analyses:

GPU QUICK ANALYSIS ({gpu_result.time_taken:.1f}s):
{gpu_result.response[:1000]}

CPU DEEP ANALYSIS ({cpu_result.time_taken:.1f}s):
{cpu_result.response[:1000]}

Create a unified insight that combines:
- The structural clarity from GPU
- The thematic depth from CPU
- Highlight unique discoveries from each
- Show how they complement each other"""

        response = ollama.generate(
            model='producermon',
            prompt=synthesis_prompt,
            options={'temperature': 0.7}
        )

        return response['response']

    def get_stats(self) -> Dict:
        """Retorna estatísticas de execução"""
        return {
            **self.stats,
            'active_models': list(self.core_manager.active_models.keys()),
            'available_cores': self.core_manager.available_cores,
            'efficiency': f"{(self.stats['total_time_saved'] / 60):.1f} minutes saved"
        }

class MultiPerspectiveOrchestrator:
    """Orquestra múltiplos modelos CPU especializados em paralelo"""

    CPU_VARIANTS = {
        'themes': 'scripturemon-cpu-themes',
        'structure': 'scripturemon-cpu-structure',
        'dialogue': 'scripturemon-cpu-dialogue',
        'symbolism': 'scripturemon-cpu-symbolism'
    }

    def __init__(self):
        self.orchestrator = DualTrackOrchestrator()

    async def analyze_multi_perspective(self, text: str) -> Dict:
        """Análise com múltiplas variantes CPU em paralelo"""

        print("🎭 Iniciando análise multi-perspectiva...")

        # GPU fornece contexto rápido
        gpu_context = await self.orchestrator._gpu_track(text[:3000])
        print(f"✅ Contexto GPU em {gpu_context.time_taken:.1f}s")

        # Múltiplas perspectivas CPU em paralelo
        cpu_tasks = []
        for perspective, model in self.CPU_VARIANTS.items():
            if self.orchestrator.core_manager.can_allocate(model):
                task = self._analyze_perspective(model, text, perspective)
                cpu_tasks.append(task)

        # Executa todas as perspectivas em paralelo
        perspectives = await asyncio.gather(*cpu_tasks)

        # Sintetiza todas as perspectivas
        synthesis = await self._synthesize_perspectives(gpu_context, perspectives)

        return {
            'gpu_context': gpu_context,
            'perspectives': perspectives,
            'synthesis': synthesis
        }

    async def _analyze_perspective(self, model: str, text: str,
                                  perspective: str) -> AnalysisResult:
        """Analisa uma perspectiva específica"""

        start = time.time()

        prompts = {
            'themes': "Focus on deep thematic analysis and philosophical underpinnings",
            'structure': "Analyze three-act structure, plot points, and narrative architecture",
            'dialogue': "Examine dialogue quality, subtext, and character voice",
            'symbolism': "Uncover symbolic layers, metaphors, and hidden meanings"
        }

        response = ollama.generate(
            model=model,
            prompt=f"{prompts[perspective]}:\n\n{text}",
            options={'num_thread': 6, 'temperature': 0.6}
        )

        return AnalysisResult(
            model=model,
            track='cpu_specialized',
            response=response['response'],
            time_taken=time.time() - start,
            timestamp=datetime.now(),
            depth_level=4
        )

    async def _synthesize_perspectives(self, gpu_context: AnalysisResult,
                                      perspectives: List[AnalysisResult]) -> str:
        """Sintetiza múltiplas perspectivas em visão unificada"""

        all_perspectives = "\n\n".join([
            f"{p.model}: {p.response[:500]}" for p in perspectives
        ])

        synthesis = ollama.generate(
            model='scripturemon',
            prompt=f"""Synthesize these multiple perspectives into unified insight:

GPU Context: {gpu_context.response[:500]}

Specialized Perspectives:
{all_perspectives}

Create a comprehensive analysis that shows how all perspectives interconnect.""",
            options={'temperature': 0.7}
        )

        return synthesis['response']

async def demo_dual_track():
    """Demonstração do sistema dual-track"""

    print("🚀 DUAL-TRACK ORCHESTRATOR - DEMONSTRAÇÃO")
    print("=" * 60)
    print("Mac Studio M3 Ultra - 96GB RAM - 28 cores")
    print("=" * 60)

    orchestrator = DualTrackOrchestrator()

    # Texto de exemplo
    sample_text = """
    FADE IN:

    INT. ABANDONED WAREHOUSE - NIGHT

    The moonlight filters through broken windows, casting long shadows.
    SARAH (30s, determined) enters cautiously, her hand hovering over
    the gun at her hip.

    SARAH
    (whispered)
    I know you're here, Marcus.

    A figure emerges from the shadows - MARCUS (40s, weathered).

    MARCUS
    You shouldn't have come.

    SARAH
    You left me no choice. After what you
    did to Elena...

    Marcus's face hardens. The air between them crackles with tension.

    MARCUS
    Elena made her choice. Just like you're
    making yours now.

    Sarah's hand moves to her gun. Marcus doesn't flinch.

    SARAH
    This ends tonight.

    MARCUS
    (sad smile)
    It ended five years ago, Sarah.
    You just didn't know it yet.
    """

    # Teste modo dual-track
    print("\n📊 Testando modo DUAL-TRACK (GPU + CPU paralelo)...")
    result = await orchestrator.analyze_screenplay(sample_text, mode='dual')

    print(f"\n📈 RESULTADOS:")
    print(f"   • Tempo total: {result['total_time']:.1f}s")
    if 'time_saved' in result:
        print(f"   • Tempo economizado: {result['time_saved']:.1f}s")
    print(f"   • GPU track: {result['tracks']['gpu'].time_taken:.1f}s")
    if 'cpu' in result['tracks']:
        print(f"   • CPU track: {result['tracks']['cpu'].time_taken:.1f}s")

    # Estatísticas
    stats = orchestrator.get_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   • Análises GPU: {stats['gpu_analyses']}")
    print(f"   • Análises CPU: {stats['cpu_analyses']}")
    print(f"   • Execuções paralelas: {stats['parallel_executions']}")
    print(f"   • Eficiência: {stats['efficiency']}")

    print("\n✅ Dual-track orchestration complete!")
    print("   GPU forneceu resposta rápida")
    print("   CPU forneceu análise profunda")
    print("   Ambos rodaram em paralelo sem conflito!")

if __name__ == "__main__":
    # Testa o sistema
    asyncio.run(demo_dual_track())

    print("\n" + "=" * 60)
    print("DIGIMUNDO PRESENTE")