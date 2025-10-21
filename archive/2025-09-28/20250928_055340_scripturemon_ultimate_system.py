#!/usr/bin/env python3
"""
SCRIPTUREMON ULTIMATE SYSTEM
Sistema completo de análise sequencial com arquivo único
Orchestrator → 23 Specialists (sequencial) → 70B Evaluator
"""

import json
import logging
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScripturemonUltimateSystem:
    """
    Sistema completo de análise de roteiros
    Execução sequencial com arquivo único acumulativo
    """

    def __init__(self,
                 orchestrator_model: str = "mixtral:8x7b-instruct-v0.1-q5_K_M",
                 evaluator_model: str = "llama3.1:70b-instruct-q4_K_M",
                 output_dir: str = "analysis_reports"):
        """
        Inicializa o sistema

        Args:
            orchestrator_model: Modelo para orchestrator e especialistas
            evaluator_model: Modelo 70B para avaliação final
            output_dir: Diretório para salvar relatórios
        """
        self.orchestrator_model = orchestrator_model
        self.evaluator_model = evaluator_model
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Lista ordenada dos 23 especialistas
        self.specialists = [
            "01_DIALOGUE",
            "02_CHARACTER",
            "03_PACING",
            "04_THEME",
            "05_ACTION",
            "06_STRUCTURE",
            "07_CONFLICT",
            "08_TENSION",
            "09_SUBTEXT",
            "10_EXPOSITION",
            "11_TRANSITIONS",
            "12_OPENING",
            "13_CLIMAX",
            "14_RESOLUTION",
            "15_WORLD-BUILDING",
            "16_STAKES",
            "17_MOTIVATION",
            "18_BACKSTORY",
            "19_FORESHADOWING",
            "20_TWIST",
            "21_SYMBOLISM",
            "22_TONE",
            "23_GENRE"
        ]

        # Carregar prompts dos especialistas
        self.specialist_prompts = self._load_specialist_prompts()

        logger.info("✅ Scripturemon Ultimate System initialized")
        logger.info(f"   Orchestrator: {orchestrator_model}")
        logger.info(f"   Evaluator: {evaluator_model}")
        logger.info(f"   Specialists: {len(self.specialists)}")

    def _load_specialist_prompts(self) -> Dict[str, str]:
        """Carrega os prompts dos especialistas"""
        prompts = {}
        specialists_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists")

        for specialist in self.specialists:
            # Extrair número e nome
            num, name = specialist.split("_", 1)

            # Procurar arquivo do especialista
            # Ajustar nome para WORLDBUILDING sem hífen
            search_name = name.replace("-", "")
            pattern = f"{num}_{search_name}_*.md"
            files = list(specialists_dir.glob(pattern))

            # Se não encontrar, tentar com nome original
            if not files:
                pattern = f"{num}_{name}_*.md"
                files = list(specialists_dir.glob(pattern))

            if files:
                with open(files[0], 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extrair prompt system
                prompt_match = re.search(r'## PROMPT SYSTEM\n\n(.*?)(?:\n===|\n##|$)', content, re.DOTALL)
                if prompt_match:
                    prompts[specialist] = prompt_match.group(1)
                    logger.info(f"   Loaded prompt for {specialist}")
                else:
                    logger.warning(f"   Could not extract prompt for {specialist}")
                    prompts[specialist] = f"You are a specialist in {name.lower()} analysis."
            else:
                logger.warning(f"   File not found for {specialist}")
                prompts[specialist] = f"You are a specialist in {name.lower()} analysis."

        return prompts

    def analyze_screenplay(self, screenplay_content: str, title: str = "Untitled") -> str:
        """
        Analisa um roteiro completo

        Args:
            screenplay_content: Conteúdo do roteiro
            title: Título do roteiro

        Returns:
            Path do arquivo de relatório gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"analysis_{title}_{timestamp}.md"

        # Inicializar relatório
        self._initialize_report(report_file, title, timestamp)

        logger.info(f"\n{'='*60}")
        logger.info(f"STARTING ANALYSIS: {title}")
        logger.info(f"{'='*60}")

        # Executar análise sequencial
        previous_analyses = ""

        for i, specialist in enumerate(self.specialists, 1):
            logger.info(f"\n[{i}/23] Running {specialist}...")

            # Preparar contexto (análises anteriores se houver)
            context = self._prepare_context(previous_analyses, i > 1)

            # Executar análise do especialista
            analysis = self._run_specialist(
                specialist,
                screenplay_content,
                context
            )

            # Adicionar ao relatório
            self._append_to_report(report_file, specialist, analysis)

            # Acumular para próximo especialista
            previous_analyses += f"\n\n## {specialist}\n{analysis}"

            logger.info(f"   ✓ Complete ({len(analysis.split())} words)")

            # Pequena pausa para não sobrecarregar
            time.sleep(0.5)

        # Executar avaliação final com 70B
        logger.info(f"\n{'='*40}")
        logger.info("RUNNING FINAL EVALUATION WITH 70B MODEL")
        logger.info(f"{'='*40}")

        final_synthesis = self._run_final_evaluation(report_file, screenplay_content)

        # Adicionar síntese final ao relatório
        self._append_final_synthesis(report_file, final_synthesis)

        logger.info(f"\n✅ Analysis complete! Report saved to: {report_file}")

        return str(report_file)

    def _initialize_report(self, report_file: Path, title: str, timestamp: str):
        """Inicializa o arquivo de relatório"""
        header = f"""# SCRIPTUREMON ULTIMATE ANALYSIS REPORT

**Title**: {title}
**Generated**: {timestamp}
**System**: Scripturemon Ultimate v1.0

---

## EXECUTIVE SUMMARY

*[Will be added after all analyses are complete]*

---

## SPECIALIST ANALYSES

"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(header)

    def _prepare_context(self, previous_analyses: str, has_previous: bool) -> str:
        """Prepara contexto para especialista"""
        if not has_previous:
            return ""

        context = f"""
CONTEXT: Previous specialists have analyzed this screenplay. You may reference, agree with, or respectfully disagree with their findings.

PREVIOUS ANALYSES SUMMARY:
{previous_analyses[:2000]}...  # Limitado para não ficar muito grande

You should:
1. Focus on YOUR specialty
2. Reference other analyses when relevant
3. Point out agreements or disagreements
4. Add unique insights from your perspective
"""
        return context

    def _run_specialist(self,
                       specialist: str,
                       screenplay: str,
                       context: str) -> str:
        """Executa análise de um especialista"""

        system_prompt = self.specialist_prompts.get(specialist, "")

        # Adicionar contexto se houver
        if context:
            system_prompt += f"\n\n{context}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this screenplay:\n\n{screenplay}"}
        ]

        data = {
            "model": self.orchestrator_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1500,  # Limitado para cada especialista
                "num_ctx": 32768
            }
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', 'Analysis failed.')
            else:
                return f"Error: Status {response.status_code}"

        except Exception as e:
            logger.error(f"Error in {specialist}: {e}")
            return f"Error: {str(e)}"

    def _append_to_report(self, report_file: Path, specialist: str, analysis: str):
        """Adiciona análise ao relatório"""
        section = f"""
### {specialist.replace('_', ' ')}

{analysis}

---
"""
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(section)

    def _run_final_evaluation(self, report_file: Path, screenplay: str) -> str:
        """Executa avaliação final com modelo 70B"""

        # Ler todo o relatório
        with open(report_file, 'r', encoding='utf-8') as f:
            full_report = f.read()

        synthesis_prompt = """You are the ULTIMATE SCREENPLAY EVALUATOR reviewing analyses from 23 specialists.

Your task is to synthesize all insights into a professional, actionable evaluation.

Based on the 23 specialist analyses, provide:

1. **OVERALL ASSESSMENT** (Score: 1-100)
   - Core strengths identified across analyses
   - Critical weaknesses consensus
   - Unique elements noted

2. **SYNTHESIS OF KEY FINDINGS**
   - Where specialists agree
   - Where specialists disagree (and your verdict)
   - Most important insights

3. **ACTIONABLE RECOMMENDATIONS**
   - Top 5 specific improvements needed
   - Elements to preserve
   - Priority revision areas

4. **MARKET ANALYSIS**
   - Genre positioning
   - Comparable successful films
   - Target audience
   - Commercial potential

5. **FINAL VERDICT**
   - Pass / Consider / Recommend / Strong Recommend
   - One-line pitch
   - Executive summary (3 sentences max)

Be specific, reference specialist findings by name, and provide professional-grade conclusions."""

        messages = [
            {"role": "system", "content": synthesis_prompt},
            {"role": "user", "content": f"Here are the 23 analyses:\n\n{full_report}\n\nProvide your final synthesis."}
        ]

        data = {
            "model": self.evaluator_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 3000,
                "num_ctx": 131072  # Grande contexto para 70B
            }
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=1000  # 1000 segundos para 70B
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', 'Synthesis failed.')
            else:
                return f"Error: Status {response.status_code}"

        except Exception as e:
            logger.error(f"Error in final evaluation: {e}")
            return f"Error: {str(e)}"

    def _append_final_synthesis(self, report_file: Path, synthesis: str):
        """Adiciona síntese final ao relatório"""

        # Atualizar executive summary no início
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Substituir placeholder do executive summary
        content = content.replace(
            "*[Will be added after all analyses are complete]*",
            synthesis[:500] + "..."  # Primeiras linhas da síntese
        )

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Adicionar síntese completa no final
        final_section = f"""

---

## FINAL EVALUATION (LLAMA 70B SYNTHESIS)

{synthesis}

---

**END OF REPORT**

*Generated by Scripturemon Ultimate System*
*23 Specialists + Llama 70B Synthesis*
"""
        with open(report_file, 'a', encoding='utf-8') as f:
            f.write(final_section)


def main():
    """Função principal para testes"""
    import sys

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Usage: python scripturemon_ultimate_system.py <screenplay_file> [title]")
        sys.exit(1)

    screenplay_file = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else Path(screenplay_file).stem

    # Ler screenplay
    try:
        with open(screenplay_file, 'r', encoding='utf-8') as f:
            screenplay_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Criar sistema e analisar
    system = ScripturemonUltimateSystem()
    report_file = system.analyze_screenplay(screenplay_content, title)

    print(f"\n✅ Success! Report saved to: {report_file}")


if __name__ == "__main__":
    main()