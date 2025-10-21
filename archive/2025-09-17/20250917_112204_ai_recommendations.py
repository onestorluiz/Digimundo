"""
AI Recommendations - Sistema de Recomendações Inteligentes
Fase 3.C - Recomendações baseadas em análise de roteiros
"""
import json
import math
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

@dataclass
class RecommendationItem:
    """Item de recomendação"""
    category: str
    priority: str
    title: str
    description: str
    rationale: str
    impact: str
    effort: str
    examples: List[str]
    suggestions: List[str]

@dataclass
class ImprovementPlan:
    """Plano de melhoria estruturado"""
    quick_wins: List[RecommendationItem]
    major_improvements: List[RecommendationItem]
    advanced_techniques: List[RecommendationItem]
    priority_order: List[str]

class RecommendationEngine:
    """Engine principal de recomendações"""

    def __init__(self):
        """Inicializa engine com base de conhecimento"""
        self.knowledge_base = self._load_knowledge_base()
        self.genre_patterns = self._load_genre_patterns()
        self.industry_standards = self._load_industry_standards()

    def _load_knowledge_base(self) -> Dict[str, Any]:
        """Carrega base de conhecimento de recomendações"""
        return {'structure': {'three_act_structure': {'act1_percentage': {'ideal': 25, 'range': [20, 30], 'importance': 'high'}, 'act2_percentage': {'ideal': 50, 'range': [45, 55], 'importance': 'high'}, 'act3_percentage': {'ideal': 25, 'range': [20, 30], 'importance': 'high'}, 'plot_points': {'inciting_incident': {'position': 0.12, 'importance': 'critical'}, 'first_plot_point': {'position': 0.25, 'importance': 'critical'}, 'midpoint': {'position': 0.5, 'importance': 'high'}, 'second_plot_point': {'position': 0.75, 'importance': 'critical'}, 'climax': {'position': 0.9, 'importance': 'critical'}}}, 'pacing': {'scene_length_avg': {'ideal': 2.5, 'range': [1.5, 4.0]}, 'action_description_ratio': {'ideal': 0.3, 'range': [0.2, 0.4]}, 'dialogue_ratio': {'ideal': 0.6, 'range': [0.5, 0.7]}}}, 'characters': {'protagonist': {'screen_time': {'min': 0.7, 'ideal': 0.8}, 'dialogue_share': {'min': 0.3, 'ideal': 0.4}, 'arc_development': {'phases': ['setup', 'confrontation', 'resolution']}}, 'supporting_cast': {'max_main_characters': 5, 'min_scenes_per_character': 3, 'distinct_voices': True}}, 'dialogue': {'subtext': {'importance': 'high', 'indicators': ['implication', 'contradiction']}, 'character_voice': {'consistency': 'critical', 'distinctiveness': 'high'}, 'length': {'avg_words': {'ideal': 15, 'range': [8, 25]}}, 'tags': {'minimal': True, 'overuse_threshold': 0.3}}, 'style': {'show_vs_tell': {'ratio': {'ideal': 0.7, 'min': 0.6}}, 'active_voice': {'percentage': {'ideal': 0.8, 'min': 0.7}}, 'sentence_variety': {'importance': 'medium'}}}

    def _load_genre_patterns(self) -> Dict[str, Any]:
        """Carrega padrões específicos por gênero"""
        return {'thriller': {'pacing': 'fast', 'tension_curve': 'escalating', 'plot_points': 'frequent', 'character_focus': 'plot_driven', 'style': 'lean'}, 'drama': {'pacing': 'measured', 'tension_curve': 'character_driven', 'plot_points': 'emotional', 'character_focus': 'character_driven', 'style': 'detailed'}, 'comedy': {'pacing': 'varied', 'tension_curve': 'relief_pattern', 'plot_points': 'setup_payoff', 'character_focus': 'ensemble', 'style': 'conversational'}, 'action': {'pacing': 'fast', 'tension_curve': 'peaks_valleys', 'plot_points': 'visual', 'character_focus': 'goal_oriented', 'style': 'concise'}, 'romance': {'pacing': 'emotional', 'tension_curve': 'will_they_wont_they', 'plot_points': 'relationship_beats', 'character_focus': 'dual_protagonist', 'style': 'intimate'}}

    def _load_industry_standards(self) -> Dict[str, Any]:
        """Carrega padrões da indústria"""
        return {'page_count': {'feature_film': {'min': 90, 'ideal': [100, 120], 'max': 130}, 'tv_pilot': {'min': 22, 'ideal': [25, 30], 'max': 35}, 'short_film': {'min': 5, 'ideal': [10, 20], 'max': 30}}, 'formatting': {'margins': {'standard': True}, 'font': {'courier': True, 'size': 12}, 'spacing': {'single': True}}, 'market_trends': {'diverse_characters': {'importance': 'increasing'}, 'environmental_themes': {'relevance': 'high'}, 'streaming_format': {'consideration': 'important'}}}

    def generate_recommendations(self, analysis_result: Dict[str, Any]) -> List[RecommendationItem]:
        """
        Gera recomendações baseadas na análise do roteiro
        
        Args:
            analysis_result: Resultado da análise completa do roteiro
            
        Returns:
            Lista de recomendações priorizadas
        """
        recommendations = []
        recommendations.extend(self._analyze_structure(analysis_result))
        recommendations.extend(self._analyze_characters(analysis_result))
        recommendations.extend(self._analyze_dialogue(analysis_result))
        recommendations.extend(self._analyze_pacing(analysis_result))
        recommendations.extend(self._analyze_style(analysis_result))
        recommendations = self._prioritize_recommendations(recommendations, analysis_result)
        return recommendations

    def _analyze_structure(self, analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Analisa estrutura e gera recomendações"""
        recommendations = []
        detailed_analysis = analysis.get('detailed_report', {}).get('detailed_analysis', {})
        structure_analysis = detailed_analysis.get('structure_analysis', {})
        if not structure_analysis:
            return recommendations
        three_act = structure_analysis.get('three_act_structure', {})
        if three_act:
            act1_pct = three_act.get('act1', {}).get('percentage', 0)
            act2_pct = three_act.get('act2', {}).get('percentage', 0)
            act3_pct = three_act.get('act3', {}).get('percentage', 0)
            if act1_pct > 35:
                recommendations.append(RecommendationItem(category='structure', priority='high', title='Primeiro Ato Muito Longo', description=f'O primeiro ato ocupa {act1_pct}% do roteiro, acima do ideal (25%)', rationale='Um primeiro ato muito longo pode perder a atenção da audiência', impact='major', effort='medium', examples=[f'Ato 1: {act1_pct}% vs ideal 25%'], suggestions=['Acelere o setup inicial', 'Introduza o inciting incident mais cedo', 'Corte cenas de exposition desnecessária']))
            elif act1_pct < 20:
                recommendations.append(RecommendationItem(category='structure', priority='medium', title='Primeiro Ato Muito Curto', description=f'O primeiro ato ocupa apenas {act1_pct}% do roteiro', rationale='Setup insuficiente pode deixar audiência perdida', impact='moderate', effort='medium', examples=[f'Ato 1: {act1_pct}% vs ideal 25%'], suggestions=['Desenvolva melhor o setup inicial', 'Apresente personagens com mais profundidade', 'Estabeleça stakes claramente']))
            if act2_pct > 60:
                recommendations.append(RecommendationItem(category='structure', priority='high', title='Segundo Ato Arrastado', description=f'O segundo ato ocupa {act2_pct}% do roteiro, muito acima do ideal (50%)', rationale='Segundo ato longo demais causa perda de ritmo', impact='major', effort='high', examples=[f'Ato 2: {act2_pct}% vs ideal 50%'], suggestions=['Identifique e corte subtramas desnecessárias', 'Acelere o desenvolvimento do conflito', 'Adicione mais plot points para manter interesse']))
        plot_points = structure_analysis.get('plot_points', {})
        if plot_points:
            if not plot_points.get('inciting_incident'):
                recommendations.append(RecommendationItem(category='structure', priority='high', title='Inciting Incident Ausente', description='Não foi identificado um inciting incident claro', rationale='Todo roteiro precisa de um evento que inicie a história', impact='major', effort='medium', examples=['Inciting incident não identificado'], suggestions=['Identifique o evento que muda a vida do protagonista', 'Posicione-o por volta da página 12-15', 'Torne-o específico e claro para a audiência']))
            if not plot_points.get('midpoint'):
                recommendations.append(RecommendationItem(category='structure', priority='medium', title='Midpoint Fraco', description='Midpoint não está bem definido', rationale='Midpoint forte mantém momentum do segundo ato', impact='moderate', effort='medium', examples=['Midpoint ausente ou fraco'], suggestions=['Adicione revelação ou twist na metade da história', 'Mude a estratégia do protagonista', 'Eleve os stakes significativamente']))
        return recommendations

    def _analyze_characters(self, analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Analisa personagens e gera recomendações"""
        recommendations = []
        detailed_analysis = analysis.get('detailed_report', {}).get('detailed_analysis', {})
        char_analysis = detailed_analysis.get('character_analysis', {})
        if not char_analysis:
            return recommendations
        characters = char_analysis.get('characters', {})
        if len(characters) < 2:
            recommendations.append(RecommendationItem(category='character', priority='high', title='Poucos Personagens Identificados', description=f'Apenas {len(characters)} personagens foram identificados', rationale='Roteiros precisam de elenco diversificado para criar conflito', impact='major', effort='medium', examples=[f'Personagens: {list(characters.keys())}'], suggestions=['Desenvolva personagens secundários', 'Adicione antagonista claro', 'Crie personagens de apoio distintos']))
        if characters:
            main_char = max(characters.items(), key=lambda x: x[1].get('dialogue_count', 0))
            char_name, char_data = main_char
            dialogue_share = char_data.get('dialogue_count', 0) / sum((c.get('dialogue_count', 0) for c in characters.values()))
            if dialogue_share < 0.3:
                recommendations.append(RecommendationItem(category='character', priority='medium', title='Protagonista Pouco Presente', description=f'{char_name} tem apenas {dialogue_share:.1%} dos diálogos', rationale='Protagonista deve dominar a narrativa', impact='moderate', effort='medium', examples=[f'{char_name}: {dialogue_share:.1%} dos diálogos'], suggestions=['Dê mais falas ao protagonista', 'Torne-o mais ativo na história', 'Desenvolva sua perspectiva única']))
            elif dialogue_share > 0.7:
                recommendations.append(RecommendationItem(category='character', priority='low', title='Protagonista Muito Dominante', description=f'{char_name} tem {dialogue_share:.1%} dos diálogos', rationale='Outros personagens precisam de desenvolvimento', impact='minor', effort='low', examples=[f'{char_name}: {dialogue_share:.1%} dos diálogos'], suggestions=['Desenvolva vozes dos personagens secundários', 'Distribua mais diálogos significativos', 'Crie cenas sem o protagonista']))
        return recommendations

    def _analyze_dialogue(self, analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Analisa diálogos e gera recomendações"""
        recommendations = []
        if 'sentiment_analysis' in analysis:
            sentiment = analysis['sentiment_analysis']
            char_analysis = sentiment.get('character_analysis', {})
            if char_analysis:
                monotone_chars = []
                for char, data in char_analysis.items():
                    sentiment_range = data.get('sentiment_range', {})
                    range_size = sentiment_range.get('max', 0) - sentiment_range.get('min', 0)
                    if range_size < 0.3:
                        monotone_chars.append(char)
                if monotone_chars:
                    recommendations.append(RecommendationItem(category='dialogue', priority='medium', title='Personagens Emocionalmente Monotônicos', description=f"Personagens com pouca variação emocional: {', '.join(monotone_chars)}", rationale='Personagens precisam de arcos emocionais para serem interessantes', impact='moderate', effort='medium', examples=[f'Personagens monotônicos: {monotone_chars}'], suggestions=['Varie as emoções dos personagens ao longo da história', 'Dê conflitos internos aos personagens', 'Use subtext para criar profundidade emocional']))
            overall = sentiment.get('overall_analysis', {})
            if overall.get('tone') == 'neutral' and overall.get('intensity', 0) < 0.4:
                recommendations.append(RecommendationItem(category='dialogue', priority='medium', title='Diálogos Sem Intensidade Emocional', description='Os diálogos carecem de intensidade emocional', rationale='Diálogos intensos criam engajamento da audiência', impact='moderate', effort='medium', examples=[f"Intensidade geral: {overall.get('intensity', 0):.2f}"], suggestions=['Adicione mais stakes pessoais nas conversas', 'Use conflito para criar tensão', 'Desenvolva subtexto nos diálogos']))
        return recommendations

    def _analyze_pacing(self, analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Analisa ritmo e gera recomendações"""
        recommendations = []
        detailed_analysis = analysis.get('detailed_report', {}).get('detailed_analysis', {})
        pacing_analysis = detailed_analysis.get('pacing_analysis', {})
        if pacing_analysis:
            scene_lengths = pacing_analysis.get('scene_length_analysis', {})
            avg_length = scene_lengths.get('average_length', 0)
            if avg_length > 4:
                recommendations.append(RecommendationItem(category='pacing', priority='medium', title='Cenas Muito Longas', description=f'Comprimento médio das cenas: {avg_length:.1f} páginas', rationale='Cenas longas podem perder a atenção da audiência', impact='moderate', effort='medium', examples=[f'Média de {avg_length:.1f} páginas por cena'], suggestions=['Corte cenas que não avançam a história', 'Entre nas cenas o mais tarde possível', 'Saia das cenas o mais cedo possível']))
            elif avg_length < 1.5:
                recommendations.append(RecommendationItem(category='pacing', priority='low', title='Cenas Muito Curtas', description=f'Comprimento médio das cenas: {avg_length:.1f} páginas', rationale='Cenas muito curtas podem criar ritmo entrecortado', impact='minor', effort='low', examples=[f'Média de {avg_length:.1f} páginas por cena'], suggestions=['Combine cenas relacionadas', 'Desenvolva mais cada momento', 'Permita breathing room para momentos importantes']))
        return recommendations

    def _analyze_style(self, analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Analisa estilo e gera recomendações"""
        recommendations = []
        metadata = analysis.get('detailed_report', {}).get('metadata', {})
        script_info = metadata.get('script_info', {})
        total_pages = script_info.get('total_pages', 0)
        if total_pages > 130:
            recommendations.append(RecommendationItem(category='style', priority='high', title='Roteiro Muito Longo', description=f'Roteiro tem {total_pages} páginas, acima do padrão (90-120)', rationale='Roteiros longos são menos comerciais e mais difíceis de produzir', impact='major', effort='high', examples=[f'{total_pages} páginas vs ideal 90-120'], suggestions=['Corte subtramas desnecessárias', 'Elimine cenas que não avançam a história', 'Torne descrições mais concisas']))
        elif total_pages < 90:
            recommendations.append(RecommendationItem(category='style', priority='medium', title='Roteiro Muito Curto', description=f'Roteiro tem {total_pages} páginas, abaixo do padrão (90-120)', rationale='Roteiros muito curtos podem parecer subdesenvolvidos', impact='moderate', effort='medium', examples=[f'{total_pages} páginas vs ideal 90-120'], suggestions=['Desenvolva mais as cenas existentes', 'Adicione subtramas que enriquecem a história', 'Aprofunde o desenvolvimento de personagens']))
        return recommendations

    def _prioritize_recommendations(self, recommendations: List[RecommendationItem], analysis: Dict[str, Any]) -> List[RecommendationItem]:
        """Prioriza recomendações baseado na análise"""

        def get_priority_score(rec: RecommendationItem) -> int:
            score = 0
            priority_scores = {'high': 100, 'medium': 50, 'low': 10}
            score += priority_scores.get(rec.priority, 0)
            impact_scores = {'major': 50, 'moderate': 25, 'minor': 10}
            score += impact_scores.get(rec.impact, 0)
            effort_scores = {'low': 30, 'medium': 10, 'high': 0}
            score += effort_scores.get(rec.effort, 0)
            category_scores = {'structure': 30, 'character': 20, 'dialogue': 15, 'pacing': 10, 'style': 5}
            score += category_scores.get(rec.category, 0)
            return score
        recommendations.sort(key=get_priority_score, reverse=True)
        return recommendations

    def create_improvement_plan(self, recommendations: List[RecommendationItem]) -> ImprovementPlan:
        """
        Cria plano estruturado de melhorias
        
        Args:
            recommendations: Lista de recomendações
            
        Returns:
            Plano de melhoria organizado
        """
        quick_wins = []
        major_improvements = []
        advanced_techniques = []
        for rec in recommendations:
            if rec.effort == 'low' and rec.impact in ['moderate', 'major']:
                quick_wins.append(rec)
            elif rec.priority == 'high' or rec.impact == 'major':
                major_improvements.append(rec)
            else:
                advanced_techniques.append(rec)
        priority_order = []
        for rec in quick_wins[:3]:
            priority_order.append(f'Quick Win: {rec.title}')
        structure_recs = [r for r in major_improvements if r.category == 'structure']
        for rec in structure_recs[:2]:
            priority_order.append(f'Structure: {rec.title}')
        char_recs = [r for r in major_improvements if r.category == 'character']
        for rec in char_recs[:2]:
            priority_order.append(f'Character: {rec.title}')
        other_recs = [r for r in major_improvements if r.category not in ['structure', 'character']]
        for rec in other_recs[:2]:
            priority_order.append(f'Polish: {rec.title}')
        return ImprovementPlan(quick_wins=quick_wins, major_improvements=major_improvements, advanced_techniques=advanced_techniques, priority_order=priority_order)
_recommendation_engine: Optional[RecommendationEngine] = None

def get_recommendation_engine() -> RecommendationEngine:
    """
    Retorna instância singleton do engine
    
    Returns:
        RecommendationEngine configurado
    """
    global _recommendation_engine
    if _recommendation_engine is None:
        _recommendation_engine = RecommendationEngine()
    return _recommendation_engine

def generate_script_recommendations(analysis_result: Dict[str, Any]) -> List[RecommendationItem]:
    """Atalho para gerar recomendações"""
    engine = get_recommendation_engine()
    return engine.generate_recommendations(analysis_result)

def create_improvement_plan(recommendations: List[RecommendationItem]) -> ImprovementPlan:
    """Atalho para criar plano de melhoria"""
    engine = get_recommendation_engine()
    return engine.create_improvement_plan(recommendations)
__all__ = ['RecommendationItem', 'ImprovementPlan', 'RecommendationEngine', 'get_recommendation_engine', 'generate_script_recommendations', 'create_improvement_plan']