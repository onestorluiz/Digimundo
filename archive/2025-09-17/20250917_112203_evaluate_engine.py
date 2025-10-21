"""
Evaluate Engine - Estágio 3 do Pipeline de Análise
Avalia qualidade do roteiro contra padrões da indústria
Fase 2.B - Implementação real
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import statistics

@dataclass
class QualityMetric:
    """Métrica de qualidade"""
    name: str
    score: float
    weight: float
    category: str
    details: str = ''
    suggestions: List[str] = field(default_factory=list)

@dataclass
class IndustryStandard:
    """Padrão da indústria para comparação"""
    name: str
    min_value: float
    max_value: float
    optimal_value: float
    unit: str

class ScriptCategory(Enum):
    """Categorias de roteiro"""
    FEATURE_FILM = 'feature_film'
    SHORT_FILM = 'short_film'
    TV_PILOT = 'tv_pilot'
    TV_EPISODE = 'tv_episode'
    WEB_SERIES = 'web_series'
    DOCUMENTARY = 'documentary'

class EvaluateEngine:
    """
    Motor de avaliação - Estágio 3 do pipeline
    Avalia qualidade contra padrões e melhores práticas
    """
    INDUSTRY_STANDARDS = {ScriptCategory.FEATURE_FILM: {'page_count': IndustryStandard('Page Count', 90, 120, 110, 'pages'), 'scene_count': IndustryStandard('Scene Count', 40, 150, 80, 'scenes'), 'avg_scene_length': IndustryStandard('Avg Scene Length', 0.5, 3.0, 1.5, 'pages'), 'dialogue_ratio': IndustryStandard('Dialogue Ratio', 0.25, 0.45, 0.35, 'ratio'), 'character_count': IndustryStandard('Character Count', 10, 30, 20, 'characters'), 'protagonist_presence': IndustryStandard('Protagonist Presence', 0.6, 0.8, 0.7, 'ratio')}, ScriptCategory.SHORT_FILM: {'page_count': IndustryStandard('Page Count', 5, 40, 15, 'pages'), 'scene_count': IndustryStandard('Scene Count', 5, 30, 15, 'scenes'), 'avg_scene_length': IndustryStandard('Avg Scene Length', 0.5, 2.0, 1.0, 'pages'), 'dialogue_ratio': IndustryStandard('Dialogue Ratio', 0.2, 0.5, 0.3, 'ratio'), 'character_count': IndustryStandard('Character Count', 2, 10, 5, 'characters'), 'protagonist_presence': IndustryStandard('Protagonist Presence', 0.7, 0.9, 0.8, 'ratio')}, ScriptCategory.TV_PILOT: {'page_count': IndustryStandard('Page Count', 50, 65, 60, 'pages'), 'scene_count': IndustryStandard('Scene Count', 30, 60, 45, 'scenes'), 'avg_scene_length': IndustryStandard('Avg Scene Length', 0.8, 2.0, 1.3, 'pages'), 'dialogue_ratio': IndustryStandard('Dialogue Ratio', 0.35, 0.55, 0.45, 'ratio'), 'character_count': IndustryStandard('Character Count', 8, 20, 15, 'characters'), 'protagonist_presence': IndustryStandard('Protagonist Presence', 0.5, 0.7, 0.6, 'ratio')}}
    CATEGORY_WEIGHTS = {'structure': 0.25, 'characters': 0.25, 'dialogue': 0.2, 'pacing': 0.15, 'formatting': 0.1, 'originality': 0.05}

    def __init__(self):
        """Inicializa engine de avaliação"""
        self.metrics: List[QualityMetric] = []
        self.category = ScriptCategory.FEATURE_FILM
        self.overall_score = 0.0

    def evaluate(self, extraction_data: Dict[str, Any], analysis_data: Dict[str, Any], category: ScriptCategory=ScriptCategory.FEATURE_FILM) -> Dict[str, Any]:
        """
        Avalia roteiro baseado em extração e análise
        Retorna scores, métricas e recomendações
        """
        self.category = category
        self.metrics.clear()
        self._evaluate_structure(extraction_data, analysis_data)
        self._evaluate_characters(extraction_data, analysis_data)
        self._evaluate_dialogue(extraction_data, analysis_data)
        self._evaluate_pacing(extraction_data, analysis_data)
        self._evaluate_formatting(extraction_data)
        self._evaluate_originality(analysis_data)
        self.overall_score = self._calculate_overall_score()
        grade = self._calculate_grade()
        strengths, weaknesses = self._identify_strengths_weaknesses()
        recommendations = self._generate_recommendations()
        return {'overall_score': round(self.overall_score, 1), 'grade': grade, 'metrics': self._serialize_metrics(), 'category_scores': self._get_category_scores(), 'strengths': strengths, 'weaknesses': weaknesses, 'recommendations': recommendations, 'industry_comparison': self._compare_to_industry_standards(extraction_data, analysis_data), 'script_category': category.value}

    def _evaluate_structure(self, extraction: Dict, analysis: Dict) -> None:
        """Avalia estrutura do roteiro"""
        three_act_score = 0.0
        if 'three_act_structure' in analysis:
            acts = analysis['three_act_structure']
            total_pages = extraction.get('statistics', {}).get('total_pages', 1)
            if total_pages == 0:
                total_pages = 1
            act1_ratio = acts.get('act1', {}).get('pages', 0) / total_pages
            act2_ratio = acts.get('act2', {}).get('pages', 0) / total_pages
            act3_ratio = acts.get('act3', {}).get('pages', 0) / total_pages
            act1_deviation = abs(act1_ratio - 0.25)
            act2_deviation = abs(act2_ratio - 0.5)
            act3_deviation = abs(act3_ratio - 0.25)
            structure_score = max(0, 100 - (act1_deviation + act2_deviation + act3_deviation) * 200)
            suggestions = []
            if act1_deviation > 0.05:
                suggestions.append(f'Ajustar duração do Ato 1 (atual: {act1_ratio:.0%}, ideal: 25%)')
            if act2_deviation > 0.05:
                suggestions.append(f'Balancear Ato 2 (atual: {act2_ratio:.0%}, ideal: 50%)')
            if act3_deviation > 0.05:
                suggestions.append(f'Revisar duração do Ato 3 (atual: {act3_ratio:.0%}, ideal: 25%)')
            self.metrics.append(QualityMetric(name='Estrutura de Três Atos', score=structure_score, weight=0.4, category='structure', details=f'Ato 1: {act1_ratio:.0%}, Ato 2: {act2_ratio:.0%}, Ato 3: {act3_ratio:.0%}', suggestions=suggestions))
        if 'plot_points' in analysis:
            plot_points = analysis['plot_points']
            pp_score = 100.0
            suggestions = []
            if not plot_points.get('inciting_incident'):
                pp_score -= 25
                suggestions.append('Adicionar incidente incitante claro')
            if not plot_points.get('midpoint'):
                pp_score -= 25
                suggestions.append('Desenvolver ponto médio forte')
            if not plot_points.get('climax'):
                pp_score -= 25
                suggestions.append('Fortalecer clímax da história')
            self.metrics.append(QualityMetric(name='Pontos de Virada', score=pp_score, weight=0.3, category='structure', details=f'{len([p for p in plot_points.values() if p])} pontos identificados', suggestions=suggestions))
        setup_payoff_score = 70.0
        if 'themes' in analysis and len(analysis['themes']) > 0:
            setup_payoff_score += min(30, len(analysis['themes']) * 10)
        self.metrics.append(QualityMetric(name='Setup & Payoff', score=setup_payoff_score, weight=0.3, category='structure', details='Avaliação de plantas e recompensas narrativas'))

    def _evaluate_characters(self, extraction: Dict, analysis: Dict) -> None:
        """Avalia personagens"""
        characters = extraction.get('characters', [])
        if characters and 'character_arcs' in analysis:
            protagonist = characters[0]
            arc_data = next((arc for arc in analysis['character_arcs'] if arc['character'] == protagonist['name']), None)
            if arc_data:
                transformation_score = arc_data.get('transformation_score', 50)
                suggestions = []
                if transformation_score < 60:
                    suggestions.append(f"Desenvolver arco de {protagonist['name']} mais claramente")
                self.metrics.append(QualityMetric(name='Arco do Protagonista', score=transformation_score, weight=0.4, category='characters', details=f"Transformação de {protagonist['name']}: {transformation_score:.0f}%", suggestions=suggestions))
        char_count = len(characters)
        standards = self.INDUSTRY_STANDARDS[self.category]
        if 'character_count' in standards:
            std = standards['character_count']
            if std.min_value <= char_count <= std.max_value:
                diversity_score = 100
            else:
                deviation = min(abs(char_count - std.min_value), abs(char_count - std.max_value))
                diversity_score = max(0, 100 - deviation * 5)
            suggestions = []
            if char_count < std.min_value:
                suggestions.append(f'Adicionar personagens (atual: {char_count}, mínimo: {std.min_value})')
            elif char_count > std.max_value:
                suggestions.append(f'Reduzir personagens (atual: {char_count}, máximo: {std.max_value})')
            self.metrics.append(QualityMetric(name='Elenco de Personagens', score=diversity_score, weight=0.3, category='characters', details=f'{char_count} personagens', suggestions=suggestions))
        distinction_score = 70.0
        if characters:
            dialogue_counts = [c['dialogue_count'] for c in characters[:5]]
            if len(dialogue_counts) > 1:
                variance = statistics.stdev(dialogue_counts)
                distinction_score = min(100, 70 + variance * 2)
        self.metrics.append(QualityMetric(name='Distinção de Personagens', score=distinction_score, weight=0.3, category='characters', details='Personalidades únicas e vozes distintas'))

    def _evaluate_dialogue(self, extraction: Dict, analysis: Dict) -> None:
        """Avalia diálogos"""
        stats = extraction.get('statistics', {})
        dialogues = extraction.get('dialogues', [])
        total_lines = stats.get('dialogue_lines', 0) + stats.get('action_mentions', 0)
        if total_lines > 0:
            dialogue_ratio = stats.get('dialogue_lines', 0) / total_lines
            standards = self.INDUSTRY_STANDARDS[self.category]
            if 'dialogue_ratio' in standards:
                std = standards['dialogue_ratio']
                if std.min_value <= dialogue_ratio <= std.max_value:
                    ratio_score = 100
                else:
                    deviation = min(abs(dialogue_ratio - std.min_value), abs(dialogue_ratio - std.max_value))
                    ratio_score = max(0, 100 - deviation * 200)
                suggestions = []
                if dialogue_ratio < std.min_value:
                    suggestions.append(f'Adicionar mais diálogo (atual: {dialogue_ratio:.0%})')
                elif dialogue_ratio > std.max_value:
                    suggestions.append(f'Reduzir diálogo, adicionar ação visual (atual: {dialogue_ratio:.0%})')
                self.metrics.append(QualityMetric(name='Balanço Diálogo/Ação', score=ratio_score, weight=0.4, category='dialogue', details=f'Proporção: {dialogue_ratio:.0%}', suggestions=suggestions))
        quality_score = 75.0
        if dialogues:
            lengths = [len(d['text'].split()) for d in dialogues]
            if lengths:
                avg_length = sum(lengths) / len(lengths)
                if 5 <= avg_length <= 20:
                    quality_score = 85.0
                else:
                    quality_score = 65.0
        self.metrics.append(QualityMetric(name='Qualidade do Diálogo', score=quality_score, weight=0.3, category='dialogue', details='Naturalidade e efetividade'))
        subtext_score = 70.0
        if 'emotional_beats' in analysis:
            beat_count = len(analysis['emotional_beats'])
            subtext_score = min(100, 70 + beat_count * 2)
        self.metrics.append(QualityMetric(name='Subtexto e Conflito', score=subtext_score, weight=0.3, category='dialogue', details='Camadas de significado nos diálogos'))

    def _evaluate_pacing(self, extraction: Dict, analysis: Dict) -> None:
        """Avalia ritmo"""
        scenes = extraction.get('scenes', [])
        if scenes and 'pacing_analysis' in analysis:
            pacing = analysis['pacing_analysis']
            rhythm_score = pacing.get('rhythm_score', 70)
            suggestions = []
            if rhythm_score < 60:
                suggestions.append('Variar mais o ritmo entre cenas')
            self.metrics.append(QualityMetric(name='Ritmo Narrativo', score=rhythm_score, weight=0.4, category='pacing', details=f'Variação e fluxo: {rhythm_score:.0f}%', suggestions=suggestions))
            scene_lengths = [s['duration'] for s in scenes]
            if scene_lengths:
                avg_length = sum(scene_lengths) / len(scene_lengths)
                standards = self.INDUSTRY_STANDARDS[self.category]
                if 'avg_scene_length' in standards:
                    std = standards['avg_scene_length']
                    if std.min_value <= avg_length <= std.max_value:
                        length_score = 100
                    else:
                        deviation = min(abs(avg_length - std.min_value), abs(avg_length - std.max_value))
                        length_score = max(0, 100 - deviation * 30)
                    suggestions = []
                    if avg_length < std.min_value:
                        suggestions.append(f'Desenvolver cenas mais (média: {avg_length:.1f} páginas)')
                    elif avg_length > std.max_value:
                        suggestions.append(f'Dividir cenas longas (média: {avg_length:.1f} páginas)')
                    self.metrics.append(QualityMetric(name='Duração das Cenas', score=length_score, weight=0.3, category='pacing', details=f'Média: {avg_length:.1f} páginas', suggestions=suggestions))
            momentum_score = 75.0
            if 'momentum_points' in pacing:
                momentum_count = len(pacing['momentum_points'])
                momentum_score = min(100, 60 + momentum_count * 5)
            self.metrics.append(QualityMetric(name='Momentum', score=momentum_score, weight=0.3, category='pacing', details='Progressão e energia narrativa'))

    def _evaluate_formatting(self, extraction: Dict) -> None:
        """Avalia formatação"""
        stats = extraction.get('statistics', {})
        page_count = stats.get('total_pages', 0)
        standards = self.INDUSTRY_STANDARDS[self.category]
        if 'page_count' in standards:
            std = standards['page_count']
            if std.min_value <= page_count <= std.max_value:
                page_score = 100
            else:
                deviation = min(abs(page_count - std.min_value), abs(page_count - std.max_value))
                page_score = max(0, 100 - deviation)
            suggestions = []
            if page_count < std.min_value:
                suggestions.append(f'Expandir roteiro (atual: {page_count}, mínimo: {std.min_value})')
            elif page_count > std.max_value:
                suggestions.append(f'Cortar conteúdo (atual: {page_count}, máximo: {std.max_value})')
            self.metrics.append(QualityMetric(name='Comprimento', score=page_score, weight=0.5, category='formatting', details=f'{page_count} páginas', suggestions=suggestions))
        format_score = 85.0
        self.metrics.append(QualityMetric(name='Formatação Técnica', score=format_score, weight=0.5, category='formatting', details='Conformidade com padrões da indústria'))

    def _evaluate_originality(self, analysis: Dict) -> None:
        """Avalia originalidade"""
        originality_score = 70.0
        if 'themes' in analysis:
            theme_count = len(analysis['themes'])
            originality_score = min(100, 70 + theme_count * 5)
        self.metrics.append(QualityMetric(name='Originalidade', score=originality_score, weight=1.0, category='originality', details='Conceito e execução únicos'))

    def _calculate_overall_score(self) -> float:
        """Calcula score geral ponderado"""
        category_scores = {}
        for metric in self.metrics:
            if metric.category not in category_scores:
                category_scores[metric.category] = []
            category_scores[metric.category].append((metric.score, metric.weight))
        final_scores = {}
        for category, scores in category_scores.items():
            total_weight = sum((w for _, w in scores))
            if total_weight > 0:
                weighted_sum = sum((s * w for s, w in scores))
                final_scores[category] = weighted_sum / total_weight
        overall = 0.0
        for category, weight in self.CATEGORY_WEIGHTS.items():
            if category in final_scores:
                overall += final_scores[category] * weight
        return overall

    def _calculate_grade(self) -> str:
        """Calcula nota baseada no score"""
        if self.overall_score >= 90:
            return 'A+'
        elif self.overall_score >= 85:
            return 'A'
        elif self.overall_score >= 80:
            return 'A-'
        elif self.overall_score >= 75:
            return 'B+'
        elif self.overall_score >= 70:
            return 'B'
        elif self.overall_score >= 65:
            return 'B-'
        elif self.overall_score >= 60:
            return 'C+'
        elif self.overall_score >= 55:
            return 'C'
        elif self.overall_score >= 50:
            return 'C-'
        elif self.overall_score >= 45:
            return 'D'
        else:
            return 'F'

    def _identify_strengths_weaknesses(self) -> Tuple[List[str], List[str]]:
        """Identifica pontos fortes e fracos"""
        strengths = []
        weaknesses = []
        for metric in self.metrics:
            if metric.score >= 80:
                strengths.append(f'{metric.name}: {metric.score:.0f}%')
            elif metric.score < 60:
                weaknesses.append(f'{metric.name}: {metric.score:.0f}%')
        return (strengths[:5], weaknesses[:5])

    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações prioritárias"""
        all_suggestions = []
        for metric in self.metrics:
            for suggestion in metric.suggestions:
                priority = (100 - metric.score) * metric.weight
                all_suggestions.append((priority, suggestion))
        all_suggestions.sort(reverse=True)
        return [sug for _, sug in all_suggestions[:10]]

    def _compare_to_industry_standards(self, extraction: Dict, analysis: Dict) -> Dict[str, Any]:
        """Compara com padrões da indústria"""
        comparisons = {}
        stats = extraction.get('statistics', {})
        standards = self.INDUSTRY_STANDARDS[self.category]
        if 'page_count' in standards:
            actual = stats.get('total_pages', 0)
            std = standards['page_count']
            comparisons['page_count'] = {'actual': actual, 'min': std.min_value, 'max': std.max_value, 'optimal': std.optimal_value, 'status': 'OK' if std.min_value <= actual <= std.max_value else 'FORA'}
        if 'scene_count' in standards:
            actual = stats.get('total_scenes', 0)
            std = standards['scene_count']
            comparisons['scene_count'] = {'actual': actual, 'min': std.min_value, 'max': std.max_value, 'optimal': std.optimal_value, 'status': 'OK' if std.min_value <= actual <= std.max_value else 'FORA'}
        return comparisons

    def _get_category_scores(self) -> Dict[str, float]:
        """Retorna scores por categoria"""
        category_scores = {}
        for category in self.CATEGORY_WEIGHTS.keys():
            metrics = [m for m in self.metrics if m.category == category]
            if metrics:
                total_weight = sum((m.weight for m in metrics))
                if total_weight > 0:
                    weighted_sum = sum((m.score * m.weight for m in metrics))
                    category_scores[category] = round(weighted_sum / total_weight, 1)
        return category_scores

    def _serialize_metrics(self) -> List[Dict[str, Any]]:
        """Serializa métricas para output"""
        return [{'name': metric.name, 'score': round(metric.score, 1), 'category': metric.category, 'details': metric.details, 'suggestions': metric.suggestions[:3]} for metric in sorted(self.metrics, key=lambda m: m.score)]
_engine_instance: Optional[EvaluateEngine] = None

def get_evaluate_engine() -> EvaluateEngine:
    """Retorna instância singleton"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = EvaluateEngine()
    return _engine_instance
__all__ = ['EvaluateEngine', 'QualityMetric', 'ScriptCategory', 'get_evaluate_engine']