#!/usr/bin/env python3
"""
SCRIPTUREMON CORE SYSTEM
Sistema principal de análise com memória integrada + Dual-Core Architecture
"""

import json
import logging
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import sys

# Adicionar path para dual_core
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports locais
from .config import (
    SPECIALISTS, SPECIALIST_MODELFILES, MODELFILES_DIR, OUTPUTS_DIR,
    ORCHESTRATOR_MODEL, EVALUATOR_MODEL, OLLAMA_HOST,
    MODEL_PARAMS, EVALUATOR_PARAMS, OLLAMA_TIMEOUT, OLLAMA_TIMEOUT_EVALUATOR,
    QUICK_SPECIALISTS, STANDARD_SPECIALISTS, ENABLE_MEMORY_ENRICHMENT,
    GIT_MEMORY_ENABLED
)
from .memory_system import ScripturemonMemory, MemoryIntegration

# Import Git-Memory if enabled
if GIT_MEMORY_ENABLED:
    try:
        from .git_memory_bridge import EnhancedMemorySystem
        GIT_MEMORY_AVAILABLE = True
    except ImportError:
        GIT_MEMORY_AVAILABLE = False
        logger.warning("⚠️ Git-Memory not available - using standard memory")
else:
    GIT_MEMORY_AVAILABLE = False

# Import Dual-Core wrapper (TRIPLE-CORE version)
try:
    from triple_core.orchestrators.dual_core_wrapper import DualCoreWrapper
    DUAL_CORE_AVAILABLE = True
except ImportError:
    DUAL_CORE_AVAILABLE = False
    logger.warning("⚠️ DualCoreWrapper not available - using LLM-only mode")

logger = logging.getLogger(__name__)


