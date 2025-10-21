#!/usr/bin/env python3
"""
Learning Lite - Sistema de Aprendizado Minimalista
Versão simplificada que aproveita BM25 e memória existente
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class LearnedConcept:
    """Um conceito aprendido"""
    concept: str
    source: str
    confidence: float
    timestamp: str
    examples: List[str] = None

class LearningLite:
    """
    Sistema de aprendizado minimalista
    Usa BM25 e memória unificada existente
    """

    def __init__(self):
        self.learning_file = Path("data/learned_concepts.json")
        self.learning_file.parent.mkdir(parents=True, exist_ok=True)
        self.concepts = self._load_concepts()

    def _load_concepts(self) -> List[LearnedConcept]:
        """Carrega conceitos aprendidos"""
        if self.learning_file.exists():
            try:
                with open(self.learning_file, 'r') as f:
                    data = json.load(f)
                    return [LearnedConcept(**c) for c in data]
            except:
                pass
        return []

    def _save_concepts(self):
        """Salva conceitos aprendidos"""
        with open(self.learning_file, 'w') as f:
            json.dump([asdict(c) for c in self.concepts], f, indent=2)

    def learn_from_analysis(self,
                           analysis_result: Dict,
                           screenplay_name: str,
                           confidence_threshold: float = 0.7):
        """
        Aprende com resultado de análise

        Args:
            analysis_result: Resultado do Script Doctor
            screenplay_name: Nome do roteiro analisado
            confidence_threshold: Confiança mínima para aprender
        """
        learned = []

        # Aprender com Save the Cat beats detectados
        if hasattr(analysis_result, 'beats'):
            for beat in analysis_result.beats:
                if beat.confidence >= confidence_threshold:
                    concept = LearnedConcept(
                        concept=f"Beat {beat.name} typically at {beat.position_pct}%",
                        source=screenplay_name,
                        confidence=beat.confidence,
                        timestamp=datetime.now().isoformat(),
                        examples=[beat.content[:100]]
                    )
                    self.concepts.append(concept)
                    learned.append(concept)

        # Aprender com personagens principais
        if hasattr(analysis_result, 'top_characters'):
            if len(analysis_result.top_characters) > 0:
                concept = LearnedConcept(
                    concept=f"Protagonist pattern: {analysis_result.top_characters[0]}",
                    source=screenplay_name,
                    confidence=0.8,
                    timestamp=datetime.now().isoformat()
                )
                self.concepts.append(concept)
                learned.append(concept)

        # Aprender com estrutura
        if hasattr(analysis_result, 'pacing_score'):
            if analysis_result.pacing_score > 0.5:
                concept = LearnedConcept(
                    concept=f"Good pacing with variation score {analysis_result.pacing_score:.2f}",
                    source=screenplay_name,
                    confidence=0.75,
                    timestamp=datetime.now().isoformat()
                )
                self.concepts.append(concept)
                learned.append(concept)

        # Limitar tamanho da base de conhecimento
        if len(self.concepts) > 100:
            # Manter apenas os 100 mais recentes/confiáveis
            self.concepts.sort(key=lambda x: (x.confidence, x.timestamp), reverse=True)
            self.concepts = self.concepts[:100]

        # Salvar
        if learned:
            self._save_concepts()

        return learned

    def get_relevant_concepts(self, query: str, top_k: int = 5) -> List[LearnedConcept]:
        """
        Recupera conceitos relevantes para uma query

        Args:
            query: Texto de busca
            top_k: Número máximo de conceitos

        Returns:
            Lista de conceitos relevantes
        """
        if not self.concepts:
            return []

        # Scoring simples baseado em palavras-chave
        scored = []
        query_words = query.lower().split()

        for concept in self.concepts:
            score = 0
            concept_text = f"{concept.concept} {concept.source}".lower()

            for word in query_words:
                if word in concept_text:
                    score += concept.confidence

            if score > 0:
                scored.append((concept, score))

        # Ordenar por score e retornar top_k
        scored.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in scored[:top_k]]

    def enrich_prompt(self, base_prompt: str, context: str = "") -> str:
        """
        Enriquece um prompt com conhecimento aprendido

        Args:
            base_prompt: Prompt original
            context: Contexto adicional para busca

        Returns:
            Prompt enriquecido
        """
        # Buscar conceitos relevantes
        search_text = f"{base_prompt} {context}"
        concepts = self.get_relevant_concepts(search_text, top_k=3)

        if not concepts:
            return base_prompt

        # Adicionar seção de conhecimento
        enrichment = "\n\nConsider these learned patterns:\n"
        for concept in concepts:
            enrichment += f"- {concept.concept} (from {concept.source})\n"

        return base_prompt + enrichment

    def get_statistics(self) -> Dict:
        """Retorna estatísticas do aprendizado"""
        if not self.concepts:
            return {
                "total_concepts": 0,
                "sources": [],
                "avg_confidence": 0
            }

        sources = list(set(c.source for c in self.concepts))
        avg_conf = sum(c.confidence for c in self.concepts) / len(self.concepts)

        return {
            "total_concepts": len(self.concepts),
            "sources": sources,
            "avg_confidence": avg_conf,
            "top_concepts": [c.concept for c in self.concepts[:5]]
        }

# Teste rápido
if __name__ == "__main__":
    learning = LearningLite()

    # Simular aprendizado
    from scripturemon_champion.script_doctor import ScriptAnalysis

    mock_analysis = ScriptAnalysis(
        scenes=120,
        characters=5,
        words=25000,
        avg_scene_len=200,
        top_characters=["JOHN", "MARY"],
        notes=[],
        dialogue_ratio=0.4,
        pacing_score=0.7
    )

    learned = learning.learn_from_analysis(mock_analysis, "Test_Screenplay")

    print("📚 Aprendizado Lite")
    print(f"Conceitos aprendidos: {len(learned)}")

    stats = learning.get_statistics()
    print(f"Total na base: {stats['total_concepts']}")

    # Testar enriquecimento
    prompt = "Analyze the protagonist"
    enriched = learning.enrich_prompt(prompt)
    if enriched != prompt:
        print(f"\nPrompt enriquecido:")
        print(enriched)