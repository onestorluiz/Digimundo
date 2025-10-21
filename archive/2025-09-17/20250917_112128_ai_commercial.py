"""
AI Commercial Prediction - Predição de Sucesso Comercial
Fase 3.C - Sistema de análise de potencial comercial de roteiros
"""
import json
import math
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import logging
logger = logging.getLogger(__name__)

@dataclass
class MarketFactor:
    """Fator de mercado para predição"""
    name: str
    score: float
    weight: float
    impact: str
    confidence: float
    rationale: str

@dataclass
class CommercialPrediction:
    """Predição completa de sucesso comercial"""
    overall_score: float
    confidence: float
    risk_level: str
    market_category: str
    target_audience: List[str]
    factors: List[MarketFactor]
    strengths: List[str]
    concerns: List[str]
    recommendations: List[str]
    comparable_films: List[str]
    budget_estimate: Dict[str, str]

class CommercialPredictor:
    """Engine de predição de sucesso comercial"""

    def __init__(self):
        """Inicializa predictor com dados de mercado"""
        self.market_weights = self._load_market_weights()
        self.genre_multipliers = self._load_genre_multipliers()
        self.audience_segments = self._load_audience_segments()
        self.success_patterns = self._load_success_patterns()

    def _load_market_weights(self) -> Dict[str, float]:
        """Carrega pesos dos fatores de mercado"""
        return {'structure_quality': 0.2, 'character_appeal': 0.18, 'emotional_engagement': 0.15, 'pacing': 0.12, 'marketable_concept': 0.1, 'genre_appeal': 0.08, 'dialogue_quality': 0.07, 'production_feasibility': 0.05, 'trend_alignment': 0.03, 'originality': 0.02}

    def _load_genre_multipliers(self) -> Dict[str, Dict[str, Any]]:
        """Carrega multiplicadores por gênero"""
        return {'action': {'commercial_multiplier': 1.3, 'international_appeal': 1.4, 'budget_category': 'medium_high', 'target_demo': ['18-34', 'male_skew'], 'risk_level': 'medium'}, 'comedy': {'commercial_multiplier': 1.1, 'international_appeal': 0.9, 'budget_category': 'low_medium', 'target_demo': ['18-44', 'broad'], 'risk_level': 'medium'}, 'drama': {'commercial_multiplier': 0.8, 'international_appeal': 1.0, 'budget_category': 'low_medium', 'target_demo': ['25-54', 'adult_skew'], 'risk_level': 'high'}, 'thriller': {'commercial_multiplier': 1.2, 'international_appeal': 1.2, 'budget_category': 'medium', 'target_demo': ['18-44', 'broad'], 'risk_level': 'low'}, 'horror': {'commercial_multiplier': 1.4, 'international_appeal': 1.3, 'budget_category': 'low', 'target_demo': ['18-34', 'young_skew'], 'risk_level': 'low'}, 'romance': {'commercial_multiplier': 0.9, 'international_appeal': 1.1, 'budget_category': 'low_medium', 'target_demo': ['18-44', 'female_skew'], 'risk_level': 'medium'}, 'sci_fi': {'commercial_multiplier': 1.1, 'international_appeal': 1.3, 'budget_category': 'high', 'target_demo': ['16-44', 'male_skew'], 'risk_level': 'high'}}

    def _load_audience_segments(self) -> Dict[str, Dict[str, Any]]:
        """Carrega dados de segmentos de audiência"""
        return {'mainstream': {'description': 'Público geral, amplo apelo', 'characteristics': ['estrutura clara', 'personagens relacionáveis', 'tema universal'], 'commercial_potential': 0.8, 'required_scores': {'structure': 70, 'characters': 65, 'pacing': 65}}, 'young_adult': {'description': 'Audiência jovem 16-25', 'characteristics': ['protagonistas jovens', 'temas coming-of-age', 'ritmo acelerado'], 'commercial_potential': 0.7, 'required_scores': {'pacing': 75, 'characters': 60}}, 'adult_drama': {'description': 'Audiência madura 35+', 'characteristics': ['temas complexos', 'personagens profundos', 'conflitos psicológicos'], 'commercial_potential': 0.6, 'required_scores': {'dialogue': 75, 'characters': 80}}, 'genre_fans': {'description': 'Fãs de gêneros específicos', 'characteristics': ['elementos de gênero claros', 'tropos reconhecíveis', 'execução competente'], 'commercial_potential': 0.7, 'required_scores': {'structure': 65, 'pacing': 70}}, 'art_house': {'description': 'Audiência de nicho, festivais', 'characteristics': ['originalidade', 'experimentação', 'profundidade temática'], 'commercial_potential': 0.4, 'required_scores': {'originality': 80, 'dialogue': 70}}}

    def _load_success_patterns(self) -> Dict[str, Any]:
        """Carrega padrões de sucesso baseados em dados históricos"""
        return {'high_commercial_success': {'min_overall_score': 75, 'key_factors': ['structure_quality', 'character_appeal', 'pacing'], 'length_range': [90, 120], 'emotional_intensity': [0.6, 0.9], 'sentiment_balance': [-0.2, 0.8]}, 'moderate_success': {'min_overall_score': 60, 'key_factors': ['genre_appeal', 'production_feasibility'], 'length_range': [85, 130], 'emotional_intensity': [0.4, 1.0], 'sentiment_balance': [-0.5, 1.0]}, 'niche_success': {'min_overall_score': 50, 'key_factors': ['originality', 'dialogue_quality'], 'length_range': [80, 140], 'emotional_intensity': [0.3, 1.0], 'sentiment_balance': [-1.0, 1.0]}}

    def predict_commercial_success(self, analysis: Dict[str, Any], target_genre: Optional[str]=None) -> CommercialPrediction:
        """
        Prediz sucesso comercial baseado na análise do roteiro
        
        Args:
            analysis: Análise completa do roteiro
            target_genre: Gênero alvo (opcional, será inferido se não fornecido)
            
        Returns:
            Predição de sucesso comercial
        """
        if not target_genre:
            target_genre = self._infer_genre(analysis)
        factors = self._calculate_market_factors(analysis, target_genre)
        overall_score = self._calculate_weighted_score(factors)
        genre_data = self.genre_multipliers.get(target_genre, {})
        genre_multiplier = genre_data.get('commercial_multiplier', 1.0)
        overall_score *= genre_multiplier
        overall_score = min(1.0, overall_score)
        market_category = self._determine_market_category(overall_score, factors)
        target_audience = self._identify_target_audience(analysis, target_genre, factors)
        risk_level = self._assess_risk_level(overall_score, factors, target_genre)
        confidence = self._calculate_prediction_confidence(factors, analysis)
        strengths, concerns = self._identify_commercial_factors(factors, analysis)
        recommendations = self._generate_commercial_recommendations(factors, analysis, target_genre)
        comparable_films = self._find_comparable_films(analysis, target_genre, market_category)
        budget_estimate = self._estimate_budget_range(analysis, target_genre, market_category)
        return CommercialPrediction(overall_score=round(overall_score, 3), confidence=round(confidence, 3), risk_level=risk_level, market_category=market_category, target_audience=target_audience, factors=factors, strengths=strengths, concerns=concerns, recommendations=recommendations, comparable_films=comparable_films, budget_estimate=budget_estimate)

    def _calculate_market_factors(self, analysis: Dict[str, Any], genre: str) -> List[MarketFactor]:
        """Calcula fatores de mercado individuais"""
        factors = []
        score_card = analysis.get('detailed_report', {}).get('score_card', {})
        category_scores = score_card.get('category_scores', {})
        overall_score = score_card.get('overall_score', 0)
        structure_score = category_scores.get('structure', 0) / 100.0
        factors.append(MarketFactor(name='structure_quality', score=structure_score, weight=self.market_weights['structure_quality'], impact='positive' if structure_score > 0.7 else 'neutral' if structure_score > 0.5 else 'negative', confidence=0.9, rationale=f'Estrutura com score {structure_score:.1%} - base sólida é crucial comercialmente'))
        char_score = category_scores.get('characters', 0) / 100.0
        factors.append(MarketFactor(name='character_appeal', score=char_score, weight=self.market_weights['character_appeal'], impact='positive' if char_score > 0.7 else 'neutral' if char_score > 0.5 else 'negative', confidence=0.8, rationale=f'Personagens com score {char_score:.1%} - personagens cativantes vendem filmes'))
        emotional_score = 0.5
        if 'sentiment_analysis' in analysis:
            intensity = analysis['sentiment_analysis']['overall_analysis'].get('intensity', 0)
            emotional_score = min(1.0, intensity * 1.5) if intensity < 0.7 else 0.7 + (intensity - 0.7) * 0.5
        factors.append(MarketFactor(name='emotional_engagement', score=emotional_score, weight=self.market_weights['emotional_engagement'], impact='positive' if emotional_score > 0.6 else 'neutral' if emotional_score > 0.4 else 'negative', confidence=0.7 if 'sentiment_analysis' in analysis else 0.4, rationale=f'Engajamento emocional {emotional_score:.1%} - audiências buscam conexão emocional'))
        pacing_score = category_scores.get('pacing', 0) / 100.0
        factors.append(MarketFactor(name='pacing', score=pacing_score, weight=self.market_weights['pacing'], impact='positive' if pacing_score > 0.7 else 'neutral' if pacing_score > 0.5 else 'negative', confidence=0.8, rationale=f'Ritmo com score {pacing_score:.1%} - ritmo adequado mantém interesse'))
        concept_score = self._evaluate_marketable_concept(analysis, genre)
        factors.append(MarketFactor(name='marketable_concept', score=concept_score, weight=self.market_weights['marketable_concept'], impact='positive' if concept_score > 0.6 else 'neutral' if concept_score > 0.4 else 'negative', confidence=0.6, rationale=f'Conceito {concept_score:.1%} comercial - hook claro facilita marketing'))
        genre_appeal = self._evaluate_genre_appeal(analysis, genre)
        factors.append(MarketFactor(name='genre_appeal', score=genre_appeal, weight=self.market_weights['genre_appeal'], impact='positive' if genre_appeal > 0.7 else 'neutral' if genre_appeal > 0.5 else 'negative', confidence=0.7, rationale=f'Apelo de gênero {genre_appeal:.1%} - {genre} tem mercado estabelecido'))
        dialogue_score = category_scores.get('dialogue', 0) / 100.0
        factors.append(MarketFactor(name='dialogue_quality', score=dialogue_score, weight=self.market_weights['dialogue_quality'], impact='positive' if dialogue_score > 0.7 else 'neutral' if dialogue_score > 0.5 else 'negative', confidence=0.8, rationale=f'Diálogos com score {dialogue_score:.1%} - diálogos memoráveis geram buzz'))
        production_score = self._evaluate_production_feasibility(analysis)
        factors.append(MarketFactor(name='production_feasibility', score=production_score, weight=self.market_weights['production_feasibility'], impact='positive' if production_score > 0.7 else 'neutral' if production_score > 0.5 else 'negative', confidence=0.6, rationale=f'Viabilidade {production_score:.1%} - produção viável atrai investidores'))
        trend_score = self._evaluate_trend_alignment(analysis)
        factors.append(MarketFactor(name='trend_alignment', score=trend_score, weight=self.market_weights['trend_alignment'], impact='positive' if trend_score > 0.6 else 'neutral', confidence=0.5, rationale=f'Alinhamento {trend_score:.1%} com tendências atuais'))
        originality_score = self._evaluate_originality(analysis)
        factors.append(MarketFactor(name='originality', score=originality_score, weight=self.market_weights['originality'], impact='positive' if originality_score > 0.7 else 'neutral', confidence=0.5, rationale=f'Originalidade {originality_score:.1%} - diferenciação no mercado'))
        return factors

    def _evaluate_marketable_concept(self, analysis: Dict[str, Any], genre: str) -> float:
        """Avalia se o conceito é comercialmente vendável"""
        score = 0.5
        metadata = analysis.get('detailed_report', {}).get('metadata', {})
        script_info = metadata.get('script_info', {})
        pages = script_info.get('total_pages', 0)
        if 90 <= pages <= 120:
            score += 0.2
        elif 80 <= pages <= 130:
            score += 0.1
        char_count = script_info.get('characters', 0)
        if 3 <= char_count <= 6:
            score += 0.1
        genre_multipliers = {'action': 0.8, 'thriller': 0.8, 'horror': 0.9, 'comedy': 0.7, 'romance': 0.6, 'drama': 0.5, 'sci_fi': 0.6}
        score *= genre_multipliers.get(genre, 0.6)
        return min(1.0, score)

    def _evaluate_genre_appeal(self, analysis: Dict[str, Any], genre: str) -> float:
        """Avalia o apelo comercial do gênero"""
        genre_data = self.genre_multipliers.get(genre, {})
        base_appeal = genre_data.get('commercial_multiplier', 1.0) / 1.4
        category_scores = analysis.get('detailed_report', {}).get('score_card', {}).get('category_scores', {})
        execution_avg = sum(category_scores.values()) / len(category_scores) if category_scores else 50
        execution_multiplier = min(1.0, execution_avg / 70)
        return min(1.0, base_appeal * execution_multiplier)

    def _evaluate_production_feasibility(self, analysis: Dict[str, Any]) -> float:
        """Avalia viabilidade de produção"""
        score = 0.7
        metadata = analysis.get('detailed_report', {}).get('metadata', {})
        script_info = metadata.get('script_info', {})
        scenes = script_info.get('scenes', 0)
        if scenes < 50:
            score += 0.2
        elif scenes < 80:
            score += 0.1
        elif scenes > 120:
            score -= 0.1
        pages = script_info.get('total_pages', 0)
        if pages > 130:
            score -= 0.1
        return max(0.1, min(1.0, score))

    def _evaluate_trend_alignment(self, analysis: Dict[str, Any]) -> float:
        """Avalia alinhamento com tendências atuais"""
        score = 0.5
        if 'sentiment_analysis' in analysis:
            char_analysis = analysis['sentiment_analysis'].get('character_analysis', {})
            if len(char_analysis) >= 3:
                score += 0.2
        sentiment = analysis.get('sentiment_analysis', {}).get('overall_analysis', {})
        if sentiment.get('tone') not in ['negative']:
            score += 0.1
        return min(1.0, score)

    def _evaluate_originality(self, analysis: Dict[str, Any]) -> float:
        """Avalia originalidade do roteiro"""
        score = 0.5
        if 'sentiment_analysis' in analysis:
            char_analysis = analysis['sentiment_analysis'].get('character_analysis', {})
            if char_analysis:
                emotional_ranges = []
                for char_data in char_analysis.values():
                    range_data = char_data.get('sentiment_range', {})
                    range_size = range_data.get('max', 0) - range_data.get('min', 0)
                    emotional_ranges.append(range_size)
                if emotional_ranges:
                    avg_range = sum(emotional_ranges) / len(emotional_ranges)
                    if avg_range > 0.6:
                        score += 0.3
        structure_analysis = analysis.get('detailed_report', {}).get('detailed_analysis', {}).get('structure_analysis', {})
        if structure_analysis:
            three_act = structure_analysis.get('three_act_structure', {})
            if three_act:
                act2_pct = three_act.get('act2', {}).get('percentage', 0)
                if act2_pct < 45 or act2_pct > 60:
                    score += 0.2
        return min(1.0, score)

    def _calculate_weighted_score(self, factors: List[MarketFactor]) -> float:
        """Calcula score ponderado final"""
        weighted_sum = 0.0
        total_weight = 0.0
        for factor in factors:
            weighted_sum += factor.score * factor.weight
            total_weight += factor.weight
        return weighted_sum / total_weight if total_weight > 0 else 0.5

    def _determine_market_category(self, score: float, factors: List[MarketFactor]) -> str:
        """Determina categoria de mercado"""
        if score >= 0.75:
            return 'mainstream'
        elif score >= 0.55:
            return 'niche'
        else:
            return 'art_house'

    def _identify_target_audience(self, analysis: Dict[str, Any], genre: str, factors: List[MarketFactor]) -> List[str]:
        """Identifica audiência alvo"""
        audience = []
        genre_data = self.genre_multipliers.get(genre, {})
        base_demo = genre_data.get('target_demo', ['general'])
        audience.extend(base_demo)
        if 'sentiment_analysis' in analysis:
            intensity = analysis['sentiment_analysis']['overall_analysis'].get('intensity', 0)
            if intensity > 0.7:
                audience.append('intensity_seekers')
            tone = analysis['sentiment_analysis']['overall_analysis'].get('tone', 'neutral')
            if tone == 'positive':
                audience.append('feel_good_seekers')
        return list(set(audience))

    def _assess_risk_level(self, score: float, factors: List[MarketFactor], genre: str) -> str:
        """Avalia nível de risco comercial"""
        genre_data = self.genre_multipliers.get(genre, {})
        base_risk = genre_data.get('risk_level', 'medium')
        if score >= 0.8:
            return 'low'
        elif score >= 0.6:
            return 'medium' if base_risk != 'high' else 'medium'
        else:
            return 'high'

    def _calculate_prediction_confidence(self, factors: List[MarketFactor], analysis: Dict[str, Any]) -> float:
        """Calcula confiança na predição"""
        factor_confidence = sum((f.confidence for f in factors)) / len(factors)
        completeness_bonus = 0.0
        if 'sentiment_analysis' in analysis:
            completeness_bonus += 0.1
        if analysis.get('detailed_report', {}).get('detailed_analysis'):
            completeness_bonus += 0.1
        return min(1.0, factor_confidence + completeness_bonus)

    def _identify_commercial_factors(self, factors: List[MarketFactor], analysis: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Identifica pontos fortes e preocupações comerciais"""
        strengths = []
        concerns = []
        for factor in factors:
            if factor.impact == 'positive' and factor.score > 0.7:
                strengths.append(f"{factor.name.replace('_', ' ').title()}: {factor.rationale}")
            elif factor.impact == 'negative' or factor.score < 0.4:
                concerns.append(f"{factor.name.replace('_', ' ').title()}: {factor.rationale}")
        return (strengths[:5], concerns[:5])

    def _generate_commercial_recommendations(self, factors: List[MarketFactor], analysis: Dict[str, Any], genre: str) -> List[str]:
        """Gera recomendações para melhorar potencial comercial"""
        recommendations = []
        weak_factors = [f for f in factors if f.score < 0.5]
        for factor in weak_factors[:3]:
            if factor.name == 'structure_quality':
                recommendations.append('Fortaleça a estrutura de três atos para maior apelo comercial')
            elif factor.name == 'character_appeal':
                recommendations.append('Desenvolva personagens mais cativantes e relacionáveis')
            elif factor.name == 'pacing':
                recommendations.append('Ajuste o ritmo para manter engajamento constante')
            elif factor.name == 'emotional_engagement':
                recommendations.append('Amplie o impacto emocional das cenas-chave')
        if genre == 'drama':
            recommendations.append('Considere elementos comerciais (suspense, humor) para ampliar apelo')
        elif genre == 'horror':
            recommendations.append('Mantenha orçamento baixo para maximizar ROI')
        elif genre == 'action':
            recommendations.append('Foque em setpieces memoráveis e marketing internacional')
        return recommendations[:5]

    def _find_comparable_films(self, analysis: Dict[str, Any], genre: str, market_category: str) -> List[str]:
        """Encontra filmes comparáveis como referência"""
        comparables_db = {('action', 'mainstream'): ['Top Gun: Maverick', 'Mission: Impossible', 'Fast & Furious'], ('action', 'niche'): ['John Wick', 'Mad Max: Fury Road', 'The Raid'], ('thriller', 'mainstream'): ['Gone Girl', 'The Silence of the Lambs', 'Se7en'], ('horror', 'mainstream'): ['Get Out', 'A Quiet Place', 'IT'], ('horror', 'niche'): ['Hereditary', 'The Witch', 'Midsommar'], ('comedy', 'mainstream'): ['The Hangover', 'Bridesmaids', 'Superbad'], ('drama', 'mainstream'): ['Three Billboards', 'Manchester by the Sea', 'The Pursuit of Happyness'], ('drama', 'art_house'): ['Moonlight', 'Parasite', 'The Master'], ('romance', 'mainstream'): ['The Proposal', 'Crazy Rich Asians', 'To All the Boys'], ('sci_fi', 'mainstream'): ['Arrival', 'Ex Machina', 'Interstellar']}
        key = (genre, market_category)
        return comparables_db.get(key, ['Similar genre films'])

    def _estimate_budget_range(self, analysis: Dict[str, Any], genre: str, market_category: str) -> Dict[str, str]:
        """Estima faixa de orçamento necessária"""
        budget_ranges = {('action', 'mainstream'): {'low': '$50M', 'mid': '$100M', 'high': '$200M+'}, ('action', 'niche'): {'low': '$15M', 'mid': '$30M', 'high': '$60M'}, ('thriller', 'mainstream'): {'low': '$20M', 'mid': '$40M', 'high': '$80M'}, ('horror', 'mainstream'): {'low': '$5M', 'mid': '$15M', 'high': '$30M'}, ('horror', 'niche'): {'low': '$1M', 'mid': '$5M', 'high': '$15M'}, ('comedy', 'mainstream'): {'low': '$10M', 'mid': '$25M', 'high': '$50M'}, ('drama', 'mainstream'): {'low': '$5M', 'mid': '$15M', 'high': '$40M'}, ('drama', 'art_house'): {'low': '$1M', 'mid': '$5M', 'high': '$15M'}, ('romance', 'mainstream'): {'low': '$8M', 'mid': '$20M', 'high': '$40M'}, ('sci_fi', 'mainstream'): {'low': '$30M', 'mid': '$80M', 'high': '$150M+'}}
        key = (genre, market_category)
        return budget_ranges.get(key, {'low': '$5M', 'mid': '$15M', 'high': '$40M'})

    def _infer_genre(self, analysis: Dict[str, Any]) -> str:
        """Infere gênero baseado na análise"""
        if 'sentiment_analysis' in analysis:
            sentiment = analysis['sentiment_analysis']['overall_analysis']
            tone = sentiment.get('tone', 'neutral')
            intensity = sentiment.get('intensity', 0)
            if intensity > 0.8:
                return 'thriller'
            elif tone == 'negative' and intensity > 0.6:
                return 'drama'
            elif tone == 'positive':
                return 'comedy'
            else:
                return 'drama'
        return 'drama'
_commercial_predictor: Optional[CommercialPredictor] = None

def get_commercial_predictor() -> CommercialPredictor:
    """
    Retorna instância singleton do predictor
    
    Returns:
        CommercialPredictor configurado
    """
    global _commercial_predictor
    if _commercial_predictor is None:
        _commercial_predictor = CommercialPredictor()
    return _commercial_predictor

def predict_commercial_success(analysis: Dict[str, Any], target_genre: Optional[str]=None) -> CommercialPrediction:
    """Atalho para predição comercial"""
    predictor = get_commercial_predictor()
    return predictor.predict_commercial_success(analysis, target_genre)
__all__ = ['MarketFactor', 'CommercialPrediction', 'CommercialPredictor', 'get_commercial_predictor', 'predict_commercial_success']