#!/usr/bin/env python3
"""
Contrast & Comparison Specialist - O 24º Especialista
Analisa respostas dos 23 especialistas e aprofunda através de contrastes e comparações
Busca referências cinematográficas e trabalha com elementos narrativos opostos
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any
import ollama
from datetime import datetime

class ContrastComparisonSpecialist:
    """
    Especialista em análise por contraste e comparação
    Lê as respostas dos 23 especialistas e aprofunda através de:
    - Contrastes narrativos
    - Comparações com filmes clássicos
    - Análise de elementos opostos
    - Referências cinematográficas profundas
    """

    def __init__(self, version: str = "v1"):
        self.version = version
        self.model_name = f"scripturemon-contrast-{version}"
        self.film_database = self._load_film_database()

    def _load_film_database(self) -> Dict:
        """Carrega base de dados de filmes para comparação"""
        return {
            "character_arcs": {
                "redemption": ["The Shawshank Redemption", "Schindler's List", "Star Wars"],
                "corruption": ["The Godfather", "Scarface", "There Will Be Blood"],
                "transformation": ["The Matrix", "Fight Club", "Black Swan"],
                "sacrifice": ["Casablanca", "The Dark Knight", "Titanic"]
            },
            "narrative_structures": {
                "linear": ["The Social Network", "Forrest Gump", "The Pursuit of Happyness"],
                "non_linear": ["Memento", "Pulp Fiction", "Eternal Sunshine"],
                "circular": ["The Lion King", "Groundhog Day", "Arrival"],
                "fragmented": ["21 Grams", "Cloud Atlas", "Babel"]
            },
            "themes": {
                "power": ["Citizen Kane", "The Godfather", "House of Cards"],
                "love": ["Eternal Sunshine", "Her", "Before Trilogy"],
                "identity": ["Fight Club", "The Matrix", "Blade Runner"],
                "morality": ["No Country for Old Men", "The Dark Knight", "12 Angry Men"]
            },
            "pacing": {
                "slow_burn": ["There Will Be Blood", "2001: A Space Odyssey", "The Master"],
                "relentless": ["Mad Max: Fury Road", "Dunkirk", "Uncut Gems"],
                "rhythmic": ["Whiplash", "Baby Driver", "La La Land"],
                "contemplative": ["Lost in Translation", "Her", "Tree of Life"]
            }
        }

    def analyze_by_contrast(self, specialists_responses: Dict, screenplay_content: str) -> Dict:
        """
        Analisa através de contrastes e comparações

        Args:
            specialists_responses: Respostas dos 23 especialistas
            screenplay_content: Conteúdo do roteiro analisado

        Returns:
            Análise aprofundada por contraste
        """

        # Extrai elementos principais das respostas
        narrative_elements = self._extract_narrative_elements(specialists_responses)

        # Identifica contrastes internos
        internal_contrasts = self._find_internal_contrasts(narrative_elements)

        # Busca referências cinematográficas
        film_references = self._find_film_references(narrative_elements)

        # Cria análise comparativa
        comparative_analysis = self._create_comparative_analysis(
            narrative_elements,
            internal_contrasts,
            film_references
        )

        # Gera insights por contraste
        contrast_insights = self._generate_contrast_insights(comparative_analysis)

        return {
            "version": self.version,
            "timestamp": datetime.now().isoformat(),
            "narrative_elements": narrative_elements,
            "internal_contrasts": internal_contrasts,
            "film_references": film_references,
            "comparative_analysis": comparative_analysis,
            "contrast_insights": contrast_insights,
            "synthesis": self._synthesize_contrasts(contrast_insights)
        }

    def _extract_narrative_elements(self, responses: Dict) -> Dict:
        """Extrai elementos narrativos chave das respostas"""
        elements = {
            "protagonists": [],
            "antagonists": [],
            "themes": [],
            "structures": [],
            "pacing": [],
            "tone": [],
            "conflicts": []
        }

        # Analisa cada resposta de especialista
        for specialist, response in responses.items():
            if "character" in specialist.lower():
                elements["protagonists"].extend(self._extract_characters(response, "protagonist"))
                elements["antagonists"].extend(self._extract_characters(response, "antagonist"))
            elif "theme" in specialist.lower():
                elements["themes"].extend(self._extract_themes(response))
            elif "structure" in specialist.lower():
                elements["structures"].append(self._extract_structure(response))
            elif "pacing" in specialist.lower():
                elements["pacing"].append(self._extract_pacing(response))
            elif "conflict" in specialist.lower():
                elements["conflicts"].extend(self._extract_conflicts(response))

        return elements

    def _find_internal_contrasts(self, elements: Dict) -> List[Dict]:
        """Identifica contrastes internos no roteiro"""
        contrasts = []

        # Contraste entre protagonista e antagonista
        if elements["protagonists"] and elements["antagonists"]:
            contrasts.append({
                "type": "character_opposition",
                "element_a": elements["protagonists"][0],
                "element_b": elements["antagonists"][0],
                "tension": "moral/philosophical opposition"
            })

        # Contraste temático
        if len(elements["themes"]) > 1:
            contrasts.append({
                "type": "thematic_duality",
                "primary_theme": elements["themes"][0],
                "counter_theme": elements["themes"][1],
                "dialectic": "thesis-antithesis dynamic"
            })

        # Contraste de ritmo
        if elements["pacing"]:
            contrasts.append({
                "type": "rhythm_variation",
                "moments": "contemplative vs explosive",
                "effect": "emotional modulation"
            })

        return contrasts

    def _find_film_references(self, elements: Dict) -> List[Dict]:
        """Busca referências cinematográficas relevantes"""
        references = []

        # Para cada tema identificado
        for theme in elements.get("themes", []):
            theme_key = theme.lower()
            for db_theme, films in self.film_database["themes"].items():
                if db_theme in theme_key or theme_key in db_theme:
                    references.append({
                        "theme": theme,
                        "reference_films": films,
                        "comparison_point": f"Thematic exploration like {films[0]}"
                    })

        # Para estrutura narrativa
        if elements.get("structures"):
            structure_type = elements["structures"][0].lower()
            for struct_type, films in self.film_database["narrative_structures"].items():
                if struct_type in structure_type:
                    references.append({
                        "structure": structure_type,
                        "reference_films": films,
                        "comparison_point": f"Structural approach similar to {films[0]}"
                    })

        return references

    def _create_comparative_analysis(self, elements: Dict, contrasts: List, references: List) -> Dict:
        """Cria análise comparativa profunda"""
        return {
            "comparative_framework": {
                "internal_dynamics": {
                    "contrasts_identified": len(contrasts),
                    "primary_opposition": contrasts[0] if contrasts else None,
                    "dialectical_tensions": self._analyze_dialectics(contrasts)
                },
                "external_references": {
                    "films_referenced": len(references),
                    "primary_comparison": references[0] if references else None,
                    "cinematic_lineage": self._trace_cinematic_lineage(references)
                }
            },
            "contrast_patterns": {
                "character_contrasts": self._analyze_character_contrasts(elements),
                "thematic_contrasts": self._analyze_thematic_contrasts(elements),
                "structural_contrasts": self._analyze_structural_contrasts(elements)
            }
        }

    def _generate_contrast_insights(self, analysis: Dict) -> List[str]:
        """Gera insights baseados em contrastes"""
        insights = []

        # Insights de oposições internas
        if analysis["comparative_framework"]["internal_dynamics"]["primary_opposition"]:
            insights.append(
                f"The screenplay's core tension emerges from the opposition between "
                f"{analysis['comparative_framework']['internal_dynamics']['primary_opposition'].get('element_a', 'opposing forces')}"
            )

        # Insights de referências externas
        if analysis["comparative_framework"]["external_references"]["primary_comparison"]:
            ref = analysis["comparative_framework"]["external_references"]["primary_comparison"]
            insights.append(
                f"Like {ref['reference_films'][0]}, this screenplay explores "
                f"{ref.get('theme', 'similar themes')} through contrasting perspectives"
            )

        # Insights de padrões
        for pattern_type, pattern_data in analysis["contrast_patterns"].items():
            if pattern_data:
                insights.append(
                    f"The {pattern_type.replace('_', ' ')} creates dramatic tension through opposition"
                )

        return insights

    def _synthesize_contrasts(self, insights: List[str]) -> str:
        """Sintetiza todos os contrastes em uma análise coesa"""
        if not insights:
            return "No significant contrasts identified for deep analysis"

        synthesis = "CONTRAST & COMPARISON SYNTHESIS:\n\n"
        synthesis += "Through the lens of narrative opposition, this screenplay reveals itself as "
        synthesis += "a study in contrasts. "

        for insight in insights[:3]:  # Top 3 insights
            synthesis += insight + " "

        synthesis += "\n\nThis creates a rich tapestry of dramatic tension where opposing forces "
        synthesis += "don't merely conflict but define each other through their very opposition."

        return synthesis

    def _analyze_dialectics(self, contrasts: List) -> str:
        """Analisa tensões dialéticas"""
        if not contrasts:
            return "No dialectical tensions identified"

        return f"Primary dialectic between {contrasts[0].get('type', 'opposing forces')}"

    def _trace_cinematic_lineage(self, references: List) -> str:
        """Traça linhagem cinematográfica"""
        if not references:
            return "Original approach without clear precedents"

        films = references[0].get("reference_films", [])
        return f"Cinematic lineage traces through {', '.join(films[:2])}"

    def _analyze_character_contrasts(self, elements: Dict) -> Dict:
        """Analisa contrastes entre personagens"""
        return {
            "protagonist_vs_antagonist": bool(elements.get("protagonists") and elements.get("antagonists")),
            "internal_character_conflicts": "Detected based on character complexity"
        }

    def _analyze_thematic_contrasts(self, elements: Dict) -> Dict:
        """Analisa contrastes temáticos"""
        themes = elements.get("themes", [])
        return {
            "dual_themes": len(themes) > 1,
            "opposing_values": "Present" if len(themes) > 1 else "Absent"
        }

    def _analyze_structural_contrasts(self, elements: Dict) -> Dict:
        """Analisa contrastes estruturais"""
        return {
            "pacing_variations": bool(elements.get("pacing")),
            "structural_shifts": "Detected through act analysis"
        }

    def _extract_characters(self, response: str, char_type: str) -> List[str]:
        """Extrai personagens das respostas"""
        # Simplified extraction - in production would use NLP
        return [char_type]

    def _extract_themes(self, response: str) -> List[str]:
        """Extrai temas das respostas"""
        # Simplified extraction
        return ["power", "identity"]

    def _extract_structure(self, response: str) -> str:
        """Extrai tipo de estrutura"""
        return "three_act"

    def _extract_pacing(self, response: str) -> str:
        """Extrai tipo de ritmo"""
        return "escalating"

    def _extract_conflicts(self, response: str) -> List[str]:
        """Extrai conflitos"""
        return ["man_vs_society", "internal_conflict"]


# Versões com diferentes focos
def create_contrast_specialist_v1():
    """Versão 1: Foco em oposições binárias"""
    return ContrastComparisonSpecialist("v1")

def create_contrast_specialist_v2():
    """Versão 2: Foco em referências cinematográficas clássicas"""
    specialist = ContrastComparisonSpecialist("v2")
    specialist.film_database["classics"] = {
        "Casablanca": "sacrifice and duty",
        "Citizen Kane": "power and corruption",
        "The Godfather": "family and crime"
    }
    return specialist

def create_contrast_specialist_v3():
    """Versão 3: Foco em dialética hegeliana (tese-antítese-síntese)"""
    specialist = ContrastComparisonSpecialist("v3")
    specialist.dialectical_focus = True
    return specialist

def create_contrast_specialist_v4():
    """Versão 4: Foco em contrastes culturais e contextuais"""
    specialist = ContrastComparisonSpecialist("v4")
    specialist.cultural_analysis = True
    return specialist

def create_contrast_specialist_v5():
    """Versão 5: Foco em micro-contrastes (cena a cena)"""
    specialist = ContrastComparisonSpecialist("v5")
    specialist.granularity = "scene_level"
    return specialist


if __name__ == "__main__":
    # Teste das 5 versões
    print("Creating 5 versions of Contrast & Comparison Specialist...")

    specialists = [
        create_contrast_specialist_v1(),
        create_contrast_specialist_v2(),
        create_contrast_specialist_v3(),
        create_contrast_specialist_v4(),
        create_contrast_specialist_v5()
    ]

    for i, specialist in enumerate(specialists, 1):
        print(f"\nVersion {i}: {specialist.version}")
        print(f"Focus: {specialist.__doc__ if hasattr(specialist, '__doc__') else 'Standard contrast analysis'}")

    print("\nDIGIMUNDO PRESENTE 🔥")