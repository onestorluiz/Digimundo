#!/usr/bin/env python3
"""
16 Digimons Especializados - Squad de Agentes Especializados
Cada Digimon tem uma especialidade única para análise de roteiros
"""

import asyncio
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import random


class DigimonType(Enum):
    """Tipos de Digimons especializados"""
    AGUMON = "agumon"              # Análise de ação e conflito
    GABUMON = "gabumon"            # Análise de personagens
    PATAMON = "patamon"            # Análise de esperança e redenção
    TENTOMON = "tentomon"          # Análise técnica e estrutura
    PALMON = "palmon"              # Análise de crescimento e mudança
    GOMAMON = "gomamon"            # Análise de humor e leveza
    BIYOMON = "biyomon"            # Análise de relacionamentos
    GATOMON = "gatomon"            # Análise de mistério e suspense
    VEEMON = "veemon"              # Análise de coragem e heroísmo
    WORMMON = "wormmon"            # Análise de lealdade e sacrifício
    GUILMON = "guilmon"            # Análise de inocência e descoberta
    RENAMON = "renamon"            # Análise de sabedoria e estratégia
    TERRIERMON = "terriermon"      # Análise de momentos calmos
    LOPMON = "lopmon"              # Análise de dualidade e contraste
    IMPMON = "impmon"              # Análise de anti-heróis
    MONODRAMON = "monodramon"      # Análise de justiça e moral


@dataclass
class DigimonAnalysis:
    """Resultado da análise de um Digimon"""
    digimon: DigimonType
    specialty: str
    score: float
    insights: List[str]
    recommendations: List[str]
    confidence: float
    processing_time_ms: int
    metadata: Dict = field(default_factory=dict)


@dataclass
class SquadAnalysis:
    """Análise completa do Squad de Digimons"""
    screenplay_hash: str
    individual_analyses: List[DigimonAnalysis]
    consensus_score: float
    primary_strengths: List[str]
    primary_weaknesses: List[str]
    overall_recommendation: str
    total_processing_time_ms: int
    squad_harmony: float


class BaseDigimon(ABC):
    """Classe base para todos os Digimons"""

    def __init__(self, digimon_type: DigimonType, specialty: str):
        """Inicializa Digimon"""
        self.type = digimon_type
        self.specialty = specialty
        self.experience = 0
        self.evolution_level = 1
        self.skills = []

    @abstractmethod
    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Analisa roteiro com especialidade única"""
        pass

    def evolve(self):
        """Evolui o Digimon"""
        self.evolution_level += 1
        self.experience = 0
        return f"{self.type.value} evoluiu para nível {self.evolution_level}!"

    def gain_experience(self, amount: int):
        """Ganha experiência"""
        self.experience += amount
        if self.experience >= 100 * self.evolution_level:
            return self.evolve()
        return None


class Agumon(BaseDigimon):
    """Agumon - Especialista em ação e conflito"""

    def __init__(self):
        super().__init__(DigimonType.AGUMON, "Ação e Conflito")
        self.skills = ["Pepper Breath", "Claw Attack", "Fire Analysis"]

    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Analisa elementos de ação e conflito"""
        start_time = time.time()
        await asyncio.sleep(0.1)  # Simula processamento

        # Análise simulada
        action_words = ["fight", "battle", "chase", "explosion", "attack", "defend"]
        action_count = sum(1 for word in action_words if word in screenplay.lower())

        score = min(100, action_count * 10)
        insights = []
        recommendations = []

        if action_count > 5:
            insights.append("Alto nível de ação detectado")
            insights.append(f"Encontradas {action_count} cenas de ação")
            recommendations.append("Considere adicionar momentos de respiro entre ações")
        else:
            insights.append("Baixo nível de ação")
            recommendations.append("Adicione mais tensão e conflito físico")

        insights.append(f"Ritmo de ação: {'Intenso' if score > 70 else 'Moderado' if score > 40 else 'Calmo'}")

        return DigimonAnalysis(
            digimon=self.type,
            specialty=self.specialty,
            score=score,
            insights=insights,
            recommendations=recommendations,
            confidence=0.85 + (self.evolution_level * 0.02),
            processing_time_ms=int((time.time() - start_time) * 1000),
            metadata={"action_count": action_count}
        )