class ScripturemonSystem:
    """
    Sistema principal Scripturemon com memória integrada
    """

    def __init__(self, use_memory: bool = True, use_dual_core: bool = True):
        """
        Inicializa o sistema

        Args:
            use_memory: Se deve usar enriquecimento com memória
            use_dual_core: Se deve usar arquitetura Dual-Core (Python + LLM)
        """
        self.use_memory = use_memory and ENABLE_MEMORY_ENRICHMENT
        self.use_dual_core = use_dual_core and DUAL_CORE_AVAILABLE

        # Configurar memória se ativada
        if self.use_memory:
            # Use Git-Memory if available, otherwise standard
            if GIT_MEMORY_AVAILABLE:
                self.memory = EnhancedMemorySystem()
                logger.info("🔥 Git-Memory integration ENABLED")
            else:
                self.memory = ScripturemonMemory()
                logger.info("✅ Standard memory ENABLED")

            self.memory_integration = MemoryIntegration(self.memory)
            logger.info(f"📊 Memory stats: {self.memory.get_stats()['total_memories']} itens")
        else:
            self.memory = None
            self.memory_integration = None
            logger.info("✅ Sistema inicializado sem memória")

        # Configurar Dual-Core se disponível
        if self.use_dual_core:
            logger.info("🔥 Dual-Core Architecture ATIVADA (Python + LLM)")
            self.python_specialists = self._load_python_specialists()
        else:
            logger.info("⚠️ LLM-only mode (Dual-Core desativado)")
            self.python_specialists = {}

        # Carregar prompts dos especialistas
        self.specialist_prompts = self._load_specialist_prompts()

        # Estatísticas da sessão
        self.session_stats = {
            'analyses_performed': 0,
            'memory_enrichments': 0,
            'specialists_executed': 0,
            'dual_core_analyses': 0,
            'time_started': datetime.now()
        }

    def _load_python_specialists(self) -> Dict[str, Any]:
        """
        Carrega especialistas Python e envolve em DualCoreWrapper.

        Por enquanto, apenas DrDialogue está disponível.
        Futuramente, carregar todos os 24 especialistas.
        """
        specialists = {}

        try:
            # Carregar DrDialogue (TRIPLE-CORE version)
            from triple_core.core_1_specialists.dialogue.dr_dialogue import DrDialogue

            # Criar especialista Python
            dr_dialogue = DrDialogue()

            # Envolver em DualCoreWrapper
            dual_core_dialogue = DualCoreWrapper(
                python_specialist=dr_dialogue,
                llm_model=ORCHESTRATOR_MODEL,
                llm_timeout=OLLAMA_TIMEOUT,
                fallback_to_python=True
            )

            specialists['01_DIALOGUE'] = dual_core_dialogue
            logger.info(f"✅ DrDialogue carregado em Dual-Core mode (01_DIALOGUE)")

        except Exception as e:
            logger.error(f"❌ Erro ao carregar DrDialogue: {e}")

        # TODO: Carregar demais especialistas Python aqui
        # - DrCharacter (character_psychology_specialist)
        # - DrPacing (pacing_specialist)
        # - DrTheme (theme_specialist)
        # ... (20 especialistas restantes)

        return specialists

    def _load_specialist_prompts(self) -> Dict[str, str]:
        """Carrega prompts dos modelfiles"""
        prompts = {}

        for specialist in SPECIALISTS:
            modelfile_name = SPECIALIST_MODELFILES.get(specialist)
            if not modelfile_name:
                prompts[specialist] = f"You are a specialist in {specialist} analysis."
                continue

            modelfile_path = MODELFILES_DIR / modelfile_name

            # Tentar com nome alternativo se não encontrar
            if not modelfile_path.exists():
                # Mapear para nomes existentes no diretório atual
                alt_names = {
                    "01_dialogue.modelfile": "01_dialogue_ultra.modelfile",
                    "02_character.modelfile": "02_character_ultra.modelfile",
                    "03_pacing.modelfile": "03_pacing_ultra_synthesis.modelfile",
                    "04_theme.modelfile": "04_theme_ultra_synthesis.modelfile",
                    "05_action.modelfile": "05_action_integrated.modelfile",
                    "06_structure.modelfile": "06_structure_ultra_synthesis.modelfile",
                    "07_conflict.modelfile": "07_conflict_integrated.modelfile",
                    "08_tension.modelfile": "08_tension_integrated_ultra.modelfile",
                    "09_subtext.modelfile": "09_subtext_integrated_master.modelfile",
                    "10_exposition.modelfile": "10_exposition_integrated_ultra.modelfile",
                    "11_transitions.modelfile": "11_transitions_integrated_master.modelfile",
                    "12_opening.modelfile": "12_opening_integrated_master.modelfile",
                    "13_climax.modelfile": "13_climax_integrated_ultra.modelfile",
                    "14_resolution.modelfile": "14_resolution_integrated_master.modelfile",
                    "15_worldbuilding.modelfile": "15_worldbuilding_integrated_master.modelfile",
                    "16_stakes.modelfile": "16_stakes_integrated_master.modelfile",
                    "17_motivation.modelfile": "17_motivation_integrated_master.modelfile",
                    "18_backstory.modelfile": "18_backstory_integrated_master.modelfile",
                    "19_foreshadowing.modelfile": "19_foreshadowing_integrated_ultra.modelfile",
                    "20_twist.modelfile": "20_twist_integrated_supreme.modelfile",
                    "21_symbolism.modelfile": "21_symbolism_jung_archetypal.modelfile",
                    "22_tone.modelfile": "22_tone_truby_master.modelfile",
                    "23_genre.modelfile": "23_genre_integrated_ultimate.modelfile",
                    "24_contrast.modelfile": "24_evaluator_70b.modelfile"
                }

                alt_name = alt_names.get(modelfile_name)
                if alt_name:
                    modelfile_path = MODELFILES_DIR / alt_name

            if not modelfile_path.exists():
                logger.warning(f"Modelfile não encontrado: {modelfile_path}")
                prompts[specialist] = f"You are a specialist in {specialist} analysis."
                continue

            try:
                with open(modelfile_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extrair SYSTEM prompt
                if 'SYSTEM """' in content:
                    start = content.find('SYSTEM """') + len('SYSTEM """')
                    end = content.find('"""', start)
                    if end > start:
                        prompts[specialist] = content[start:end].strip()
                    else:
                        prompts[specialist] = f"You are a specialist in {specialist} analysis."
                else:
                    prompts[specialist] = f"You are a specialist in {specialist} analysis."

            except Exception as e:
                logger.error(f"Erro ao carregar {modelfile_path}: {e}")
                prompts[specialist] = f"You are a specialist in {specialist} analysis."

        return prompts

    def analyze(self,
                screenplay_content: str,
                title: str = "Untitled",
                mode: str = "STANDARD") -> str:
        """
        Analisa um roteiro

        Args:
            screenplay_content: Conteúdo do roteiro
            title: Título do roteiro
            mode: Modo de análise (QUICK, STANDARD, COMPLETE)

        Returns:
            Caminho do relatório gerado
        """
        # Selecionar especialistas baseado no modo
        if mode == "QUICK":
            specialists_to_run = QUICK_SPECIALISTS
        elif mode == "STANDARD":
            specialists_to_run = STANDARD_SPECIALISTS
        else:  # COMPLETE
            specialists_to_run = SPECIALISTS

        # Criar arquivo de relatório
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = OUTPUTS_DIR / f"analysis_{title}_{timestamp}.md"

        # Inicializar relatório
        self._initialize_report(report_file, title, timestamp, mode, len(specialists_to_run))

        logger.info(f"\n{'='*60}")
        logger.info(f"🎬 ANALISANDO: {title}")
        logger.info(f"   Modo: {mode} ({len(specialists_to_run)} especialistas)")
        logger.info(f"   Memória: {'Ativada' if self.use_memory else 'Desativada'}")
        logger.info(f"{'='*60}")

        # Executar análises
        self.session_stats['analyses_performed'] += 1
        previous_analyses = ""

        for i, specialist in enumerate(specialists_to_run, 1):
            logger.info(f"\n[{i}/{len(specialists_to_run)}] {specialist}...")

            # Preparar prompt base
            base_prompt = self.specialist_prompts.get(specialist, "")

            # Enriquecer com memória se ativado
            if self.use_memory and self.memory_integration:
                enriched_prompt = self.memory_integration.enrich_specialist_prompt(
                    specialist_name=specialist,
                    screenplay_excerpt=screenplay_content[:1000],
                    base_prompt=base_prompt
                )
                if len(enriched_prompt) > len(base_prompt):
                    self.session_stats['memory_enrichments'] += 1
                    logger.debug(f"   🧠 Enriquecido com memória")
            else:
                enriched_prompt = base_prompt

            # Adicionar contexto das análises anteriores
            if previous_analyses:
                enriched_prompt += f"\n\nPrevious analyses:\n{previous_analyses[:2000]}"

            # Executar análise
            analysis = self._run_specialist(specialist, screenplay_content, enriched_prompt)

            # Armazenar na memória
            if self.use_memory and self.memory:
                self.memory.store_analysis(
                    screenplay_title=title,
                    specialist=specialist,
                    content=analysis,
                    metadata={
                        'timestamp': timestamp,
                        'mode': mode
                    }
                )

            # Adicionar ao relatório
            self._append_to_report(report_file, specialist, analysis)

            # Acumular para contexto
            previous_analyses += f"\n{specialist}: {analysis[:500]}...\n"

            self.session_stats['specialists_executed'] += 1
            logger.info(f"   ✓ Completo")

            time.sleep(0.2)  # Pequena pausa

        # Síntese final se modo COMPLETE
        if mode == "COMPLETE":
            logger.info(f"\n{'='*40}")
            logger.info("🎯 EXECUTANDO SÍNTESE FINAL...")
            logger.info(f"{'='*40}")

            synthesis = self._run_final_synthesis(report_file, screenplay_content)
            self._append_final_synthesis(report_file, synthesis)

        # Adicionar estatísticas
        self._append_statistics(report_file)

        logger.info(f"\n✅ Análise completa!")
        logger.info(f"📄 Relatório: {report_file}")

        if self.use_memory:
            stats = self.memory.get_stats()
            logger.info(f"🧠 Memória: {stats['queries_made']} consultas, {stats['hits']} hits")

        return str(report_file)

    def _initialize_report(self, report_file: Path, title: str, timestamp: str, mode: str, num_specialists: int):
        """Inicializa arquivo de relatório"""
        header = f"""# SCRIPTUREMON ANALYSIS REPORT

**Title:** {title}
**Generated:** {timestamp}
**Mode:** {mode}
**Specialists:** {num_specialists}
**Memory:** {'Enabled' if self.use_memory else 'Disabled'}

---

## ANALYSES

"""
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(header)

    def _run_specialist(self, specialist: str, screenplay: str, prompt: str) -> str:
        """
        Executa análise de um especialista.

        Se Dual-Core estiver ativado E especialista Python existir,
        usa análise Dual-Core (Python + LLM).
        Caso contrário, usa LLM-only tradicional.
        """
        # DUAL-CORE MODE: Verificar se existe especialista Python
        if self.use_dual_core and specialist in self.python_specialists:
            try:
                logger.info(f"🔥 Executando {specialist} em DUAL-CORE mode")

                # Chamar análise Dual-Core
                dual_core_specialist = self.python_specialists[specialist]
                result = dual_core_specialist.analyze(screenplay)

                # Incrementar estatísticas
                self.session_stats['dual_core_analyses'] += 1

                # Formatar resultado Dual-Core para markdown
                formatted_result = self._format_dual_core_result(specialist, result)
                return formatted_result

            except Exception as e:
                logger.error(f"❌ Dual-Core falhou para {specialist}: {e}")
                logger.info(f"⚠️ Fallback para LLM-only mode")
                # Continua para LLM-only abaixo

        # LLM-ONLY MODE (tradicional ou fallback)
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Analyze this screenplay:\n\n{screenplay}"}
        ]

        data = {
            "model": ORCHESTRATOR_MODEL,
            "messages": messages,
            "stream": False,
            "options": MODEL_PARAMS
        }

        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/chat",
                json=data,
                timeout=OLLAMA_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', 'Analysis failed.')
            else:
                return f"Error: Status {response.status_code}"

        except Exception as e:
            logger.error(f"Error in {specialist}: {e}")
            return f"Error: {str(e)}"

    def _format_dual_core_result(self, specialist: str, result: Dict) -> str:
        """
        Formata resultado Dual-Core para markdown.

        Combina análise Python + insights LLM + synthesis.
        """
        output = []

        # Cabeçalho
        output.append(f"**🔥 DUAL-CORE ANALYSIS (Python + LLM) 🔥**\n")

        # Synthesis (resumo combinado)
        if result.get('synthesis'):
            synthesis = result['synthesis']
            output.append(f"**Quality Score:** {synthesis.get('quality_score', 'N/A')}")
            output.append(f"**Methodology:** {synthesis['combined_analysis']['methodology']}\n")

        # LLM Insights (principal conteúdo)
        if result.get('llm_insights'):
            output.append("## LLM Qualitative Insights\n")
            output.append(result['llm_insights'])
            output.append("")

        # Python Metrics (dados estruturais)
        if result.get('python_analysis'):
            output.append("\n## Python Structural Analysis\n")
            python_data = result['python_analysis']

            # Formatar métricas principais
            if isinstance(python_data, dict):
                # Score geral
                if 'score' in python_data:
                    output.append(f"**Overall Score:** {python_data['score']}/100")

                # Métricas específicas (depende do especialista)
                if 'authenticity_score' in python_data:
                    output.append(f"**Authenticity:** {python_data['authenticity_score']:.1f}/100")
                if 'natural_speech_score' in python_data:
                    output.append(f"**Natural Speech:** {python_data['natural_speech_score']:.1f}/100")
                if 'voice_distinctiveness' in python_data:
                    output.append(f"**Voice Distinctiveness:** {python_data['voice_distinctiveness']:.1f}/100")

                # Diagnóstico
                if 'diagnosis' in python_data:
                    output.append(f"\n**Diagnosis:** {python_data['diagnosis']}")

                # Recomendações Python
                if 'recommendations' in python_data and python_data['recommendations']:
                    output.append("\n**Python Recommendations:**")
                    for rec in python_data['recommendations'][:5]:  # Top 5
                        output.append(f"- {rec}")

        return '\n'.join(output)

    def _append_to_report(self, report_file: Path, specialist: str, analysis: str):
        """Adiciona análise ao relatório"""
        section = f"""### {specialist.replace('_', ' ')}

{analysis}

---

"""
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(section)

    def _run_final_synthesis(self, report_file: Path, screenplay: str) -> str:
        """Executa síntese final com modelo avaliador"""
        # Ler todo o relatório
        with open(report_file, 'r', encoding='utf-8') as f:
            full_report = f.read()

        synthesis_prompt = """You are the ULTIMATE SCREENPLAY EVALUATOR.
Based on all specialist analyses, provide:

1. **OVERALL SCORE** (1-100)
2. **KEY STRENGTHS** (Top 3)
3. **KEY WEAKNESSES** (Top 3)
4. **RECOMMENDATIONS** (Top 5 specific actions)
5. **FINAL VERDICT**

Be concise and actionable."""

        messages = [
            {"role": "system", "content": synthesis_prompt},
            {"role": "user", "content": f"Synthesize these analyses:\n\n{full_report}"}
        ]

        data = {
            "model": EVALUATOR_MODEL,
            "messages": messages,
            "stream": False,
            "options": EVALUATOR_PARAMS
        }

        try:
            response = requests.post(
                f"{OLLAMA_HOST}/api/chat",
                json=data,
                timeout=OLLAMA_TIMEOUT_EVALUATOR
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', 'Synthesis failed.')
            else:
                return f"Error: Status {response.status_code}"

        except Exception as e:
            logger.error(f"Error in synthesis: {e}")
            return f"Error: {str(e)}"

    def _append_final_synthesis(self, report_file: Path, synthesis: str):
        """Adiciona síntese final ao relatório"""
        section = f"""

## FINAL SYNTHESIS

{synthesis}

---

"""
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(section)

    def _append_statistics(self, report_file: Path):
        """Adiciona estatísticas ao relatório"""
        duration = (datetime.now() - self.session_stats['time_started']).total_seconds()

        stats_section = f"""

## SESSION STATISTICS

- **Duration:** {duration:.1f} seconds
- **Specialists Executed:** {self.session_stats['specialists_executed']}
- **Memory Enrichments:** {self.session_stats['memory_enrichments']}
"""

        if self.use_memory and self.memory:
            mem_stats = self.memory.get_stats()
            stats_section += f"""- **Memory Queries:** {mem_stats['queries_made']}
- **Memory Hits:** {mem_stats['hits']}
- **Total Memories:** {mem_stats['total_memories']}
"""

        stats_section += """
---

*Generated by Scripturemon Ultimate System*
"""

        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(stats_section)

    def close(self):
        """Fecha conexões"""
        if self.memory:
            self.memory.close()


"""
DIGIMUNDO PRESENTE 🥷
"""