"""
TripleCoreWrapper - Orquestrador do Triple-Core Architecture

ARQUITETURA:
┌─────────────────────────────────────────────────────────────┐
│                    TRIPLE-CORE ANALYSIS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  INPUT: Screenplay Text                                      │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PYTHON CORE 1: Specialist Analysis                   │  │
│  │  (Technical, objective metrics)                       │  │
│  │  → Score, violations, recommendations                 │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PYTHON CORE 2: Example Finder                        │  │
│  │  (Search masters for solutions)                       │  │
│  │  → Real examples from Tarantino, Nolan, etc           │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLM CORE: Theory Enrichment                          │  │
│  │  (McKee theory + synthesis)                           │  │
│  │  → Deep insights, connections, learning               │  │
│  └──────────────────────────────────────────────────────┘  │
│     ↓                                                        │
│  OUTPUT: Complete Analysis (3 cores synthesized)            │
│                                                              │
└─────────────────────────────────────────────────────────────┘

FASES DO RELATÓRIO:
1. Python Core 1: Análise Técnica (objetiva)
2. Python Core 2: Exemplos de Mestres (concreto)
3. LLM Core: Teoria e Insights (profundo)
4. Síntese: Combinação dos 3 cores
5. Plano de Ação: Próximos passos
"""

import time
import subprocess
import json
from typing import Dict, Any, Optional
from pathlib import Path

from triple_core.core_2_examples.example_finder import ExampleFinderCore
from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper

# Para type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass


class TripleCoreWrapper(DualCoreWrapper):
    """
    Orquestra análise com 3 cores: Python Base + Python Examples + LLM Theory.

    Este é o WRAPPER PRINCIPAL do Triple-Core.
    Substitui o DualCoreWrapper para análises mais profundas.

    Usage:
        specialist = DrDialogue()
        wrapper = TripleCoreWrapper(
            python_specialist=specialist,
            llm_model="scripturemon-optimized",
            deep_context=True
        )
        result = wrapper.analyze(screenplay_text)
    """

    def __init__(self,
                 python_specialist: Any,
                 llm_model: str = "scripturemon-optimized",
                 llm_timeout: int = 600,
                 deep_context: bool = True):
        """
        Args:
            python_specialist: Instância do especialista Python (DrDialogue, DrStructure, etc)
            llm_model: Modelo Ollama para LLM Core
            llm_timeout: Timeout do LLM em segundos
            deep_context: Se True, envia teoria completa (Deep Dive)
        """
        # Chamar init do DualCoreWrapper (herda todo o comportamento)
        super().__init__(
            python_specialist=python_specialist,
            llm_model=llm_model,
            llm_timeout=llm_timeout,
            fallback_to_python=True,
            use_theory=True,
            deep_context=deep_context
        )

        # Triple-Core adicional: Example Finder
        self.example_finder = ExampleFinderCore()

    def analyze(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Executa análise Triple-Core completa.

        Args:
            screenplay_text: Texto do roteiro

        Returns:
            Dicionário com resultados dos 3 cores + síntese
        """
        result = {
            'triple_core': True,
            'specialist': self.specialist_name,
            'timestamp': time.time(),
            'deep_context': self.deep_context,
            'cores': []
        }

        # ============================================================
        # CORE 1: PYTHON SPECIALIST (Análise Técnica)
        # ============================================================
        print("⚙️  [1/3] Python Core 1: Technical Analysis...")
        try:
            core1_start = time.time()
            core1_result = self.python_specialist.analyze(screenplay_text)
            core1_time = time.time() - core1_start

            result['python_core1'] = core1_result
            result['python_core1_time'] = core1_time
            result['python_success'] = True
            result['cores'].append('Python Core 1')
            print(f"   ✅ Core 1 completed in {core1_time:.1f}s")

        except Exception as e:
            result['python_success'] = False
            result['python_core1'] = {'error': str(e)}
            print(f"   ❌ Core 1 failed: {e}")
            # Não abortar - continuar com cores 2 e 3

        # ============================================================
        # CORE 2: EXAMPLE FINDER (Exemplos de Mestres)
        # ============================================================
        print("📚 [2/3] Python Core 2: Finding Examples in Masters...")
        try:
            core2_start = time.time()

            # Passar análise do Core 1 para o Core 2
            core2_result = self.example_finder.analyze(
                base_analysis=result.get('python_core1', {}),
                screenplay_text=screenplay_text,
                max_examples_per_problem=7  # Sweet spot: 15 problemas × 7 exemplos = ~105 total
            )
            core2_time = time.time() - core2_start

            result['python_core2'] = core2_result
            result['python_core2_time'] = core2_time
            result['examples_success'] = True
            result['cores'].append('Python Core 2')
            print(f"   ✅ Core 2 completed in {core2_time:.1f}s")
            print(f"   📖 Found {core2_result['total_examples']} examples from masters")

        except Exception as e:
            result['examples_success'] = False
            result['python_core2'] = {'error': str(e)}
            print(f"   ❌ Core 2 failed: {e}")

        # ============================================================
        # CORE 3: LLM (Teoria + Síntese)
        # ============================================================
        print("🤖 [3/3] LLM Core: Theory Enrichment...")
        try:
            core3_start = time.time()

            # Usar prompt do DualCoreWrapper (herdado - tem few-shot + task instructions)
            # Passar Core 1 como se fosse python_result do Dual-Core
            llm_prompt = super()._build_llm_prompt(
                screenplay_text=screenplay_text,
                python_result=result.get('python_core1', {})
            )

            # Chamar LLM via subprocess (como Dual-Core faz)
            print(f"   📝 Prompt length: {len(llm_prompt)} chars")
            llm_result = subprocess.run(
                ['ollama', 'run', self.llm_model],
                input=llm_prompt,
                capture_output=True,
                text=True,
                timeout=self.llm_timeout
            )
            core3_time = time.time() - core3_start

            print(f"   📊 LLM return code: {llm_result.returncode}")
            print(f"   📊 LLM stdout length: {len(llm_result.stdout)}")
            print(f"   📊 LLM stderr length: {len(llm_result.stderr)}")

            if llm_result.returncode == 0:
                result['llm_insights'] = llm_result.stdout.strip()
                print(f"   📊 Stored insights length: {len(result['llm_insights'])}")
            else:
                raise Exception(f"Ollama error: {llm_result.stderr}")
            result['llm_time'] = core3_time
            result['llm_success'] = True
            result['cores'].append('LLM Core')
            print(f"   ✅ Core 3 completed in {core3_time:.1f}s")

        except Exception as e:
            result['llm_success'] = False
            result['llm_insights'] = {'error': str(e)}
            print(f"   ❌ Core 3 failed: {e}")

        # ============================================================
        # SYNTHESIS: Combinar os 3 cores
        # ============================================================
        result['synthesis'] = super()._synthesize(
            python_result=result.get('python_core1', {}),
            llm_response=result.get('llm_insights', '')
        )

        # Calcular quality score (herdado do DualCoreWrapper)
        result['quality_score'] = super()._calculate_quality_score(
            python_result=result.get('python_core1', {}),
            llm_response=result.get('llm_insights', '')
        )

        # Tempo total
        result['total_time'] = time.time() - result['timestamp']
        print(f"✅ Triple-Core analysis complete in {result['total_time']:.1f}s")

        return result

    # Métodos _build_llm_prompt, _call_ollama, _synthesize herdados do DualCoreWrapper
    # Não precisa reimplementar - usa o prompt completo com few-shot + task instructions