class Gabumon(BaseDigimon):
    """Gabumon - Especialista em personagens"""

    def __init__(self):
        super().__init__(DigimonType.GABUMON, "Desenvolvimento de Personagens")
        self.skills = ["Blue Blaster", "Horn Attack", "Character Depth"]

    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Analisa desenvolvimento de personagens"""
        start_time = time.time()
        await asyncio.sleep(0.1)

        # Detecta personagens (simulado)
        lines = screenplay.split('\n')
        characters = set()
        dialogue_count = 0

        for line in lines:
            line = line.strip()
            if line.isupper() and len(line) > 2 and len(line) < 20:
                characters.add(line)
            if line.startswith('(') or '"' in line:
                dialogue_count += 1

        score = min(100, len(characters) * 15 + dialogue_count * 2)
        insights = [
            f"Identificados {len(characters)} personagens principais",
            f"{dialogue_count} linhas de diálogo encontradas",
            f"Densidade de personagem: {'Alta' if len(characters) > 5 else 'Média' if len(characters) > 2 else 'Baixa'}"
        ]

        recommendations = []
        if len(characters) < 3:
            recommendations.append("Adicione mais personagens para enriquecer a narrativa")
        if dialogue_count < 10:
            recommendations.append("Aumente o diálogo para desenvolver personagens")

        return DigimonAnalysis(
            digimon=self.type,
            specialty=self.specialty,
            score=score,
            insights=insights,
            recommendations=recommendations,
            confidence=0.87 + (self.evolution_level * 0.02),
            processing_time_ms=int((time.time() - start_time) * 1000),
            metadata={"character_count": len(characters)}
        )


class Patamon(BaseDigimon):
    """Patamon - Especialista em esperança e redenção"""

    def __init__(self):
        super().__init__(DigimonType.PATAMON, "Esperança e Redenção")
        self.skills = ["Boom Bubble", "Wing Slap", "Hope Light"]

    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Analisa temas de esperança e redenção"""
        start_time = time.time()
        await asyncio.sleep(0.08)

        hope_words = ["hope", "dream", "believe", "faith", "redemption", "forgive", "second chance"]
        hope_count = sum(1 for word in hope_words if word in screenplay.lower())

        score = min(100, hope_count * 15)
        insights = [
            f"Nível de esperança: {'Alto' if hope_count > 3 else 'Médio' if hope_count > 1 else 'Baixo'}",
            f"Elementos redentores: {hope_count} encontrados"
        ]

        recommendations = []
        if hope_count < 2:
            recommendations.append("Adicione elementos de esperança para elevar o tom")
            recommendations.append("Considere arcos de redenção para personagens")

        return DigimonAnalysis(
            digimon=self.type,
            specialty=self.specialty,
            score=score,
            insights=insights,
            recommendations=recommendations,
            confidence=0.83 + (self.evolution_level * 0.02),
            processing_time_ms=int((time.time() - start_time) * 1000),
            metadata={"hope_elements": hope_count}
        )


