#!/usr/bin/env python3
"""
QUALITY EVALUATOR ULTIMATE - Avaliador Final com Llama 70B/Qwen 72B
Sistema de avaliação e síntese dos 23 especialistas
"""

import json
import logging
import time
import requests
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import subprocess
import re
from dataclasses import dataclass, asdict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SpecialistResult:
    """Resultado de um especialista"""
    name: str
    score: int
    base_citations: int
    technique_bonus: int
    word_count: int
    analysis: str
    timestamp: str

@dataclass
class EvaluationReport:
    """Relatório de avaliação completo"""
    total_specialists: int
    total_score: int
    average_score: float
    top_performers: List[SpecialistResult]
    weak_spots: List[SpecialistResult]
    synthesis: str
    recommendations: List[str]
    timestamp: str

class QualityEvaluatorUltimate:
    """
    Avaliador de qualidade usando Llama 70B ou Qwen 72B
    Analisa os resultados dos 23 especialistas e gera síntese final
    """

    def __init__(self,
                 model_name: str = "qwen2.5:72b",
                 backup_model: str = "llama3.1:70b"):
        """
        Inicializa o avaliador

        Args:
            model_name: Modelo principal (qwen2.5:72b)
            backup_model: Modelo backup (llama3.1:70b)
        """
        self.model_name = model_name
        self.backup_model = backup_model
        self.current_model = None

        # Verificar modelos disponíveis
        self._check_models()

        # Carregar configuração dos especialistas
        self.specialists_config = self._load_specialists_config()

        logger.info(f"✅ Quality Evaluator Ultimate initialized")
        logger.info(f"   Primary model: {self.current_model}")
        logger.info(f"   Specialists to evaluate: 23")

    def _check_models(self):
        """Verifica modelos disponíveis e seleciona o melhor"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True
            )

            available_models = result.stdout.lower()

            # Tentar modelo principal
            if self.model_name.lower() in available_models:
                self.current_model = self.model_name
                logger.info(f"✅ Using primary model: {self.model_name}")
            # Tentar modelo backup
            elif self.backup_model.lower() in available_models:
                self.current_model = self.backup_model
                logger.info(f"⚠️ Primary model not found, using backup: {self.backup_model}")
            else:
                # Tentar qualquer modelo grande disponível
                large_models = ["mixtral", "llama2:70b", "yi:34b", "deepseek"]
                for model in large_models:
                    if model in available_models:
                        self.current_model = model
                        logger.warning(f"⚠️ Using alternative model: {model}")
                        break

                if not self.current_model:
                    logger.error("❌ No suitable large model found!")
                    logger.info("💡 Install with: ollama pull qwen2.5:72b")
                    self.current_model = "mixtral:8x7b"  # Fallback

        except Exception as e:
            logger.error(f"Error checking models: {e}")
            self.current_model = "mixtral:8x7b"  # Fallback

    def _load_specialists_config(self) -> Dict[str, Dict]:
        """Carrega configuração dos 23 especialistas"""
        specialists_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate/super_specialists")

        specialists = {}

        # Lista dos 23 especialistas na ordem
        specialist_names = [
            "DIALOGUE", "CHARACTER", "PACING", "THEME", "ACTION",
            "STRUCTURE", "CONFLICT", "TENSION", "SUBTEXT", "EXPOSITION",
            "TRANSITIONS", "OPENING", "CLIMAX", "RESOLUTION", "WORLD-BUILDING",
            "STAKES", "MOTIVATION", "BACKSTORY", "FORESHADOWING", "TWIST",
            "SYMBOLISM", "TONE", "GENRE"
        ]

        for i, name in enumerate(specialist_names, 1):
            # Procurar arquivo do especialista
            pattern = f"{i:02d}_{name}_*.md"
            files = list(specialists_dir.glob(pattern))

            if files:
                file_path = files[0]
                # Extrair informações do arquivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extrair score usando regex
                score_match = re.search(r'Score[:\s]+(\d+)\s+pontos', content)
                score = int(score_match.group(1)) if score_match else 0

                specialists[name] = {
                    "number": i,
                    "file": str(file_path),
                    "score": score,
                    "exists": True
                }
            else:
                specialists[name] = {
                    "number": i,
                    "file": None,
                    "score": 0,
                    "exists": False
                }

        return specialists

    def evaluate_specialist(self,
                           specialist_name: str,
                           script_content: str) -> SpecialistResult:
        """
        Avalia um especialista específico

        Args:
            specialist_name: Nome do especialista
            script_content: Conteúdo do script para análise

        Returns:
            Resultado da avaliação
        """
        if specialist_name not in self.specialists_config:
            logger.error(f"Specialist {specialist_name} not found")
            return None

        config = self.specialists_config[specialist_name]

        if not config["exists"]:
            logger.warning(f"Specialist {specialist_name} file not found")
            return SpecialistResult(
                name=specialist_name,
                score=0,
                base_citations=0,
                technique_bonus=0,
                word_count=0,
                analysis="Specialist not available",
                timestamp=datetime.now().isoformat()
            )

        # Ler prompt do especialista
        with open(config["file"], 'r', encoding='utf-8') as f:
            specialist_content = f.read()

        # Extrair prompt system
        prompt_match = re.search(r'## PROMPT SYSTEM\n\n(.*?)\n\n===', specialist_content, re.DOTALL)
        if not prompt_match:
            prompt_match = re.search(r'## PROMPT SYSTEM\n\n(.*?)$', specialist_content, re.DOTALL)

        specialist_prompt = prompt_match.group(1) if prompt_match else ""

        # Executar análise com o modelo
        analysis = self._run_analysis(specialist_prompt, script_content)

        # Calcular scores
        scores = self._calculate_scores(analysis)

        return SpecialistResult(
            name=specialist_name,
            score=scores["total"],
            base_citations=scores["citations"],
            technique_bonus=scores["techniques"],
            word_count=len(analysis.split()),
            analysis=analysis,
            timestamp=datetime.now().isoformat()
        )

    def _run_analysis(self, system_prompt: str, content: str) -> str:
        """
        Executa análise com o modelo

        Args:
            system_prompt: Prompt do sistema
            content: Conteúdo para análise

        Returns:
            Texto da análise
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this screenplay:\n\n{content}"}
        ]

        data = {
            "model": self.current_model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 4000,
                "num_ctx": 131072  # Contexto grande para modelo 70B
            }
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=data,
                timeout=1000  # 1000 segundos para modelo grande
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', '')
            else:
                logger.error(f"Model returned status {response.status_code}")
                return ""

        except Exception as e:
            logger.error(f"Error running analysis: {e}")
            return ""

    def _calculate_scores(self, analysis: str) -> Dict[str, int]:
        """
        Calcula scores baseado na análise

        Args:
            analysis: Texto da análise

        Returns:
            Dicionário com scores
        """
        # Contar citações de teóricos
        theorists = [
            'mckee', 'truby', 'field', 'snyder', 'vogler', 'campbell',
            'aristotle', 'hitchcock', 'kubrick', 'lynch', 'fincher',
            'nolan', 'spielberg', 'scorsese', 'coen', 'tarkovsky',
            'shakespeare', 'jung', 'freud', 'stanislavski'
        ]

        citations = 0
        for theorist in theorists:
            citations += len(re.findall(rf'(?i)\b{theorist}\b', analysis))

        # Contar técnicas específicas (simplificado)
        techniques = len(re.findall(r'(?i)(technique|method|approach|strategy|principle)', analysis))
        technique_bonus = techniques * 2

        return {
            "citations": citations,
            "techniques": technique_bonus,
            "total": citations + technique_bonus
        }

    def evaluate_all_specialists(self, script_content: str) -> List[SpecialistResult]:
        """
        Avalia todos os 23 especialistas

        Args:
            script_content: Conteúdo do script

        Returns:
            Lista com todos os resultados
        """
        results = []

        logger.info("Starting evaluation of all 23 specialists...")

        for name, config in self.specialists_config.items():
            logger.info(f"Evaluating {config['number']:02d}. {name}...")
            result = self.evaluate_specialist(name, script_content)
            if result:
                results.append(result)
                logger.info(f"   Score: {result.score} points")

            # Pequena pausa para não sobrecarregar
            time.sleep(1)

        # Ordenar por score
        results.sort(key=lambda x: x.score, reverse=True)

        return results

    def generate_synthesis(self,
                         results: List[SpecialistResult],
                         script_content: str) -> str:
        """
        Gera síntese final dos resultados

        Args:
            results: Lista de resultados dos especialistas
            script_content: Conteúdo original do script

        Returns:
            Síntese final
        """
        # Preparar contexto para síntese
        context = {
            "total_specialists": len(results),
            "total_score": sum(r.score for r in results),
            "average_score": sum(r.score for r in results) / len(results) if results else 0,
            "top_3": results[:3] if len(results) >= 3 else results,
            "bottom_3": results[-3:] if len(results) >= 3 else [],
        }

        synthesis_prompt = f"""
You are the ULTIMATE SCREENPLAY EVALUATOR synthesizing insights from 23 specialist analyses.

CONTEXT:
- Total Specialists Evaluated: {context['total_specialists']}
- Combined Score: {context['total_score']} points
- Average Score: {context['average_score']:.1f} points

TOP PERFORMERS:
{chr(10).join([f"- {r.name}: {r.score} points" for r in context['top_3']])}

WEAKEST AREAS:
{chr(10).join([f"- {r.name}: {r.score} points" for r in context['bottom_3']])}

Based on all specialist analyses, provide:

1. OVERALL QUALITY ASSESSMENT
   - Strengths of the screenplay
   - Weaknesses identified
   - Unique elements

2. CRITICAL INSIGHTS
   - Most important findings from top specialists
   - Patterns across multiple analyses
   - Contradictions or tensions

3. ACTIONABLE RECOMMENDATIONS
   - Top 5 specific improvements
   - Priority areas for revision
   - Elements to preserve

4. MARKET POTENTIAL
   - Genre positioning
   - Target audience
   - Comparable successful films

5. FINAL VERDICT
   - Overall score (1-100)
   - Recommendation (Pass/Consider/Recommend/Strong Recommend)
   - One-line summary

Be specific, reference the specialist findings, and provide professional-grade evaluation.
"""

        synthesis = self._run_analysis(synthesis_prompt, script_content)

        return synthesis

    def generate_full_report(self,
                           script_content: str,
                           output_file: Optional[str] = None) -> EvaluationReport:
        """
        Gera relatório completo de avaliação

        Args:
            script_content: Conteúdo do script
            output_file: Arquivo para salvar o relatório (opcional)

        Returns:
            Relatório completo
        """
        logger.info("=" * 60)
        logger.info("STARTING ULTIMATE QUALITY EVALUATION")
        logger.info("=" * 60)

        # Avaliar todos os especialistas
        results = self.evaluate_all_specialists(script_content)

        # Gerar síntese
        logger.info("Generating final synthesis with 70B model...")
        synthesis = self.generate_synthesis(results, script_content)

        # Extrair recomendações da síntese
        recommendations = self._extract_recommendations(synthesis)

        # Criar relatório
        report = EvaluationReport(
            total_specialists=len(results),
            total_score=sum(r.score for r in results),
            average_score=sum(r.score for r in results) / len(results) if results else 0,
            top_performers=results[:5],
            weak_spots=results[-5:] if len(results) >= 5 else results,
            synthesis=synthesis,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat()
        )

        # Salvar relatório se solicitado
        if output_file:
            self._save_report(report, output_file)

        # Exibir resumo
        self._display_summary(report)

        return report

    def _extract_recommendations(self, synthesis: str) -> List[str]:
        """Extrai recomendações da síntese"""
        recommendations = []

        # Procurar seção de recomendações
        rec_match = re.search(r'RECOMMENDATIONS?:?\s*(.*?)(?:MARKET|VERDICT|$)', synthesis, re.DOTALL | re.IGNORECASE)
        if rec_match:
            rec_text = rec_match.group(1)
            # Extrair items numerados ou com bullets
            items = re.findall(r'(?:[-•*]|\d+\.)\s*(.+?)(?:\n|$)', rec_text)
            recommendations = [item.strip() for item in items[:5]]

        return recommendations

    def _save_report(self, report: EvaluationReport, filename: str):
        """Salva relatório em arquivo"""
        output_path = Path(filename)

        # Criar diretório se não existir
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Preparar conteúdo
        content = f"""# SCRIPTUREMON ULTIMATE - EVALUATION REPORT
Generated: {report.timestamp}

## EXECUTIVE SUMMARY
- **Total Score**: {report.total_score} points
- **Average Score**: {report.average_score:.1f} points
- **Specialists Evaluated**: {report.total_specialists}/23

## TOP PERFORMERS
{chr(10).join([f"{i+1}. **{r.name}**: {r.score} points" for i, r in enumerate(report.top_performers)])}

## AREAS FOR IMPROVEMENT
{chr(10).join([f"- {r.name}: {r.score} points" for r in report.weak_spots])}

## SYNTHESIS
{report.synthesis}

## KEY RECOMMENDATIONS
{chr(10).join([f"{i+1}. {rec}" for i, rec in enumerate(report.recommendations)])}

---
*Scripturemon Ultimate - Professional Screenplay Analysis System*
"""

        # Salvar arquivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"📄 Report saved to: {output_path}")

    def _display_summary(self, report: EvaluationReport):
        """Exibe resumo do relatório"""
        print("\n" + "=" * 60)
        print("EVALUATION COMPLETE")
        print("=" * 60)
        print(f"Total Score: {report.total_score} points")
        print(f"Average Score: {report.average_score:.1f} points")
        print(f"\nTop 3 Specialists:")
        for i, r in enumerate(report.top_performers[:3], 1):
            print(f"  {i}. {r.name}: {r.score} points")
        print(f"\nKey Recommendations:")
        for i, rec in enumerate(report.recommendations[:3], 1):
            print(f"  {i}. {rec}")
        print("=" * 60)


def main():
    """Função principal para testes"""
    import sys

    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Usage: python quality_evaluator_ultimate.py <screenplay_file>")
        sys.exit(1)

    screenplay_file = sys.argv[1]

    # Ler conteúdo do script
    try:
        with open(screenplay_file, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Criar avaliador
    evaluator = QualityEvaluatorUltimate()

    # Gerar relatório
    output_file = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report = evaluator.generate_full_report(script_content, output_file)

    print(f"\n✅ Evaluation complete! Report saved to: {output_file}")


if __name__ == "__main__":
    main()