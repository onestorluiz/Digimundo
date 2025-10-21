#!/usr/bin/env python3
"""
Specificity Score Calculator
Calcula score de especificidade de análises Script Doctor
Valida se análise é específica ao roteiro ou genérica
"""

import re
from typing import Dict, List, Set, Any


class SpecificityScoreCalculator:
    """Calcula score de especificidade da análise LLM."""

    def __init__(self, screenplay_text: str):
        """
        Inicializa calculadora com texto do roteiro.

        Args:
            screenplay_text: Texto completo do roteiro
        """
        self.screenplay = screenplay_text
        self.character_names = self._extract_character_names()

    def _extract_character_names(self) -> Set[str]:
        """Extrai nomes de personagens do roteiro."""
        names = set()

        # Padrão: linha com texto todo em maiúsculas (character names)
        pattern = r'^([A-Z][A-Z\s]+)\s*$'

        for line in self.screenplay.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                name = match.group(1).strip()
                # Filtrar scene headings e transitions
                if not any(x in name for x in ['INT.', 'EXT.', 'FADE', 'CUT', 'TO:', 'IN.', 'OUT.']):
                    # Remover parentheses
                    name = name.split('(')[0].strip()
                    if len(name) > 2:  # Nomes com pelo menos 3 chars
                        names.add(name)

        return names

    def count_scene_citations(self, text: str) -> int:
        """Conta referências específicas a cenas."""
        patterns = [
            r'\bscene\s+\d+\b',           # "scene 3", "scene 12"
            r'\bcena\s+\d+\b',            # "cena 3", "cena 8"
            r'\bin\s+scene\s+\d+\b',      # "in scene 3"
            r'\bna\s+cena\s+\d+\b',       # "na cena 3"
            r'\bSCENE\s+\d+\b',           # "SCENE 3"
            r'\bCENA\s+\d+\b',            # "CENA 3"
        ]

        citations = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            citations += len(matches)

        return citations

    def count_dialogue_quotes(self, text: str) -> int:
        """Conta citações diretas de diálogo."""
        patterns = [
            r'["""]([^"""]{15,})["""]',     # Aspas inglesas, min 15 chars
            r'[""]([^""]{15,})[""]',        # Aspas curvas
            r'says?\s+["""]([^"""]{10,})["""]',  # "says 'texto'"
            r':\s+["""]([^"""]{15,})["""]',      # Character: "texto"
        ]

        quotes = set()  # Use set para evitar duplicatas
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Filtrar citações substanciais
                if isinstance(match, str) and len(match) > 15:
                    quotes.add(match.strip())

        return len(quotes)

    def count_character_name_usage(self, text: str) -> int:
        """Conta quantas vezes nomes específicos são usados."""
        usage_count = 0

        for name in self.character_names:
            # Conta menções do nome (case insensitive)
            # Usa word boundary para evitar partial matches
            pattern = rf'\b{re.escape(name)}\b'
            count = len(re.findall(pattern, text, re.IGNORECASE))
            usage_count += count

        return usage_count

    def count_placeholders(self, text: str) -> int:
        """Conta placeholders genéricos."""
        patterns = [
            r'\[insert\s+\w+\s+here\]',
            r'\[example\s+needed\]',
            r'\[TODO:',
            r'\[TBD\]',
            r'\[see\s+above\]',
            r'\[reference\s+needed\]',
            r'e\.g\.\s*\.\.\.',
            r'for\s+example\s*\.\.\.',
            r'such\s+as\s*\.\.\.',
        ]

        placeholder_count = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            placeholder_count += len(matches)

        return placeholder_count

    def calculate_genericity_penalty(self, text: str) -> float:
        """Calcula penalidade por genericidade."""
        antipatterns = [
            # Referências vagas
            r'\bthe\s+screenplay\b',
            r'\bthis\s+script\b',
            r'\bthe\s+story\b',
            r'\bthe\s+protagonist\b',
            r'\bthe\s+main\s+character\b',
            r'\bone\s+scene\b',
            r'\bin\s+some\s+scenes\b',
            r'\bthroughout\s+the\s+narrative\b',
            r'\bthe\s+writer\b',
            # Frases genéricas
            r'\bcould\s+be\s+improved\b',
            r'\bneeds\s+work\b',
            r'\bhas\s+potential\b',
            r'\bdemonstrates\s+understanding\b',
            r'\bshows\s+promise\b',
        ]

        generic_count = 0
        for pattern in antipatterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            generic_count += len(matches)

        # Normalizar por tamanho do texto (por 1000 chars)
        text_length_chars = len(text)
        if text_length_chars == 0:
            return 0.0

        genericity_ratio = generic_count / (text_length_chars / 1000)

        # Penalidade: 0 a -0.3
        penalty = min(0.3, genericity_ratio * 0.05)

        return -penalty

    def calculate_scene_citation_score(self, citations: int) -> float:
        """Retorna score 0-1 baseado em citações de cena."""
        if citations >= 8:
            return 1.0
        elif citations >= 5:
            return 0.8
        elif citations >= 3:
            return 0.6
        elif citations >= 1:
            return 0.3
        else:
            return 0.0

    def calculate_dialogue_quote_score(self, quotes: int) -> float:
        """Retorna score 0-1 baseado em citações de diálogo."""
        if quotes >= 6:
            return 1.0
        elif quotes >= 4:
            return 0.8
        elif quotes >= 2:
            return 0.6
        elif quotes >= 1:
            return 0.3
        else:
            return 0.0

    def calculate_character_name_score(self, usage: int) -> float:
        """Retorna score 0-1 baseado em uso de nomes."""
        if usage >= 15:
            return 1.0
        elif usage >= 10:
            return 0.8
        elif usage >= 5:
            return 0.6
        elif usage >= 2:
            return 0.3
        else:
            return 0.0

    def calculate(self, analysis_text: str) -> Dict[str, Any]:
        """
        Calcula score completo de especificidade.

        Args:
            analysis_text: Texto da análise LLM

        Returns:
            Dict com score final e componentes detalhados
        """
        # Componentes
        scene_citations = self.count_scene_citations(analysis_text)
        dialogue_quotes = self.count_dialogue_quotes(analysis_text)
        character_usage = self.count_character_name_usage(analysis_text)
        placeholders = self.count_placeholders(analysis_text)

        # Scores individuais
        scene_score = self.calculate_scene_citation_score(scene_citations)
        dialogue_score = self.calculate_dialogue_quote_score(dialogue_quotes)
        character_score = self.calculate_character_name_score(character_usage)

        # Penalidades
        placeholder_penalty = min(
            placeholders * -0.1,  # -10% por placeholder
            -0.5  # Máximo -50%
        )
        genericity_penalty = self.calculate_genericity_penalty(analysis_text)

        # Score final (média ponderada)
        base_score = (
            scene_score * 0.30 +        # 30%
            dialogue_score * 0.40 +      # 40%
            character_score * 0.20 +     # 20%
            0.10                         # 10% base
        )

        # Aplicar penalidades
        final_score = max(0.0, min(1.0, base_score + placeholder_penalty + genericity_penalty))

        return {
            'final_score': final_score,
            'percentage': final_score * 100,
            'passed': final_score >= 0.60,
            'threshold': 0.60,
            'components': {
                'scene_citations': {
                    'count': scene_citations,
                    'score': scene_score,
                    'weight': 0.30,
                    'minimum': 3,
                    'good': 5,
                    'excellent': 8
                },
                'dialogue_quotes': {
                    'count': dialogue_quotes,
                    'score': dialogue_score,
                    'weight': 0.40,
                    'minimum': 2,
                    'good': 4,
                    'excellent': 6
                },
                'character_names': {
                    'count': character_usage,
                    'score': character_score,
                    'weight': 0.20,
                    'characters_found': list(self.character_names),
                    'minimum': 5,
                    'good': 10,
                    'excellent': 15
                },
                'base_bonus': {
                    'score': 0.10,
                    'weight': 0.10
                }
            },
            'penalties': {
                'placeholders': {
                    'count': placeholders,
                    'penalty': placeholder_penalty,
                    'max_penalty': -0.5
                },
                'genericity': {
                    'penalty': genericity_penalty,
                    'max_penalty': -0.3
                }
            },
            'metadata': {
                'analysis_length': len(analysis_text),
                'screenplay_length': len(self.screenplay),
                'character_count': len(self.character_names)
            }
        }


def main():
    """Teste da calculadora."""
    # Exemplo de uso
    screenplay = """
INT. KITCHEN - DAY

SAMANTHA, 28, sits at the table.

SAMANTHA
I can't remember anything.

ALBERTO enters.

ALBERTO
It's okay, daughter.
"""

    analysis_good = """
In scene 3, Samantha says "I can't remember anything" which reveals
her vulnerability. Alberto's response "It's okay, daughter" shows
his protective nature.
"""

    analysis_bad = """
The protagonist struggles with memory. The screenplay could be improved
by adding more character development.
"""

    calc = SpecificityScoreCalculator(screenplay)

    print("GOOD ANALYSIS:")
    result_good = calc.calculate(analysis_good)
    print(f"Score: {result_good['percentage']:.1f}%")
    print(f"Passed: {result_good['passed']}")

    print("\nBAD ANALYSIS:")
    result_bad = calc.calculate(analysis_bad)
    print(f"Score: {result_bad['percentage']:.1f}%")
    print(f"Passed: {result_bad['passed']}")


if __name__ == '__main__':
    main()
