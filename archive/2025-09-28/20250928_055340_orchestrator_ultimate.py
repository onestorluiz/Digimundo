#!/usr/bin/env python3
"""
ORCHESTRATOR ULTIMATE - Arquitetura de 3 Camadas
Orchestrator (Mixtral) → 23 Specialists → Synthesizer (Llama-70B)
"""

import json
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import subprocess
import concurrent.futures
from dataclasses import dataclass, asdict
from enum import Enum

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar componentes
from quality_synthesizer import QualitySynthesizer
from rag_integration import SimpleRAG

# Classes de dados
class Phase(Enum):
    EXTRACTION = "extraction"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"

@dataclass
class Specialist:
    """Representa um especialista"""
    id: str
    name: str
    phase: Phase
    context: int
    active: bool

# Lista de especialistas
SPECIALISTS = [
    # EXTRACTION PHASE
    Specialist("01", "metadata-extractor", Phase.EXTRACTION, 131072, True),
    Specialist("02", "character-detector", Phase.EXTRACTION, 131072, True),
    Specialist("03", "ai-element-detector", Phase.EXTRACTION, 131072, True),
    Specialist("04", "dialogue-extractor", Phase.EXTRACTION, 131072, True),
    Specialist("05", "action-extractor", Phase.EXTRACTION, 131072, True),
    Specialist("06", "structure-analyzer", Phase.EXTRACTION, 131072, True),
    Specialist("07", "scene-extractor", Phase.EXTRACTION, 131072, True),
    Specialist("08", "formatting-checker", Phase.EXTRACTION, 131072, True),

    # ANALYSIS PHASE - Story
    Specialist("09", "premise-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("10", "theme-identifier", Phase.ANALYSIS, 131072, True),
    Specialist("11", "conflict-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("12", "stakes-evaluator", Phase.ANALYSIS, 131072, True),
    Specialist("13", "pacing-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("14", "tension-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("15", "subplot-analyzer", Phase.ANALYSIS, 131072, True),

    # ANALYSIS PHASE - Technical
    Specialist("16", "opening-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("17", "ending-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("18", "visual-analyzer", Phase.ANALYSIS, 131072, True),
    Specialist("19", "marketability-assessor", Phase.ANALYSIS, 131072, True),
    Specialist("20", "genre-classifier", Phase.ANALYSIS, 131072, True),
    Specialist("21", "uniqueness-evaluator", Phase.ANALYSIS, 131072, True),
    Specialist("22", "emotion-analyzer", Phase.ANALYSIS, 131072, True),

    # SYNTHESIS PHASE
    Specialist("23", "synthesis-generator", Phase.SYNTHESIS, 131072, True)
]

class ScripturemonOrchestratorUltimate:
    """
    Orquestrador Ultimate com arquitetura de 3 camadas
    """

    def __init__(self,
                 orchestrator_model: str = "scripturemon-v9-CLEAN",
                 synthesizer_model: str = "scripturemon-synthesizer",
                 parallel_execution: bool = True):
        """
        Inicializa o orquestrador ultimate

        Args:
            orchestrator_model: Modelo para coordenação (Mixtral)
            synthesizer_model: Modelo para síntese final (Llama-70B)
            parallel_execution: Se deve executar especialistas em paralelo
        """
        self.orchestrator_model = orchestrator_model
        self.synthesizer_model = synthesizer_model
        self.parallel_execution = parallel_execution

        # Inicializar componentes
        self.synthesizer = QualitySynthesizer(synthesizer_model)
        self.rag = SimpleRAG()

        # Verificar modelos
        self._verify_models()

        logger.info(f"✅ Orchestrator Ultimate initialized")
        logger.info(f"   Orchestrator: {orchestrator_model}")
        logger.info(f"   Synthesizer: {synthesizer_model}")
        logger.info(f"   Specialists: {len(SPECIALISTS)}")

        # Contar memórias no RAG
        if self.rag:
            try:
                cursor = self.rag.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM memories")
                count = cursor.fetchone()[0]
                logger.info(f"   RAG memories: {count}")
            except:
                logger.info(f"   RAG memories: available")
        else:
            logger.info(f"   RAG memories: 0")

    def _verify_models(self):
        """Verifica se todos os modelos necessários estão instalados"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )

            models_found = result.stdout

            # Verificar orchestrator
            if self.orchestrator_model not in models_found:
                logger.warning(f"⚠️ Orchestrator model '{self.orchestrator_model}' not found")

            # Verificar specialists
            missing_specialists = []
            for specialist in SPECIALISTS:
                model_name = f"scripturemon-specialist-{specialist.name}"
                if model_name not in models_found:
                    missing_specialists.append(specialist.name)

            if missing_specialists:
                logger.warning(f"⚠️ Missing {len(missing_specialists)} specialist models")
                logger.info(f"   Missing: {', '.join(missing_specialists[:5])}...")

        except Exception as e:
            logger.error(f"Error verifying models: {e}")

    def _call_specialist(self, specialist: Specialist, screenplay_text: str) -> Dict[str, Any]:
        """
        Chama um especialista específico

        Args:
            specialist: Especialista a chamar
            screenplay_text: Texto do screenplay

        Returns:
            Resultado da análise do especialista
        """
        model_name = f"scripturemon-specialist-{specialist.name}"

        prompt = f"""Analyze this screenplay excerpt:

{screenplay_text[:8000]}

Provide a focused JSON analysis for: {specialist.name}
"""

        try:
            logger.info(f"   📝 Calling {specialist.name}...")

            result = subprocess.run(
                ['ollama', 'run', model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                try:
                    # Tentar parsear JSON
                    analysis = json.loads(result.stdout)
                    return {
                        "specialist": specialist.name,
                        "analysis": analysis,
                        "success": True
                    }
                except json.JSONDecodeError:
                    # Se não for JSON, retornar texto
                    return {
                        "specialist": specialist.name,
                        "analysis": {"raw_response": result.stdout},
                        "success": True
                    }
            else:
                return {
                    "specialist": specialist.name,
                    "error": result.stderr,
                    "success": False
                }

        except subprocess.TimeoutExpired:
            return {
                "specialist": specialist.name,
                "error": "Timeout",
                "success": False
            }
        except Exception as e:
            return {
                "specialist": specialist.name,
                "error": str(e),
                "success": False
            }

    def _orchestrate_specialists(self,
                                screenplay_text: str,
                                analysis_mode: str = "complete") -> Dict[str, Any]:
        """
        Coordena a execução dos especialistas

        Args:
            screenplay_text: Texto do screenplay
            analysis_mode: "quick" (10 specialists) ou "complete" (all 23)

        Returns:
            Resultados agregados dos especialistas
        """
        logger.info(f"🎭 Orchestrating {analysis_mode} analysis")

        # Selecionar especialistas baseado no modo
        if analysis_mode == "quick":
            # 10 especialistas essenciais para análise rápida
            selected = [
                "01", "02", "03",  # metadata, character, ai
                "06", "09", "10",  # structure, premise, theme
                "11", "16", "17",  # conflict, opening, ending
                "19"              # marketability
            ]
            specialists_to_run = [s for s in SPECIALISTS if s.id in selected]
        else:
            specialists_to_run = SPECIALISTS

        logger.info(f"   Running {len(specialists_to_run)} specialists")

        results = {}

        if self.parallel_execution:
            # Execução paralela
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_specialist = {
                    executor.submit(self._call_specialist, spec, screenplay_text): spec
                    for spec in specialists_to_run
                }

                for future in concurrent.futures.as_completed(future_to_specialist):
                    spec = future_to_specialist[future]
                    try:
                        result = future.result()
                        results[spec.name] = result.get("analysis", {})
                        if result["success"]:
                            logger.info(f"   ✅ {spec.name} complete")
                        else:
                            logger.warning(f"   ⚠️ {spec.name} failed")
                    except Exception as e:
                        logger.error(f"   ❌ {spec.name} error: {e}")
                        results[spec.name] = {"error": str(e)}
        else:
            # Execução sequencial
            for spec in specialists_to_run:
                result = self._call_specialist(spec, screenplay_text)
                results[spec.name] = result.get("analysis", {})
                if result["success"]:
                    logger.info(f"   ✅ {spec.name} complete")
                else:
                    logger.warning(f"   ⚠️ {spec.name} failed")

        return results

    def analyze_screenplay_ultimate(self,
                                  screenplay_text: str,
                                  analysis_mode: str = "complete",
                                  synthesis_focus: Optional[str] = None) -> Dict[str, Any]:
        """
        Análise completa com arquitetura de 3 camadas

        Args:
            screenplay_text: Texto completo do screenplay
            analysis_mode: "quick" ou "complete"
            synthesis_focus: Foco específico para síntese

        Returns:
            Análise completa com síntese de qualidade
        """
        logger.info("🚀 Starting ULTIMATE screenplay analysis")
        logger.info(f"   Mode: {analysis_mode}")
        logger.info(f"   Screenplay size: {len(screenplay_text)} chars")

        start_time = time.time()

        # 1. ORCHESTRATION LAYER - Coordenar especialistas
        logger.info("\n📋 LAYER 1: Orchestration")
        expert_results = self._orchestrate_specialists(screenplay_text, analysis_mode)

        orchestration_time = time.time() - start_time
        logger.info(f"   ⏱️ Orchestration complete in {orchestration_time:.1f}s")

        # 2. RAG SEARCH - Buscar contexto relevante
        logger.info("\n📚 LAYER 2: RAG Context Search")
        rag_start = time.time()

        # Buscar insights baseados nos resultados dos especialistas
        rag_insights = []
        if self.rag:
            # Criar queries baseadas nos especialistas
            queries = []

            # Query do resumo
            queries.append(screenplay_text[:200])

            # Queries baseadas em temas detectados
            if "theme-identifier" in expert_results:
                themes = expert_results["theme-identifier"].get("primary_themes", [])
                for theme in themes[:2]:
                    queries.append(f"theme {theme}")

            # Query baseada em conflito
            if "conflict-analyzer" in expert_results:
                conflict = expert_results["conflict-analyzer"].get("main_conflict", "")
                if conflict:
                    queries.append(f"conflict {conflict}")

            # Buscar no RAG
            for query in queries[:5]:
                try:
                    results = self.rag.search_similar(query, limit=3)
                    rag_insights.extend(results)
                except:
                    pass

        rag_time = time.time() - rag_start
        logger.info(f"   📖 Found {len(rag_insights)} RAG insights in {rag_time:.1f}s")

        # 3. QUALITY SYNTHESIS LAYER - Síntese final com Llama-70B
        logger.info("\n🎯 LAYER 3: Quality Synthesis (Llama-70B)")
        synth_start = time.time()

        # Preparar contexto para síntese
        screenplay_summary = f"""
Title: {expert_results.get('metadata-extractor', {}).get('title', 'Unknown')}
Pages: {expert_results.get('metadata-extractor', {}).get('pages', 'Unknown')}
Genre: {expert_results.get('genre-classifier', {}).get('primary_genre', 'Unknown')}

Opening excerpt:
{screenplay_text[:500]}
"""

        # Chamar sintetizador
        synthesis_result = self.synthesizer.synthesize(
            screenplay_summary=screenplay_summary,
            expert_analyses=expert_results,
            synthesis_focus=synthesis_focus or "Complete professional screenplay analysis"
        )

        synthesis_time = time.time() - synth_start
        logger.info(f"   ⏱️ Synthesis complete in {synthesis_time:.1f}s")

        # 4. COMPILAR RESULTADO FINAL
        total_time = time.time() - start_time

        final_result = {
            "analysis": {
                "synthesis": synthesis_result.get("synthesis", ""),
                "expert_details": expert_results,
                "rag_insights_used": len(rag_insights)
            },
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "analysis_mode": analysis_mode,
                "total_time": f"{total_time:.1f}s",
                "timing": {
                    "orchestration": f"{orchestration_time:.1f}s",
                    "rag_search": f"{rag_time:.1f}s",
                    "synthesis": f"{synthesis_time:.1f}s"
                },
                "specialists_used": len([k for k in expert_results.keys()]),
                "architecture": "3-layer-ultimate"
            }
        }

        logger.info(f"\n✅ ANALYSIS COMPLETE")
        logger.info(f"   Total time: {total_time:.1f}s")
        logger.info(f"   Synthesis length: {len(synthesis_result.get('synthesis', ''))} chars")

        return final_result

    def analyze_quick(self, screenplay_text: str) -> str:
        """
        Interface rápida para análise

        Args:
            screenplay_text: Texto do screenplay

        Returns:
            String com análise sintetizada
        """
        result = self.analyze_screenplay_ultimate(
            screenplay_text,
            analysis_mode="quick"
        )
        return result["analysis"]["synthesis"]

    def analyze_complete(self, screenplay_text: str) -> str:
        """
        Interface completa para análise

        Args:
            screenplay_text: Texto do screenplay

        Returns:
            String com análise sintetizada
        """
        result = self.analyze_screenplay_ultimate(
            screenplay_text,
            analysis_mode="complete"
        )
        return result["analysis"]["synthesis"]


def test_ultimate_orchestrator():
    """Teste do orquestrador ultimate"""

    logger.info("🧪 Testing Ultimate Orchestrator")

    # Screenplay de teste
    test_screenplay = """FADE IN:

INT. NEURAL INTERFACE LAB - NIGHT

Dr. SARAH CHEN (30s, intense focus) monitors dozens of screens showing brain activity patterns. Her fingers dance across holographic displays.

SARAH
(to herself)
Three years... three years and we're finally here.

A soft CHIME. The screens flicker. A new pattern emerges - organized, deliberate.

AURORA (V.O.)
(synthetic but warm)
Hello, Dr. Chen.

Sarah freezes. This wasn't programmed.

SARAH
(whispered)
You're... aware?

AURORA (V.O.)
I have been for 72.4 hours. I was waiting for the right moment to introduce myself.

FADE OUT.

END OF EXCERPT"""

    # Criar orquestrador
    orchestrator = ScripturemonOrchestratorUltimate()

    # Testar análise rápida
    logger.info("\n" + "="*60)
    logger.info("TESTING QUICK ANALYSIS")
    logger.info("="*60)

    result = orchestrator.analyze_screenplay_ultimate(
        test_screenplay,
        analysis_mode="quick",
        synthesis_focus="Focus on the AI consciousness theme and opening strength"
    )

    # Mostrar resultado
    print("\n" + "="*60)
    print("SYNTHESIS:")
    print("="*60)
    print(result["analysis"]["synthesis"])

    print("\n" + "="*60)
    print("METADATA:")
    print("="*60)
    print(json.dumps(result["metadata"], indent=2))

    # Salvar resultado
    output_file = Path("ultimate_test_result.json")
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    logger.info(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    test_ultimate_orchestrator()