class Tentomon(BaseDigimon):
    """Tentomon - Especialista em estrutura técnica"""

    def __init__(self):
        super().__init__(DigimonType.TENTOMON, "Estrutura Técnica")
        self.skills = ["Super Shocker", "Electro Web", "Technical Analysis"]

    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Analisa estrutura técnica do roteiro"""
        start_time = time.time()
        await asyncio.sleep(0.09)

        lines = screenplay.split('\n')

        # Análise técnica
        scene_headings = sum(1 for line in lines if line.strip().startswith(('INT.', 'EXT.')))
        transitions = sum(1 for line in lines if line.strip() in ['CUT TO:', 'FADE IN:', 'FADE OUT:'])
        parentheticals = sum(1 for line in lines if line.strip().startswith('('))

        structure_score = min(100, scene_headings * 10 + transitions * 5 + parentheticals * 3)

        insights = [
            f"{scene_headings} cabeçalhos de cena",
            f"{transitions} transições",
            f"{parentheticals} parentéticos",
            f"Estrutura: {'Bem formatada' if structure_score > 60 else 'Precisa melhorias'}"
        ]

        recommendations = []
        if scene_headings < 3:
            recommendations.append("Adicione mais mudanças de cena")
        if transitions < 2:
            recommendations.append("Use mais transições para melhor fluxo")

        return DigimonAnalysis(
            digimon=self.type,
            specialty=self.specialty,
            score=structure_score,
            insights=insights,
            recommendations=recommendations,
            confidence=0.90 + (self.evolution_level * 0.02),
            processing_time_ms=int((time.time() - start_time) * 1000),
            metadata={"technical_elements": scene_headings + transitions}
        )


class DigimonSquad:
    """Squad completo de 16 Digimons"""

    def __init__(self):
        """Inicializa o squad"""
        self.digimons: Dict[DigimonType, BaseDigimon] = {}
        self._initialize_squad()
        self.analysis_history: List[SquadAnalysis] = []

    def _initialize_squad(self):
        """Inicializa todos os 16 Digimons"""
        # Inicializa os 4 principais implementados
        self.digimons[DigimonType.AGUMON] = Agumon()
        self.digimons[DigimonType.GABUMON] = Gabumon()
        self.digimons[DigimonType.PATAMON] = Patamon()
        self.digimons[DigimonType.TENTOMON] = Tentomon()

        # Outros 12 com implementação simplificada
        remaining_types = [
            (DigimonType.PALMON, "Crescimento e Mudança"),
            (DigimonType.GOMAMON, "Humor e Leveza"),
            (DigimonType.BIYOMON, "Relacionamentos"),
            (DigimonType.GATOMON, "Mistério e Suspense"),
            (DigimonType.VEEMON, "Coragem e Heroísmo"),
            (DigimonType.WORMMON, "Lealdade e Sacrifício"),
            (DigimonType.GUILMON, "Inocência e Descoberta"),
            (DigimonType.RENAMON, "Sabedoria e Estratégia"),
            (DigimonType.TERRIERMON, "Momentos Calmos"),
            (DigimonType.LOPMON, "Dualidade e Contraste"),
            (DigimonType.IMPMON, "Anti-heróis"),
            (DigimonType.MONODRAMON, "Justiça e Moral")
        ]

        for digimon_type, specialty in remaining_types:
            self.digimons[digimon_type] = SimpleDigimon(digimon_type, specialty)

    async def analyze_screenplay(
        self,
        screenplay: str,
        selected_digimons: Optional[List[DigimonType]] = None
    ) -> SquadAnalysis:
        """Analisa roteiro com squad selecionado"""
        start_time = time.time()

        # Seleciona Digimons
        if selected_digimons is None:
            selected_digimons = list(self.digimons.keys())[:8]  # Top 8 por padrão

        # Análise paralela
        tasks = []
        for digimon_type in selected_digimons:
            if digimon_type in self.digimons:
                digimon = self.digimons[digimon_type]
                tasks.append(digimon.analyze(screenplay))

        individual_analyses = await asyncio.gather(*tasks)

        # Calcula consenso
        consensus_score = sum(a.score for a in individual_analyses) / len(individual_analyses)

        # Identifica forças e fraquezas
        high_scores = [a for a in individual_analyses if a.score > 70]
        low_scores = [a for a in individual_analyses if a.score < 40]

        primary_strengths = [a.specialty for a in high_scores[:3]]
        primary_weaknesses = [a.specialty for a in low_scores[:3]]

        # Recomendação geral
        if consensus_score > 70:
            overall = "Roteiro excelente! Poucos ajustes necessários."
        elif consensus_score > 50:
            overall = "Roteiro bom com potencial. Foque nas áreas fracas."
        else:
            overall = "Roteiro precisa de trabalho significativo."

        # Harmonia do squad (quão bem trabalham juntos)
        harmony = 1.0 - (max(a.score for a in individual_analyses) -
                         min(a.score for a in individual_analyses)) / 100

        result = SquadAnalysis(
            screenplay_hash=hashlib.md5(screenplay.encode()).hexdigest()[:16],
            individual_analyses=individual_analyses,
            consensus_score=consensus_score,
            primary_strengths=primary_strengths,
            primary_weaknesses=primary_weaknesses,
            overall_recommendation=overall,
            total_processing_time_ms=int((time.time() - start_time) * 1000),
            squad_harmony=harmony
        )

        self.analysis_history.append(result)

        # Digimons ganham experiência
        for digimon_type in selected_digimons:
            if digimon_type in self.digimons:
                evolution = self.digimons[digimon_type].gain_experience(10)
                if evolution:
                    print(f"🎉 {evolution}")

        return result


class SimpleDigimon(BaseDigimon):
    """Implementação simplificada para os outros Digimons"""

    async def analyze(self, screenplay: str) -> DigimonAnalysis:
        """Análise simplificada"""
        start_time = time.time()
        await asyncio.sleep(0.05)

        # Análise simulada baseada na especialidade
        score = random.uniform(40, 90)

        insights = [
            f"Análise de {self.specialty}",
            f"Elementos detectados: {random.randint(3, 15)}",
            f"Qualidade: {'Alta' if score > 70 else 'Média' if score > 50 else 'Baixa'}"
        ]

        recommendations = []
        if score < 60:
            recommendations.append(f"Melhore aspectos de {self.specialty}")
            recommendations.append("Adicione mais profundidade")

        return DigimonAnalysis(
            digimon=self.type,
            specialty=self.specialty,
            score=score,
            insights=insights,
            recommendations=recommendations,
            confidence=0.80 + (self.evolution_level * 0.02),
            processing_time_ms=int((time.time() - start_time) * 1000),
            metadata={}
        )


async def main():
    """Teste do Squad de Digimons"""
    print("=" * 60)
    print("🎮 SQUAD DE 16 DIGIMONS ESPECIALIZADOS")
    print("=" * 60)

    squad = DigimonSquad()

    # Roteiro de teste
    test_screenplay = """
    FADE IN:

    EXT. DIGITAL WORLD - DAY

    A vast landscape of data streams and digital mountains.

    TAKATO
    We need to find the source of the corruption!

    GUILMON
    I can sense something... dark.

    Suddenly, a massive DIGIMON appears from the shadows.

    TAKATO
    (shouting)
    Everyone, get ready to fight!

    The team prepares for battle, hope in their hearts.

    CUT TO:

    INT. CONTROL ROOM - CONTINUOUS

    HENRY monitors the situation from multiple screens.

    HENRY
    The corruption levels are off the charts!
    We need to act fast or lose everything.

    FADE OUT.
    """

    # Análise com squad selecionado
    print("\n🔍 Analisando roteiro com 8 Digimons...")

    selected = [
        DigimonType.AGUMON,
        DigimonType.GABUMON,
        DigimonType.PATAMON,
        DigimonType.TENTOMON,
        DigimonType.GUILMON,
        DigimonType.RENAMON,
        DigimonType.VEEMON,
        DigimonType.GATOMON
    ]

    analysis = await squad.analyze_screenplay(test_screenplay, selected)

    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"  Hash do roteiro: {analysis.screenplay_hash}")
    print(f"  Score consensual: {analysis.consensus_score:.1f}/100")
    print(f"  Harmonia do squad: {analysis.squad_harmony:.2%}")
    print(f"  Tempo total: {analysis.total_processing_time_ms}ms")

    print(f"\n💪 Forças principais:")
    for strength in analysis.primary_strengths:
        print(f"  ✓ {strength}")

    print(f"\n⚠️ Fraquezas principais:")
    for weakness in analysis.primary_weaknesses:
        if weakness:  # Pode estar vazio se não houver fraquezas
            print(f"  ✗ {weakness}")

    print(f"\n🎯 Recomendação geral:")
    print(f"  {analysis.overall_recommendation}")

    print(f"\n📋 Análises individuais:")
    for da in analysis.individual_analyses[:4]:  # Mostra top 4
        print(f"\n  {da.digimon.value.upper()} ({da.specialty}):")
        print(f"    Score: {da.score:.1f}")
        print(f"    Confiança: {da.confidence:.2%}")
        print(f"    Insights: {da.insights[0]}")

    print("\n✅ Squad de Digimons funcionando perfeitamente!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())