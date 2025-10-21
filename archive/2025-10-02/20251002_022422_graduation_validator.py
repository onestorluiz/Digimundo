#!/usr/bin/env python3
"""
Script Doctor Graduation Validator
Sistema completo de validação em 3 camadas
"""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from .specificity_calculator import SpecificityScoreCalculator
from .depth_calculator import DepthScoreCalculator


# Critérios técnicos (Camada 1)
TECHNICAL_CRITERIA = {
    'llm_success': {
        'test': lambda r: r.get('llm_success', False) == True,
        'weight': 'mandatory',
        'description': 'LLM executou sem erros'
    },
    'substantial_analysis': {
        'test': lambda r: len(r.get('llm_insights', '')) > 2000,
        'weight': 'mandatory',
        'threshold': 2000,
        'description': 'Análise com mínimo de 2000 caracteres'
    },
    'structure_adequate': {
        'test': lambda r: r.get('structure_score', 0) >= 3,
        'weight': 'mandatory',
        'threshold': 3,
        'max': 5,
        'description': 'Estrutura V4.1 com pelo menos 3/5 seções'
    },
    'quality_score': {
        'test': lambda r: r.get('quality_score', 0) >= 0.9,
        'weight': 'mandatory',
        'threshold': 0.9,
        'description': 'Python synthesis quality score ≥ 0.9'
    },
    'acceptable_time': {
        'test': lambda r: r.get('elapsed', 999) < 300,
        'weight': 'mandatory',
        'threshold': 300,
        'unit': 'seconds',
        'description': 'Tempo de execução < 5 minutos'
    }
}


