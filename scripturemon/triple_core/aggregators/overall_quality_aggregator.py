#!/usr/bin/env python3
"""
Overall Quality Aggregator - Triple-Core Version

Agrega resultados de todos os 22 especialistas Triple-Core em um score de qualidade geral.
NÃO analisa o screenplay diretamente - apenas agrega resultados de outros especialistas.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from collections import defaultdict
import statistics


@dataclass
class QualityDimensionScore:
    """Score agregado de uma dimensão de qualidade."""
    dimension: str
    score: float  # 0-100
    specialist_count: int
    specialists: List[str]
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)


@dataclass
class OverallQualityResult:
    """Resultado da agregação de qualidade."""
    overall_score: float  # 0-100
    quality_level: str  # amateur, developing, competent, professional, excellent, masterful

    # Scores por dimensão
    narrative_score: float  # Structure, Pacing, Opening, Climax, Resolution, Transitions
    character_score: float  # Psychology, Arcs, Relationships
    dialogue_score: float  # Dialogue, Voice
    technical_score: float  # Formatting, Action
    depth_score: float  # Subtext, Symbolism, Theme, Tone, Visual Motifs
    craft_score: float  # Genre, World Building
    market_score: float  # Originality, Market Potential

    # Detalhes
    dimension_scores: List[QualityDimensionScore]
    specialist_results: Dict[str, Dict[str, Any]]  # Resultados de cada especialista
    recommendations: List[str]
    critical_issues: List[str]
    standout_elements: List[str]


class OverallQualityAggregator:
    """Agregador de qualidade geral baseado em resultados Triple-Core."""

    def __init__(self):
        self.name = "Overall Quality Aggregator"

        # Mapeamento de especialistas para dimensões
        self.dimension_mapping = {
            'narrative': [
                'Structure', 'Pacing', 'Opening', 'Climax', 'Resolution', 'Transitions'
            ],
            'character': [
                'Character Psychology', 'Character Arcs', 'Character Relationships'
            ],
            'dialogue': [
                'Dialogue', 'Voice Consistency'
            ],
            'technical': [
                'Formatting', 'Action Description'
            ],
            'depth': [
                'Subtext', 'Symbolism', 'Theme Consistency',
                'Tone Consistency', 'Visual Motifs'
            ],
            'craft': [
                'Genre Conventions', 'World Building'
            ],
            'market': [
                'Originality', 'Market Potential'
            ]
        }

        # Quality levels
        self.quality_levels = [
            (90, 'masterful'),
            (80, 'excellent'),
            (70, 'professional'),
            (60, 'competent'),
            (50, 'developing'),
            (0, 'amateur')
        ]

    def aggregate(self, specialist_results: Dict[str, Dict[str, Any]]) -> OverallQualityResult:
        """
        Agrega resultados de todos os especialistas Triple-Core.

        Args:
            specialist_results: Dict com {specialist_name: result_dict}
                Cada result_dict deve ter pelo menos {'score': int, ...}

        Returns:
            OverallQualityResult com scores agregados
        """
        # Agregar scores por dimensão
        dimension_scores = self._aggregate_by_dimension(specialist_results)

        # Calcular scores de alto nível
        narrative_score = self._get_dimension_score(dimension_scores, 'narrative')
        character_score = self._get_dimension_score(dimension_scores, 'character')
        dialogue_score = self._get_dimension_score(dimension_scores, 'dialogue')
        technical_score = self._get_dimension_score(dimension_scores, 'technical')
        depth_score = self._get_dimension_score(dimension_scores, 'depth')
        craft_score = self._get_dimension_score(dimension_scores, 'craft')
        market_score = self._get_dimension_score(dimension_scores, 'market')

        # Calcular score geral (weighted average)
        overall_score = self._calculate_overall_score(
            narrative_score, character_score, dialogue_score,
            technical_score, depth_score, craft_score, market_score
        )

        # Determinar quality level
        quality_level = self._get_quality_level(overall_score)

        # Gerar recomendações
        recommendations = self._generate_recommendations(
            dimension_scores, specialist_results
        )

        # Identificar problemas críticos
        critical_issues = self._identify_critical_issues(specialist_results)

        # Identificar elementos de destaque
        standout_elements = self._identify_standout_elements(specialist_results)

        return OverallQualityResult(
            overall_score=overall_score,
            quality_level=quality_level,
            narrative_score=narrative_score,
            character_score=character_score,
            dialogue_score=dialogue_score,
            technical_score=technical_score,
            depth_score=depth_score,
            craft_score=craft_score,
            market_score=market_score,
            dimension_scores=dimension_scores,
            specialist_results=specialist_results,
            recommendations=recommendations,
            critical_issues=critical_issues,
            standout_elements=standout_elements
        )

    def _aggregate_by_dimension(
        self, specialist_results: Dict[str, Dict[str, Any]]
    ) -> List[QualityDimensionScore]:
        """Agrega scores por dimensão de qualidade."""
        dimension_scores = []

        for dimension, specialists in self.dimension_mapping.items():
            scores = []
            specialist_names = []
            strengths = []
            weaknesses = []

            for specialist_name, result in specialist_results.items():
                # Match specialist name (fuzzy)
                if any(spec.lower() in specialist_name.lower() for spec in specialists):
                    score = result.get('score', 0)
                    scores.append(score)
                    specialist_names.append(specialist_name)

                    # Coletar strengths/weaknesses
                    if score >= 80:
                        strengths.append(f"{specialist_name}: {score}/100")
                    elif score < 60:
                        weaknesses.append(f"{specialist_name}: {score}/100")

            if scores:
                avg_score = statistics.mean(scores)
                dimension_scores.append(
                    QualityDimensionScore(
                        dimension=dimension,
                        score=avg_score,
                        specialist_count=len(scores),
                        specialists=specialist_names,
                        strengths=strengths,
                        weaknesses=weaknesses
                    )
                )

        return dimension_scores

    def _get_dimension_score(
        self, dimension_scores: List[QualityDimensionScore], dimension: str
    ) -> float:
        """Obtém score de uma dimensão específica."""
        for dim_score in dimension_scores:
            if dim_score.dimension == dimension:
                return dim_score.score
        return 0.0

    def _calculate_overall_score(
        self, narrative: float, character: float, dialogue: float,
        technical: float, depth: float, craft: float, market: float
    ) -> float:
        """Calcula score geral com pesos."""
        weights = {
            'narrative': 0.25,  # Estrutura é fundamental
            'character': 0.20,  # Personagens são cruciais
            'dialogue': 0.15,  # Diálogo importante
            'technical': 0.10,  # Formatação necessária
            'depth': 0.15,  # Profundidade adiciona valor
            'craft': 0.10,  # Craft skills importantes
            'market': 0.05   # Mercado é bonus
        }

        overall = (
            narrative * weights['narrative'] +
            character * weights['character'] +
            dialogue * weights['dialogue'] +
            technical * weights['technical'] +
            depth * weights['depth'] +
            craft * weights['craft'] +
            market * weights['market']
        )

        return round(overall, 1)

    def _get_quality_level(self, score: float) -> str:
        """Determina quality level baseado no score."""
        for threshold, level in self.quality_levels:
            if score >= threshold:
                return level
        return 'amateur'

    def _generate_recommendations(
        self, dimension_scores: List[QualityDimensionScore],
        specialist_results: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Gera recomendações de alto nível."""
        recommendations = []

        # Recomendar baseado em dimensões fracas
        for dim_score in dimension_scores:
            if dim_score.score < 60:
                recommendations.append(
                    f"PRIORITY: Improve {dim_score.dimension} "
                    f"(current score: {dim_score.score:.1f}/100)"
                )

        # Adicionar top 3 recomendações de especialistas com scores mais baixos
        specialist_scores = [
            (name, result.get('score', 0), result.get('recommendations', []))
            for name, result in specialist_results.items()
        ]
        specialist_scores.sort(key=lambda x: x[1])  # Sort by score

        for name, score, recs in specialist_scores[:3]:
            if recs and score < 70:
                # Pegar primeira recomendação
                recommendations.append(f"[{name}] {recs[0]}")

        return recommendations[:10]  # Max 10 recomendações

    def _identify_critical_issues(
        self, specialist_results: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Identifica problemas críticos (scores < 50)."""
        critical = []

        for name, result in specialist_results.items():
            score = result.get('score', 0)
            if score < 50:
                critical.append(
                    f"{name}: CRITICAL ({score}/100) - "
                    f"{len(result.get('recommendations', []))} issues"
                )

        return critical

    def _identify_standout_elements(
        self, specialist_results: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Identifica elementos de destaque (scores >= 80)."""
        standout = []

        for name, result in specialist_results.items():
            score = result.get('score', 0)
            if score >= 80:
                standout.append(f"{name}: EXCELLENT ({score}/100)")

        return standout
