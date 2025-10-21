"""
AI Comparison - Comparação Automática entre Roteiros
Fase 3.C - Sistema de comparação inteligente e análise diferencial
"""
import json
import math
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import hashlib
import logging
logger = logging.getLogger(__name__)

@dataclass
class ComparisonMetric:
    """Métrica de comparação entre dois roteiros"""
    name: str
    script_a_value: Any
    script_b_value: Any
    similarity_score: float
    difference: str
    significance: str
    description: str

@dataclass
class ComparisonDimension:
    """Dimensão de comparação (ex: structure, characters, etc.)"""
    dimension: str
    overall_similarity: float
    metrics: List[ComparisonMetric]
    summary: str
    winner: Optional[str]
    winner_reason: str

@dataclass
class ScriptComparison:
    """Resultado completo da comparação"""
    script_a_name: str
    script_b_name: str
    overall_similarity: float
    dimensions: List[ComparisonDimension]
    strengths_a: List[str]
    strengths_b: List[str]
    key_differences: List[str]
    recommendations: List[str]
    similarity_breakdown: Dict[str, float]

class ComparisonEngine:
    """Engine principal para comparação de roteiros"""

    def __init__(self):
        """Inicializa engine"""
        self.comparison_weights = {'structure': 0.25, 'characters': 0.2, 'dialogue': 0.15, 'pacing': 0.15, 'sentiment': 0.1, 'style': 0.1, 'themes': 0.05}

    def compare_scripts(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any], script_a_name: str='Script A', script_b_name: str='Script B') -> ScriptComparison:
        """
        Compara dois roteiros baseado em suas análises
        
        Args:
            analysis_a: Análise completa do primeiro roteiro
            analysis_b: Análise completa do segundo roteiro
            script_a_name: Nome do primeiro roteiro
            script_b_name: Nome do segundo roteiro
            
        Returns:
            Comparação detalhada entre os roteiros
        """
        dimensions = []
        similarity_breakdown = {}
        dimensions.append(self._compare_structure(analysis_a, analysis_b))
        dimensions.append(self._compare_characters(analysis_a, analysis_b))
        dimensions.append(self._compare_dialogue(analysis_a, analysis_b))
        dimensions.append(self._compare_pacing(analysis_a, analysis_b))
        dimensions.append(self._compare_sentiment(analysis_a, analysis_b))
        dimensions.append(self._compare_style(analysis_a, analysis_b))
        dimensions.append(self._compare_themes(analysis_a, analysis_b))
        overall_similarity = 0.0
        for dim in dimensions:
            weight = self.comparison_weights.get(dim.dimension, 0.1)
            overall_similarity += dim.overall_similarity * weight
            similarity_breakdown[dim.dimension] = dim.overall_similarity
        strengths_a, strengths_b = self._identify_strengths(dimensions, script_a_name, script_b_name)
        key_differences = self._identify_key_differences(dimensions)
        recommendations = self._generate_comparison_recommendations(dimensions, analysis_a, analysis_b)
        return ScriptComparison(script_a_name=script_a_name, script_b_name=script_b_name, overall_similarity=round(overall_similarity, 3), dimensions=dimensions, strengths_a=strengths_a, strengths_b=strengths_b, key_differences=key_differences, recommendations=recommendations, similarity_breakdown=similarity_breakdown)

    def _compare_structure(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara estrutura dos roteiros"""
        metrics = []
        score_a = analysis_a.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('structure', 0)
        score_b = analysis_b.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('structure', 0)
        structure_similarity = 1.0 - abs(score_a - score_b) / 100.0
        metrics.append(ComparisonMetric(name='Structure Score', script_a_value=score_a, script_b_value=score_b, similarity_score=structure_similarity, difference='higher' if score_a > score_b else 'lower' if score_a < score_b else 'similar', significance='major' if abs(score_a - score_b) > 20 else 'moderate' if abs(score_a - score_b) > 10 else 'minor', description=f'Scores de estrutura: {score_a} vs {score_b}'))
        pages_a = analysis_a.get('detailed_report', {}).get('metadata', {}).get('script_info', {}).get('total_pages', 0)
        pages_b = analysis_b.get('detailed_report', {}).get('metadata', {}).get('script_info', {}).get('total_pages', 0)
        if pages_a > 0 and pages_b > 0:
            page_similarity = 1.0 - min(abs(pages_a - pages_b) / max(pages_a, pages_b), 1.0)
            metrics.append(ComparisonMetric(name='Length', script_a_value=f'{pages_a} páginas', script_b_value=f'{pages_b} páginas', similarity_score=page_similarity, difference='longer' if pages_a > pages_b else 'shorter' if pages_a < pages_b else 'similar', significance='major' if abs(pages_a - pages_b) > 30 else 'moderate' if abs(pages_a - pages_b) > 15 else 'minor', description=f'Diferença de {abs(pages_a - pages_b)} páginas'))
        struct_a = analysis_a.get('detailed_report', {}).get('detailed_analysis', {}).get('structure_analysis', {})
        struct_b = analysis_b.get('detailed_report', {}).get('detailed_analysis', {}).get('structure_analysis', {})
        if struct_a and struct_b:
            three_act_a = struct_a.get('three_act_structure', {})
            three_act_b = struct_b.get('three_act_structure', {})
            if three_act_a and three_act_b:
                act_similarities = []
                for act in ['act1', 'act2', 'act3']:
                    pct_a = three_act_a.get(act, {}).get('percentage', 0)
                    pct_b = three_act_b.get(act, {}).get('percentage', 0)
                    if pct_a > 0 and pct_b > 0:
                        act_sim = 1.0 - abs(pct_a - pct_b) / 100.0
                        act_similarities.append(act_sim)
                if act_similarities:
                    three_act_similarity = sum(act_similarities) / len(act_similarities)
                    metrics.append(ComparisonMetric(name='Three Act Structure', script_a_value='Presente', script_b_value='Presente', similarity_score=three_act_similarity, difference='similar', significance='moderate', description=f'Estruturas de três atos {three_act_similarity:.1%} similares'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.0
        winner = None
        winner_reason = ''
        if score_a > score_b + 10:
            winner = 'script_a'
            winner_reason = f'Estrutura mais sólida (score {score_a} vs {score_b})'
        elif score_b > score_a + 10:
            winner = 'script_b'
            winner_reason = f'Estrutura mais sólida (score {score_b} vs {score_a})'
        else:
            winner = 'tie'
            winner_reason = 'Estruturas equivalentes'
        return ComparisonDimension(dimension='structure', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade estrutural: {overall_similarity:.1%}', winner=winner, winner_reason=winner_reason)

    def _compare_characters(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara desenvolvimento de personagens"""
        metrics = []
        score_a = analysis_a.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('characters', 0)
        score_b = analysis_b.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('characters', 0)
        char_similarity = 1.0 - abs(score_a - score_b) / 100.0
        metrics.append(ComparisonMetric(name='Character Development Score', script_a_value=score_a, script_b_value=score_b, similarity_score=char_similarity, difference='higher' if score_a > score_b else 'lower' if score_a < score_b else 'similar', significance='major' if abs(score_a - score_b) > 15 else 'moderate' if abs(score_a - score_b) > 8 else 'minor', description=f'Desenvolvimento de personagens: {score_a} vs {score_b}'))
        char_data_a = analysis_a.get('detailed_report', {}).get('detailed_analysis', {}).get('character_analysis', {})
        char_data_b = analysis_b.get('detailed_report', {}).get('detailed_analysis', {}).get('character_analysis', {})
        if char_data_a and char_data_b:
            chars_a = len(char_data_a.get('characters', {}))
            chars_b = len(char_data_b.get('characters', {}))
            if chars_a > 0 and chars_b > 0:
                char_count_similarity = 1.0 - min(abs(chars_a - chars_b) / max(chars_a, chars_b), 1.0)
                metrics.append(ComparisonMetric(name='Character Count', script_a_value=f'{chars_a} personagens', script_b_value=f'{chars_b} personagens', similarity_score=char_count_similarity, difference='more' if chars_a > chars_b else 'fewer' if chars_a < chars_b else 'similar', significance='moderate' if abs(chars_a - chars_b) > 3 else 'minor', description=f'Diferença de {abs(chars_a - chars_b)} personagens principais'))
        if 'sentiment_analysis' in analysis_a and 'sentiment_analysis' in analysis_b:
            sent_a = analysis_a['sentiment_analysis'].get('character_analysis', {})
            sent_b = analysis_b['sentiment_analysis'].get('character_analysis', {})
            if sent_a and sent_b:
                diversity_a = self._calculate_emotional_diversity(sent_a)
                diversity_b = self._calculate_emotional_diversity(sent_b)
                emotion_similarity = 1.0 - abs(diversity_a - diversity_b)
                metrics.append(ComparisonMetric(name='Emotional Diversity', script_a_value=f'{diversity_a:.2f}', script_b_value=f'{diversity_b:.2f}', similarity_score=emotion_similarity, difference='higher' if diversity_a > diversity_b else 'lower' if diversity_a < diversity_b else 'similar', significance='moderate', description=f'Diversidade emocional dos personagens'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.0
        winner = None
        winner_reason = ''
        if score_a > score_b + 12:
            winner = 'script_a'
            winner_reason = f'Personagens mais bem desenvolvidos (score {score_a})'
        elif score_b > score_a + 12:
            winner = 'script_b'
            winner_reason = f'Personagens mais bem desenvolvidos (score {score_b})'
        else:
            winner = 'tie'
            winner_reason = 'Desenvolvimento de personagens equivalente'
        return ComparisonDimension(dimension='characters', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade de personagens: {overall_similarity:.1%}', winner=winner, winner_reason=winner_reason)

    def _compare_dialogue(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara qualidade dos diálogos"""
        metrics = []
        score_a = analysis_a.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('dialogue', 0)
        score_b = analysis_b.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('dialogue', 0)
        dialogue_similarity = 1.0 - abs(score_a - score_b) / 100.0
        metrics.append(ComparisonMetric(name='Dialogue Quality Score', script_a_value=score_a, script_b_value=score_b, similarity_score=dialogue_similarity, difference='higher' if score_a > score_b else 'lower' if score_a < score_b else 'similar', significance='major' if abs(score_a - score_b) > 15 else 'moderate' if abs(score_a - score_b) > 8 else 'minor', description=f'Qualidade do diálogo: {score_a} vs {score_b}'))
        if 'sentiment_analysis' in analysis_a and 'sentiment_analysis' in analysis_b:
            dialogue_count_a = analysis_a['sentiment_analysis'].get('dialogue_count', 0)
            dialogue_count_b = analysis_b['sentiment_analysis'].get('dialogue_count', 0)
            if dialogue_count_a > 0 and dialogue_count_b > 0:
                dialogue_qty_similarity = 1.0 - min(abs(dialogue_count_a - dialogue_count_b) / max(dialogue_count_a, dialogue_count_b), 1.0)
                metrics.append(ComparisonMetric(name='Dialogue Quantity', script_a_value=f'{dialogue_count_a} diálogos', script_b_value=f'{dialogue_count_b} diálogos', similarity_score=dialogue_qty_similarity, difference='more' if dialogue_count_a > dialogue_count_b else 'fewer' if dialogue_count_a < dialogue_count_b else 'similar', significance='moderate' if abs(dialogue_count_a - dialogue_count_b) > 50 else 'minor', description=f'Diferença de {abs(dialogue_count_a - dialogue_count_b)} diálogos'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.0
        winner = None
        winner_reason = ''
        if score_a > score_b + 10:
            winner = 'script_a'
            winner_reason = f'Diálogos mais efetivos (score {score_a})'
        elif score_b > score_a + 10:
            winner = 'script_b'
            winner_reason = f'Diálogos mais efetivos (score {score_b})'
        else:
            winner = 'tie'
            winner_reason = 'Qualidade de diálogo equivalente'
        return ComparisonDimension(dimension='dialogue', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade de diálogos: {overall_similarity:.1%}', winner=winner, winner_reason=winner_reason)

    def _compare_pacing(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara ritmo dos roteiros"""
        metrics = []
        score_a = analysis_a.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('pacing', 0)
        score_b = analysis_b.get('detailed_report', {}).get('score_card', {}).get('category_scores', {}).get('pacing', 0)
        pacing_similarity = 1.0 - abs(score_a - score_b) / 100.0
        metrics.append(ComparisonMetric(name='Pacing Score', script_a_value=score_a, script_b_value=score_b, similarity_score=pacing_similarity, difference='higher' if score_a > score_b else 'lower' if score_a < score_b else 'similar', significance='major' if abs(score_a - score_b) > 15 else 'moderate' if abs(score_a - score_b) > 8 else 'minor', description=f'Scores de ritmo: {score_a} vs {score_b}'))
        overall_similarity = pacing_similarity
        winner = None
        winner_reason = ''
        if score_a > score_b + 10:
            winner = 'script_a'
            winner_reason = f'Ritmo mais bem estruturado (score {score_a})'
        elif score_b > score_a + 10:
            winner = 'script_b'
            winner_reason = f'Ritmo mais bem estruturado (score {score_b})'
        else:
            winner = 'tie'
            winner_reason = 'Ritmo equivalente'
        return ComparisonDimension(dimension='pacing', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade de ritmo: {overall_similarity:.1%}', winner=winner, winner_reason=winner_reason)

    def _compare_sentiment(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara análise de sentimentos"""
        metrics = []
        if 'sentiment_analysis' not in analysis_a or 'sentiment_analysis' not in analysis_b:
            return ComparisonDimension(dimension='sentiment', overall_similarity=0.5, metrics=[], summary='Análise de sentimento não disponível', winner='tie', winner_reason='Dados insuficientes')
        sent_a = analysis_a['sentiment_analysis']['overall_analysis']
        sent_b = analysis_b['sentiment_analysis']['overall_analysis']
        sentiment_a = sent_a.get('sentiment', 0)
        sentiment_b = sent_b.get('sentiment', 0)
        sentiment_similarity = 1.0 - min(abs(sentiment_a - sentiment_b) / 2.0, 1.0)
        metrics.append(ComparisonMetric(name='Overall Sentiment', script_a_value=f'{sentiment_a:.2f}', script_b_value=f'{sentiment_b:.2f}', similarity_score=sentiment_similarity, difference='more positive' if sentiment_a > sentiment_b else 'more negative' if sentiment_a < sentiment_b else 'similar', significance='major' if abs(sentiment_a - sentiment_b) > 0.5 else 'moderate' if abs(sentiment_a - sentiment_b) > 0.2 else 'minor', description=f"Tons emocionais: {sent_a.get('tone', 'N/A')} vs {sent_b.get('tone', 'N/A')}"))
        intensity_a = sent_a.get('intensity', 0)
        intensity_b = sent_b.get('intensity', 0)
        intensity_similarity = 1.0 - abs(intensity_a - intensity_b)
        metrics.append(ComparisonMetric(name='Emotional Intensity', script_a_value=f'{intensity_a:.2f}', script_b_value=f'{intensity_b:.2f}', similarity_score=intensity_similarity, difference='higher' if intensity_a > intensity_b else 'lower' if intensity_a < intensity_b else 'similar', significance='moderate' if abs(intensity_a - intensity_b) > 0.3 else 'minor', description=f'Intensidade emocional'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.0
        winner = None
        winner_reason = ''
        tone_a = sent_a.get('tone', 'neutral')
        tone_b = sent_b.get('tone', 'neutral')
        if intensity_a > intensity_b + 0.2:
            winner = 'script_a'
            winner_reason = f'Mais envolvente emocionalmente (intensidade {intensity_a:.2f})'
        elif intensity_b > intensity_a + 0.2:
            winner = 'script_b'
            winner_reason = f'Mais envolvente emocionalmente (intensidade {intensity_b:.2f})'
        elif tone_a != 'neutral' and tone_b == 'neutral':
            winner = 'script_a'
            winner_reason = f'Tom emocional mais definido ({tone_a})'
        elif tone_b != 'neutral' and tone_a == 'neutral':
            winner = 'script_b'
            winner_reason = f'Tom emocional mais definido ({tone_b})'
        else:
            winner = 'tie'
            winner_reason = 'Perfil emocional similar'
        return ComparisonDimension(dimension='sentiment', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade emocional: {overall_similarity:.1%}', winner=winner, winner_reason=winner_reason)

    def _compare_style(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara estilo de escrita"""
        metrics = []
        pages_a = analysis_a.get('detailed_report', {}).get('metadata', {}).get('script_info', {}).get('total_pages', 0)
        pages_b = analysis_b.get('detailed_report', {}).get('metadata', {}).get('script_info', {}).get('total_pages', 0)
        if pages_a > 0 and pages_b > 0:
            style_similarity = 1.0 - min(abs(pages_a - pages_b) / max(pages_a, pages_b), 1.0)
            metrics.append(ComparisonMetric(name='Writing Density', script_a_value=f'{pages_a} páginas', script_b_value=f'{pages_b} páginas', similarity_score=style_similarity, difference='denser' if pages_a > pages_b else 'leaner' if pages_a < pages_b else 'similar', significance='moderate' if abs(pages_a - pages_b) > 20 else 'minor', description=f'Densidade de escrita comparada'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.5
        return ComparisonDimension(dimension='style', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade de estilo: {overall_similarity:.1%}', winner='tie', winner_reason='Análise de estilo limitada')

    def _compare_themes(self, analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> ComparisonDimension:
        """Compara temas dos roteiros"""
        metrics = []
        if 'sentiment_analysis' in analysis_a and 'sentiment_analysis' in analysis_b:
            insights_a = set(analysis_a['sentiment_analysis'].get('insights', []))
            insights_b = set(analysis_b['sentiment_analysis'].get('insights', []))
            if insights_a and insights_b:
                common_insights = len(insights_a.intersection(insights_b))
                total_insights = len(insights_a.union(insights_b))
                theme_similarity = common_insights / total_insights if total_insights > 0 else 0.5
                metrics.append(ComparisonMetric(name='Thematic Elements', script_a_value=f'{len(insights_a)} elementos', script_b_value=f'{len(insights_b)} elementos', similarity_score=theme_similarity, difference='similar' if common_insights > 0 else 'different', significance='moderate' if theme_similarity > 0.3 else 'minor', description=f'{common_insights} elementos temáticos em comum'))
        overall_similarity = sum((m.similarity_score for m in metrics)) / len(metrics) if metrics else 0.5
        return ComparisonDimension(dimension='themes', overall_similarity=round(overall_similarity, 3), metrics=metrics, summary=f'Similaridade temática: {overall_similarity:.1%}', winner='tie', winner_reason='Análise temática em desenvolvimento')

    def _calculate_emotional_diversity(self, character_analysis: Dict[str, Any]) -> float:
        """Calcula diversidade emocional média dos personagens"""
        if not character_analysis:
            return 0.0
        diversities = []
        for char_data in character_analysis.values():
            sentiment_range = char_data.get('sentiment_range', {})
            range_size = sentiment_range.get('max', 0) - sentiment_range.get('min', 0)
            diversities.append(range_size)
        return sum(diversities) / len(diversities) if diversities else 0.0

    def _identify_strengths(self, dimensions: List[ComparisonDimension], script_a_name: str, script_b_name: str) -> Tuple[List[str], List[str]]:
        """Identifica pontos fortes de cada roteiro"""
        strengths_a = []
        strengths_b = []
        for dim in dimensions:
            if dim.winner == 'script_a':
                strengths_a.append(f'{dim.dimension.title()}: {dim.winner_reason}')
            elif dim.winner == 'script_b':
                strengths_b.append(f'{dim.dimension.title()}: {dim.winner_reason}')
        return (strengths_a, strengths_b)

    def _identify_key_differences(self, dimensions: List[ComparisonDimension]) -> List[str]:
        """Identifica principais diferenças entre os roteiros"""
        differences = []
        for dim in dimensions:
            for metric in dim.metrics:
                if metric.significance in ['major', 'moderate']:
                    differences.append(f'{metric.name}: {metric.description}')
        return differences[:5]

    def _generate_comparison_recommendations(self, dimensions: List[ComparisonDimension], analysis_a: Dict[str, Any], analysis_b: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas na comparação"""
        recommendations = []
        for dim in dimensions:
            if dim.winner == 'script_a':
                recommendations.append(f'Script B pode melhorar {dim.dimension}: {dim.winner_reason}')
            elif dim.winner == 'script_b':
                recommendations.append(f'Script A pode melhorar {dim.dimension}: {dim.winner_reason}')
        low_similarity_dims = [d for d in dimensions if d.overall_similarity < 0.5]
        if low_similarity_dims:
            recommendations.append(f"Considere analisar diferenças em: {', '.join([d.dimension for d in low_similarity_dims])}")
        high_similarity_dims = [d for d in dimensions if d.overall_similarity > 0.8]
        if len(high_similarity_dims) >= 3:
            recommendations.append('Roteiros muito similares - considere diferenciação para evitar redundância')
        return recommendations[:5]
_comparison_engine: Optional[ComparisonEngine] = None

def get_comparison_engine() -> ComparisonEngine:
    """
    Retorna instância singleton do engine
    
    Returns:
        ComparisonEngine configurado
    """
    global _comparison_engine
    if _comparison_engine is None:
        _comparison_engine = ComparisonEngine()
    return _comparison_engine

def compare_scripts(analysis_a: Dict[str, Any], analysis_b: Dict[str, Any], script_a_name: str='Script A', script_b_name: str='Script B') -> ScriptComparison:
    """Atalho para comparar roteiros"""
    engine = get_comparison_engine()
    return engine.compare_scripts(analysis_a, analysis_b, script_a_name, script_b_name)
__all__ = ['ComparisonMetric', 'ComparisonDimension', 'ScriptComparison', 'ComparisonEngine', 'get_comparison_engine', 'compare_scripts']