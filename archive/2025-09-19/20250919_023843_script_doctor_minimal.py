#!/usr/bin/env python3
"""
Script Doctor Minimal - Análise avançada de roteiros
Refatorado das 5 perguntas: 800+ → 200 linhas

RESPOSTAS ÀS 5 PERGUNTAS:
1. É necessário? SIM - Análise de roteiros é core
2. O que faz? Save the Cat beats + análise hierárquica
3. Quantas linhas? 200 vs 800+ (75% redução)
4. Dependências? Apenas stdlib (removido numpy/aiohttp)
5. Uma função? Não, mas drasticamente simplificado
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class StoryBeat(Enum):
    """Save the Cat beats com posições percentuais"""
    OPENING_IMAGE = 0.01
    CATALYST = 0.12
    BREAK_INTO_TWO = 0.25
    MIDPOINT = 0.50
    ALL_IS_LOST = 0.75
    FINALE = 0.90
    FINAL_IMAGE = 0.99

@dataclass
class BeatAnalysis:
    """Resultado da análise de um beat"""
    beat: StoryBeat
    position: int  # Página
    found: bool
    content: str
    confidence: float

class ScriptDoctorMinimal:
    """Análise minimalista mas poderosa de roteiros"""

    def __init__(self):
        self.beats_descriptions = {
            StoryBeat.OPENING_IMAGE: "Snapshot inicial do protagonista",
            StoryBeat.CATALYST: "Evento que inicia a história",
            StoryBeat.BREAK_INTO_TWO: "Entrada no novo mundo",
            StoryBeat.MIDPOINT: "Reviravolta central",
            StoryBeat.ALL_IS_LOST: "Ponto mais baixo",
            StoryBeat.FINALE: "Batalha final",
            StoryBeat.FINAL_IMAGE: "Transformação completa"
        }

    def analyze_script(self, script_text: str) -> Dict[str, any]:
        """Análise completa do roteiro"""

        # Divide em páginas (aproximadamente 1 página = 120 palavras)
        pages = self._split_into_pages(script_text)
        total_pages = len(pages)

        # Detecta beats
        beats = self._detect_beats(pages, total_pages)

        # Analisa estrutura
        structure_score = self._analyze_structure(beats)

        # Extrai personagens principais
        characters = self._extract_characters(script_text)

        # Analisa arco do protagonista
        protagonist_arc = self._analyze_protagonist_arc(script_text, characters[0] if characters else "PROTAGONIST")

        # Gera recomendações
        recommendations = self._generate_recommendations(beats, structure_score, protagonist_arc)

        return {
            'pages': total_pages,
            'beats': {b.beat.name: {
                'page': b.position,
                'found': b.found,
                'confidence': b.confidence
            } for b in beats},
            'structure_score': structure_score,
            'protagonist': characters[0] if characters else None,
            'characters': characters,
            'protagonist_arc': protagonist_arc,
            'recommendations': recommendations
        }

    def _split_into_pages(self, text: str) -> List[str]:
        """Divide texto em páginas (120 palavras ≈ 1 página)"""
        words = text.split()
        pages = []
        for i in range(0, len(words), 120):
            pages.append(' '.join(words[i:i+120]))
        return pages if pages else [text]

    def _detect_beats(self, pages: List[str], total_pages: int) -> List[BeatAnalysis]:
        """Detecta beats nas posições esperadas"""
        beats = []

        for beat in StoryBeat:
            expected_page = int(beat.value * total_pages)

            # Busca em janela de ±2 páginas
            found = False
            confidence = 0.0
            content = ""
            actual_page = expected_page

            for offset in range(-2, 3):
                page_num = expected_page + offset
                if 0 <= page_num < len(pages):
                    page_text = pages[page_num].upper()

                    # Detecta padrões específicos de cada beat
                    if self._check_beat_patterns(beat, page_text):
                        found = True
                        actual_page = page_num
                        confidence = 1.0 - (abs(offset) * 0.2)  # Reduz confiança se longe da posição esperada
                        content = pages[page_num][:100] + "..."
                        break

            beats.append(BeatAnalysis(
                beat=beat,
                position=actual_page,
                found=found,
                content=content,
                confidence=confidence
            ))

        return beats

    def _check_beat_patterns(self, beat: StoryBeat, text: str) -> bool:
        """Verifica padrões específicos de cada beat"""
        patterns = {
            StoryBeat.OPENING_IMAGE: ['FADE IN', 'INT.', 'EXT.'],
            StoryBeat.CATALYST: ['SUDDENLY', 'EXPLOSION', 'DIES', 'DISCOVERS', 'RECEIVES'],
            StoryBeat.BREAK_INTO_TWO: ['DECIDES', 'MUST', 'NO CHOICE', 'JOURNEY'],
            StoryBeat.MIDPOINT: ['REVELATION', 'TRUTH', 'REALIZES', 'DISCOVERS'],
            StoryBeat.ALL_IS_LOST: ['DEATH', 'LOST', 'DEFEATED', 'FAILS', 'DESTROYED'],
            StoryBeat.FINALE: ['FINAL', 'CONFRONTS', 'BATTLE', 'FACES'],
            StoryBeat.FINAL_IMAGE: ['FADE OUT', 'THE END', 'YEARS LATER']
        }

        beat_patterns = patterns.get(beat, [])
        return any(pattern in text for pattern in beat_patterns)

    def _analyze_structure(self, beats: List[BeatAnalysis]) -> float:
        """Calcula score de estrutura (0-100)"""
        found_beats = sum(1 for b in beats if b.found)
        confidence_sum = sum(b.confidence for b in beats if b.found)

        # 50% por beats encontrados, 50% por confiança
        found_score = (found_beats / len(beats)) * 50
        confidence_score = (confidence_sum / len(beats)) * 50 if found_beats > 0 else 0

        return found_score + confidence_score

    def _extract_characters(self, text: str) -> List[str]:
        """Extrai nomes de personagens (palavras em caps seguidas de diálogo)"""
        import re

        # Padrão: linha com apenas CAPS (nome do personagem)
        pattern = r'^([A-Z][A-Z\s]+)$'
        characters = set()

        for line in text.split('\n'):
            line = line.strip()
            if re.match(pattern, line) and len(line) < 30:  # Nome não pode ser muito longo
                # Remove indicações como (V.O.), (CONT'D)
                name = re.sub(r'\([^)]*\)', '', line).strip()
                if name and len(name) > 1:
                    characters.add(name)

        # Retorna top 10 personagens mais frequentes
        char_count = {}
        for char in characters:
            char_count[char] = text.count(char)

        sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)
        return [char for char, _ in sorted_chars[:10]]

    def _analyze_protagonist_arc(self, text: str, protagonist: str) -> Dict[str, str]:
        """Analisa arco do protagonista"""

        # Análise simplificada baseada em posição das menções
        mentions = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if protagonist in line.upper():
                mentions.append(i / len(lines))  # Posição percentual

        if not mentions:
            return {'want': 'Unknown', 'need': 'Unknown', 'change': 'Unknown'}

        # Início (primeiro 25%)
        early_mentions = [m for m in mentions if m < 0.25]
        # Final (último 25%)
        late_mentions = [m for m in mentions if m > 0.75]

        return {
            'want': 'External goal estabelecido' if early_mentions else 'Não claramente definido',
            'need': 'Transformação interna sugerida' if late_mentions else 'Arc incompleto',
            'change': 'Presente' if early_mentions and late_mentions else 'Ausente'
        }

    def _generate_recommendations(self, beats: List[BeatAnalysis], structure_score: float,
                                 protagonist_arc: Dict) -> List[str]:
        """Gera recomendações específicas"""
        recommendations = []

        # Estrutura
        if structure_score < 70:
            missing_beats = [b.beat.name for b in beats if not b.found]
            if missing_beats:
                recommendations.append(f"Fortalecer beats ausentes: {', '.join(missing_beats[:3])}")

        # Beats mal posicionados
        for beat in beats:
            if beat.found and beat.confidence < 0.6:
                recommendations.append(f"Reposicionar {beat.beat.name} para página ~{int(beat.beat.value * 120)}")

        # Arco do protagonista
        if protagonist_arc['change'] == 'Ausente':
            recommendations.append("Desenvolver transformação clara do protagonista")

        # Limita a 5 recomendações mais importantes
        return recommendations[:5] if recommendations else ["Estrutura sólida - focar em polimento de diálogos"]

# Exemplo de uso
if __name__ == "__main__":
    print("🎬 Testando Script Doctor Minimal...")

    sample_script = """
    FADE IN:

    INT. COFFEE SHOP - DAY

    JOHN, 30s, tired eyes, sits alone.

    JOHN
    Just another day...

    Suddenly, an EXPLOSION outside!

    JOHN
    What the hell?

    He must investigate. No choice.

    FADE OUT.
    """

    doctor = ScriptDoctorMinimal()
    analysis = doctor.analyze_script(sample_script)

    print(f"✅ Páginas: {analysis['pages']}")
    print(f"✅ Score estrutural: {analysis['structure_score']:.1f}/100")
    print(f"✅ Protagonista: {analysis['protagonist']}")
    print(f"✅ Recomendações: {len(analysis['recommendations'])}")

    print("\nDIGIMUNDO PRESENTE 🥷")