class ScriptDoctorGraduationValidator:
    """Sistema completo de validação de graduação."""

    def __init__(self, screenplay_path: str, specialist_type: str):
        """
        Inicializa validator.

        Args:
            screenplay_path: Caminho para o roteiro
            specialist_type: Tipo do especialista
        """
        self.screenplay_path = Path(screenplay_path)
        self.specialist_type = specialist_type

        # Carrega roteiro
        self.screenplay = self._load_screenplay()

        # Inicializa calculadoras
        self.specificity_calc = SpecificityScoreCalculator(self.screenplay)
        self.depth_calc = DepthScoreCalculator(specialist_type)

    def _load_screenplay(self) -> str:
        """Carrega texto do roteiro."""
        if not self.screenplay_path.exists():
            raise FileNotFoundError(f"Screenplay not found: {self.screenplay_path}")

        return self.screenplay_path.read_text(encoding='utf-8', errors='ignore')

    def _validate_technical_criteria(self, result: Dict) -> Dict[str, Any]:
        """Valida critérios técnicos da Camada 1."""
        criteria_results = {}
        all_passed = True

        for criterion, config in TECHNICAL_CRITERIA.items():
            passed = config['test'](result)
            criteria_results[criterion] = {
                'passed': passed,
                'description': config['description']
            }
            if not passed:
                all_passed = False

        return {
            'all_passed': all_passed,
            'criteria': criteria_results
        }

    def _calculate_final_score(
        self,
        layer1: Dict,
        layer2: Dict,
        layer3: Dict
    ) -> Dict[str, Any]:
        """Calcula score final combinando as 3 camadas."""
        # Camada 1 é pass/fail (peso 20%)
        layer1_score = 1.0 if layer1['all_passed'] else 0.0

        # Camada 2 é score 0-1 (peso 40%)
        layer2_score = layer2['final_score']

        # Camada 3 é score 0-1 (peso 40%)
        layer3_score = layer3['final_score']

        # Média ponderada
        weighted_score = (
            layer1_score * 0.20 +
            layer2_score * 0.40 +
            layer3_score * 0.40
        )

        return {
            'weighted_score': weighted_score,
            'percentage': weighted_score * 100,
            'components': {
                'technical': layer1_score,
                'specificity': layer2_score,
                'depth': layer3_score
            },
            'weights': {
                'technical': 0.20,
                'specificity': 0.40,
                'depth': 0.40
            }
        }

    def _make_graduation_decision(
        self,
        layer1: Dict,
        layer2: Dict,
        layer3: Dict,
        final_score: Dict
    ) -> Dict[str, Any]:
        """Determina se especialista gradua."""
        # Requisitos absolutos
        must_pass_technical = layer1['all_passed']
        must_pass_specificity = layer2['passed']
        must_pass_depth = layer3['passed']

        # Score mínimo
        minimum_final_score = 0.65  # 65%

        # Decisão
        can_graduate = (
            must_pass_technical and
            must_pass_specificity and
            must_pass_depth and
            final_score['weighted_score'] >= minimum_final_score
        )

        # Classificação
        score = final_score['weighted_score']
        if score >= 0.90:
            classification = 'EXCELLENT'
            tier = 'A'
        elif score >= 0.80:
            classification = 'VERY_GOOD'
            tier = 'A-'
        elif score >= 0.70:
            classification = 'GOOD'
            tier = 'B+'
        elif score >= 0.65:
            classification = 'PASSING'
            tier = 'B'
        elif score >= 0.50:
            classification = 'WEAK'
            tier = 'C'
        else:
            classification = 'FAILING'
            tier = 'D'

        # Feedback
        feedback = self._generate_feedback(layer1, layer2, layer3)

        return {
            'approved': can_graduate,
            'classification': classification,
            'tier': tier,
            'final_score': final_score['percentage'],
            'requirements': {
                'technical_passed': must_pass_technical,
                'specificity_passed': must_pass_specificity,
                'depth_passed': must_pass_depth,
                'minimum_score_met': final_score['weighted_score'] >= minimum_final_score
            },
            'feedback': feedback
        }

    def _generate_feedback(
        self,
        layer1: Dict,
        layer2: Dict,
        layer3: Dict
    ) -> Dict[str, Any]:
        """Gera feedback detalhado."""
        strengths = []
        weaknesses = []
        recommendations = []

        # Análise de Layer 2 (Especificidade)
        spec = layer2['components']

        if spec['scene_citations']['score'] >= 0.8:
            strengths.append("Excellent scene citations")
        elif spec['scene_citations']['score'] < 0.6:
            weaknesses.append("Insufficient scene citations")
            recommendations.append(
                f"Add more specific scene references (current: {spec['scene_citations']['count']}, "
                f"minimum: 3, recommended: 5+)"
            )

        if spec['dialogue_quotes']['score'] >= 0.8:
            strengths.append("Strong dialogue quotes")
        elif spec['dialogue_quotes']['score'] < 0.6:
            weaknesses.append("Lacks dialogue quotes")
            recommendations.append(
                f"Include exact dialogue quotes from screenplay (current: {spec['dialogue_quotes']['count']}, "
                f"minimum: 2, recommended: 4+)"
            )

        if spec['character_names']['score'] >= 0.8:
            strengths.append("Good use of character names")
        elif spec['character_names']['score'] < 0.6:
            weaknesses.append("Insufficient use of character names")
            recommendations.append(
                f"Use specific character names more (current: {spec['character_names']['count']}, "
                f"minimum: 5, recommended: 10+)"
            )

        # Penalidades
        if layer2['penalties']['placeholders']['count'] > 0:
            weaknesses.append(f"Contains {layer2['penalties']['placeholders']['count']} placeholders")
            recommendations.append("Remove all placeholders like '[insert example here]'")

        # Análise de Layer 3 (Profundidade)
        depth = layer3['components']

        if depth['expertise']['total_score'] >= 0.7:
            strengths.append("Demonstrates specialist expertise")
        elif depth['expertise']['total_score'] < 0.5:
            weaknesses.append("Lacks specialist expertise")
            recommendations.append(
                f"Focus more on {self.specialist_type}-specific analysis"
            )

        if depth['theory_application']['application_ratio'] >= 0.6:
            strengths.append("Applies theory effectively")
        elif depth['theory_application']['application_ratio'] < 0.5:
            weaknesses.append("Cites theory but doesn't apply it")
            recommendations.append(
                "Connect theoretical concepts to specific screenplay examples"
            )

        if depth['interconnections']['has_depth_section'] and depth['interconnections']['connection_score'] >= 0.5:
            strengths.append("Shows problem interconnections")
        elif not depth['interconnections']['has_depth_section']:
            weaknesses.append("Missing DEPTH & SYNTHESIS section")
            recommendations.append("Add DEPTH & SYNTHESIS section connecting problems")
        elif depth['interconnections']['connection_score'] < 0.4:
            weaknesses.append("Weak problem interconnections")
            recommendations.append("Show how problems relate to each other causally")

        if depth['actionability']['actionability_score'] >= 0.7:
            strengths.append("Provides actionable solutions")
        elif depth['actionability']['actionability_score'] < 0.6:
            weaknesses.append("Solutions are too vague")
            recommendations.append(
                "Make solutions more specific with concrete rewrites/changes"
            )

        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': recommendations
        }

    def validate(self, result: Dict) -> Dict[str, Any]:
        """
        Executa validação completa em 3 camadas.

        Args:
            result: Resultado da graduação (dict com llm_insights, etc)

        Returns:
            Dict completo com validação
        """
        analysis_text = result.get('llm_insights', '')

        # CAMADA 1: Critérios Técnicos (Pass/Fail)
        layer1 = self._validate_technical_criteria(result)

        # CAMADA 2: Especificidade (Score 0-100)
        layer2 = self.specificity_calc.calculate(analysis_text)

        # CAMADA 3: Profundidade (Score 0-100)
        layer3 = self.depth_calc.calculate(analysis_text)

        # Score Final
        final_score = self._calculate_final_score(layer1, layer2, layer3)

        # Decisão de Graduação
        graduation_decision = self._make_graduation_decision(
            layer1, layer2, layer3, final_score
        )

        return {
            'layer1_technical': layer1,
            'layer2_specificity': layer2,
            'layer3_depth': layer3,
            'final_score': final_score,
            'graduation': graduation_decision,
            'metadata': {
                'specialist_type': self.specialist_type,
                'analysis_length': len(analysis_text),
                'screenplay_path': str(self.screenplay_path),
                'timestamp': result.get('timestamp', datetime.now().timestamp())
            }
        }

    def generate_report(self, validation_result: Dict) -> str:
        """Gera relatório legível de validação."""
        grad = validation_result['graduation']
        l1 = validation_result['layer1_technical']
        l2 = validation_result['layer2_specificity']
        l3 = validation_result['layer3_depth']
        meta = validation_result['metadata']

        report = f"""
{'='*80}
🎓 SCRIPT DOCTOR GRADUATION VALIDATION REPORT
{'='*80}

Specialist: {meta['specialist_type']}
Analysis Length: {meta['analysis_length']} characters
Screenplay: {Path(meta['screenplay_path']).name}
Date: {datetime.fromtimestamp(meta['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
FINAL DECISION: {'✅ APPROVED' if grad['approved'] else '❌ NOT APPROVED'}
{'='*80}

Classification: {grad['classification']}
Tier: {grad['tier']}
Final Score: {grad['final_score']:.1f}%

Requirements Met:
  {'✅' if grad['requirements']['technical_passed'] else '❌'} Technical Criteria
  {'✅' if grad['requirements']['specificity_passed'] else '❌'} Specificity Threshold (60%)
  {'✅' if grad['requirements']['depth_passed'] else '❌'} Depth Threshold (60%)
  {'✅' if grad['requirements']['minimum_score_met'] else '❌'} Final Score (65%)

{'='*80}
LAYER 1: TECHNICAL CRITERIA (Pass/Fail)
{'='*80}

Status: {'✅ PASSED' if l1['all_passed'] else '❌ FAILED'}

"""
        for criterion, result in l1['criteria'].items():
            status = '✅' if result['passed'] else '❌'
            report += f"  {status} {result['description']}\n"

        report += f"""
{'='*80}
LAYER 2: SPECIFICITY SCORE
{'='*80}

Final Score: {l2['final_score']:.2f} / 1.00 ({l2['percentage']:.1f}%)
Status: {'✅ PASSED' if l2['passed'] else '❌ FAILED'} (threshold: 0.60)

Components:
"""
        for comp, data in l2['components'].items():
            if 'count' in data:
                report += f"  • {comp}: {data['count']} found (score: {data['score']:.2f}, weight: {data['weight']:.0%})\n"
            else:
                report += f"  • {comp}: score {data['score']:.2f} (weight: {data['weight']:.0%})\n"

        report += f"""
Penalties:
  • Placeholders: {l2['penalties']['placeholders']['penalty']:.2f} ({l2['penalties']['placeholders']['count']} found)
  • Genericity: {l2['penalties']['genericity']['penalty']:.2f}

{'='*80}
LAYER 3: DEPTH SCORE
{'='*80}

Final Score: {l3['final_score']:.2f} / 1.00 ({l3['percentage']:.1f}%)
Status: {'✅ PASSED' if l3['passed'] else '❌ FAILED'} (threshold: 0.60)

Components:
  • Expertise: {l3['components']['expertise']['total_score']:.2f} (weight: {l3['weights']['expertise']:.0%})
  • Theory Application: {l3['components']['theory_application']['application_ratio']:.2f} (weight: {l3['weights']['theory_application']:.0%})
  • Interconnections: {l3['components']['interconnections']['connection_score']:.2f} (weight: {l3['weights']['interconnections']:.0%})
  • Actionability: {l3['components']['actionability']['actionability_score']:.2f} (weight: {l3['weights']['actionability']:.0%})

{'='*80}
FINAL SCORE BREAKDOWN
{'='*80}

Technical (20%):    {validation_result['final_score']['components']['technical']:.2f}
Specificity (40%):  {validation_result['final_score']['components']['specificity']:.2f}
Depth (40%):        {validation_result['final_score']['components']['depth']:.2f}

Weighted Score:     {validation_result['final_score']['weighted_score']:.2f}
Percentage:         {validation_result['final_score']['percentage']:.1f}%

{'='*80}
FEEDBACK
{'='*80}

✅ STRENGTHS:
"""
        for strength in grad['feedback']['strengths']:
            report += f"   • {strength}\n"

        if not grad['feedback']['strengths']:
            report += "   (none identified)\n"

        report += "\n❌ WEAKNESSES:\n"
        for weakness in grad['feedback']['weaknesses']:
            report += f"   • {weakness}\n"

        if not grad['feedback']['weaknesses']:
            report += "   (none identified)\n"

        report += "\n💡 RECOMMENDATIONS:\n"
        for rec in grad['feedback']['recommendations']:
            report += f"   • {rec}\n"

        if not grad['feedback']['recommendations']:
            report += "   (none needed)\n"

        report += "\n" + "="*80 + "\n"

        return report

    def save_validation_report(self, validation_result: Dict, output_path: Path) -> None:
        """Salva relatório em arquivo."""
        report_text = self.generate_report(validation_result)

        # Salva texto
        txt_path = output_path.with_suffix('.txt')
        txt_path.write_text(report_text, encoding='utf-8')

        # Salva JSON
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(validation_result, f, indent=2, ensure_ascii=False)

        print(f"📄 Report saved: {txt_path}")
        print(f"📊 JSON saved: {json_path}")
