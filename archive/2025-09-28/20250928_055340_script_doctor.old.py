#!/usr/bin/env python3
"""
Script Doctor Enhanced - Análise Avançada de Roteiros
Versão minimalista adaptada do sistema original
Integra com Ollama real, BM25 e Learning Lite
"""

import re
import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Padrões de roteiro
SCENE_RE = re.compile(r'^(INT\.|EXT\.|INT/EXT\.)\s+.+', re.I|re.M)
CHAR_RE = re.compile(r'^[A-Z][A-Z0-9\- ]+$', re.M)
DIALOGUE_RE = re.compile(r'^[A-Z][A-Z0-9\- ]+\n(.+?)(?=\n[A-Z]|\n\n|\Z)', re.M|re.S)
ACTION_RE = re.compile(r'^[A-Z].*?[.!?](?=\s+[A-Z]|\n|\Z)', re.M)

# Save the Cat Beats (15 beats com timing)
SAVE_THE_CAT_BEATS = {
    "opening_image": (0, 1),          # 0-1%
    "setup": (1, 10),                 # 1-10%
    "theme_stated": (5, 5),           # 5% (dentro do setup)
    "catalyst": (10, 12),             # 10-12%
    "debate": (12, 25),               # 12-25%
    "break_into_2": (25, 25),         # 25%
    "b_story": (30, 30),              # 30%
    "fun_and_games": (30, 50),        # 30-50%
    "midpoint": (50, 50),             # 50%
    "bad_guys_close_in": (50, 75),    # 50-75%
    "all_is_lost": (75, 75),          # 75%
    "dark_night": (75, 85),           # 75-85%
    "break_into_3": (85, 85),         # 85%
    "finale": (85, 99),               # 85-99%
    "final_image": (99, 100)          # 99-100%
}

@dataclass
class ScriptAnalysis:
    """Análise básica de roteiro"""
    scenes: int
    characters: int
    words: int
    avg_scene_len: float
    top_characters: List[str]
    notes: List[str]
    dialogue_ratio: float = 0.0
    pacing_score: float = 0.0
    beats: List = field(default_factory=list)  # Para compatibilidade com Learning

    def to_dict(self) -> Dict[str, Any]:
        return {
            'scenes': self.scenes,
            'characters': self.characters,
            'words': self.words,
            'avg_scene_len': self.avg_scene_len,
            'top_characters': self.top_characters,
            'notes': self.notes,
            'dialogue_ratio': self.dialogue_ratio,
            'pacing_score': self.pacing_score,
            'beats': self.beats
        }

@dataclass
class Beat:
    """Um beat narrativo"""
    name: str
    position_pct: float
    content: str
    confidence: float

@dataclass
class SaveTheCatAnalysis:
    """Análise Save the Cat"""
    beats: List[Beat]
    missing_beats: List[str]
    structure_score: float
    notes: List[str]

class ScriptDoctorEnhanced:
    """Script Doctor com análise avançada e aprendizado"""

    def __init__(self, use_ollama: bool = True, use_learning: bool = True):
        """
        Inicializa Script Doctor

        Args:
            use_ollama: Se True, usa Ollama para análise profunda
            use_learning: Se True, usa sistema de aprendizado
        """
        self.use_ollama = use_ollama
        self.use_learning = use_learning
        self.ollama = None
        self.learning = None

        if use_ollama:
            try:
                from .ollama import OllamaReal
                self.ollama = OllamaReal()
                logger.info(f"Ollama ativado: {self.ollama.default_model}")
            except Exception as e:
                logger.warning(f"Ollama não disponível: {e}")
                self.use_ollama = False

        if use_learning:
            try:
                from .learning import LearningLite
                self.learning = LearningLite()
                logger.info(f"Learning ativado: {len(self.learning.concepts)} conceitos")
            except Exception as e:
                logger.warning(f"Learning não disponível: {e}")
                self.use_learning = False

    def analyze_script(self, text: str, screenplay_name: str = "Unknown") -> ScriptAnalysis:
        """
        Análise básica de roteiro com aprendizado

        Args:
            text: Texto do roteiro
            screenplay_name: Nome do roteiro para learning

        Returns:
            ScriptAnalysis com métricas
        """
        # Encontrar cenas
        scenes = [m.group(0) for m in SCENE_RE.finditer(text)]
        spans = [m.span() for m in SCENE_RE.finditer(text)]
        lens = []

        # Calcular tamanho das cenas
        for i, (a, b) in enumerate(spans):
            end = spans[i+1][0] if i+1 < len(spans) else len(text)
            lens.append(len(text[a:end].split()))

        # Encontrar personagens
        chars = [m.group(0).strip() for m in CHAR_RE.finditer(text)]
        blacklist = {'INT', 'EXT', 'INT/EXT', 'FADE', 'CUT', 'CONTINUED'}
        cc = {}

        for c in chars:
            if len(c) < 3 or c in blacklist or c.endswith('.'):
                continue
            cc[c] = cc.get(c, 0) + 1

        # Estatísticas básicas
        words = len(text.split())
        avg = statistics.mean(lens) if lens else 0.0

        # Top personagens
        top = sorted(cc.items(), key=lambda x: x[1], reverse=True)[:8]

        # Diálogos
        dialogues = DIALOGUE_RE.findall(text)
        dialogue_words = sum(len(d.split()) for d in dialogues)
        dialogue_ratio = dialogue_words / words if words > 0 else 0.0

        # Pacing score (variação no tamanho das cenas)
        pacing_score = 0.0
        if lens and len(lens) > 1:
            pacing_score = statistics.stdev(lens) / avg if avg > 0 else 0.0

        # Notas
        notes = []
        if len(scenes) < 5:
            notes.append('Poucas cenas — verifique headings (INT./EXT.).')
        if avg > 400:
            notes.append('Cenas longas — considere respiros/variações.')
        if dialogue_ratio < 0.2:
            notes.append('Pouco diálogo — roteiro pode estar muito descritivo.')
        if dialogue_ratio > 0.7:
            notes.append('Muito diálogo — considere mais ação visual.')
        if pacing_score < 0.3:
            notes.append('Ritmo monótono — varie tamanho das cenas.')

        # Análise Save the Cat para beats
        stc_analysis = self.analyze_save_the_cat(text)

        analysis = ScriptAnalysis(
            scenes=len(scenes),
            characters=len(top),
            words=words,
            avg_scene_len=avg,
            top_characters=[n for n, _ in top],
            notes=notes,
            dialogue_ratio=dialogue_ratio,
            pacing_score=pacing_score,
            beats=stc_analysis.beats  # Adicionar beats para learning
        )

        # APRENDER com a análise
        if self.learning and screenplay_name != "Unknown":
            learned = self.learning.learn_from_analysis(analysis, screenplay_name)
            if learned:
                logger.info(f"Aprendeu {len(learned)} conceitos de {screenplay_name}")

        return analysis

    def analyze_save_the_cat(self, text: str) -> SaveTheCatAnalysis:
        """
        Análise Save the Cat com aprendizado

        Args:
            text: Texto do roteiro

        Returns:
            SaveTheCatAnalysis com beats identificados
        """
        total_words = len(text.split())
        beats_found = []
        missing_beats = []

        # Enriquecer análise com conhecimento aprendido
        base_prompt = "Analyze Save the Cat beats"
        if self.learning:
            base_prompt = self.learning.enrich_prompt(base_prompt, "save the cat structure")

        # Procurar cada beat
        for beat_name, (start_pct, end_pct) in SAVE_THE_CAT_BEATS.items():
            # Calcular posição no texto
            start_pos = int(len(text) * start_pct / 100)
            end_pos = int(len(text) * end_pct / 100)

            # Extrair trecho
            excerpt = text[start_pos:end_pos][:500]  # Primeiros 500 chars

            # Analisar com Ollama se disponível
            confidence = 0.5  # Default

            if self.ollama and self.ollama.default_model and len(excerpt) > 50:
                prompt = f"""{base_prompt}

                Analyze if this excerpt represents a "{beat_name.replace('_', ' ')}" beat:

                {excerpt}

                Reply with just a confidence score 0-1."""

                response = self.ollama.generate(
                    prompt,
                    temperature=0.3,
                    max_tokens=10,
                    timeout=5
                )

                if response.success:
                    try:
                        confidence = float(response.completion.strip())
                    except:
                        confidence = 0.5

            if confidence > 0.3:  # Threshold
                beats_found.append(Beat(
                    name=beat_name,
                    position_pct=(start_pct + end_pct) / 2,
                    content=excerpt[:200],
                    confidence=confidence
                ))
            else:
                missing_beats.append(beat_name)

        # Calcular score
        structure_score = len(beats_found) / len(SAVE_THE_CAT_BEATS)

        # Notas
        notes = []
        if structure_score < 0.5:
            notes.append("Estrutura incompleta - muitos beats ausentes")
        if structure_score > 0.8:
            notes.append("Boa estrutura Save the Cat")

        if "opening_image" in missing_beats:
            notes.append("Falta imagem de abertura forte")
        if "midpoint" in missing_beats:
            notes.append("Midpoint não identificado - revisar ponto de virada")

        return SaveTheCatAnalysis(
            beats=beats_found,
            missing_beats=missing_beats,
            structure_score=structure_score,
            notes=notes
        )

    def analyze_characters(self, text: str, character_name: str) -> Dict[str, Any]:
        """
        Análise profunda de personagem com aprendizado

        Args:
            text: Texto do roteiro
            character_name: Nome do personagem

        Returns:
            Análise do arco do personagem
        """
        analysis = {
            "name": character_name,
            "appearances": 0,
            "dialogue_count": 0,
            "arc_detected": False,
            "want": None,
            "need": None,
            "ghost": None,
            "lie": None,
            "truth": None
        }

        # Contar aparições
        pattern = re.compile(f"\\b{character_name}\\b", re.I)
        analysis["appearances"] = len(pattern.findall(text))

        # Contar diálogos
        dialogue_pattern = re.compile(f"^{character_name}\\n(.+?)(?=\\n[A-Z]|\\n\\n|\\Z)", re.M|re.S)
        dialogues = dialogue_pattern.findall(text)
        analysis["dialogue_count"] = len(dialogues)

        # Enriquecer análise com conhecimento aprendido
        base_prompt = f"Analyze the character arc for {character_name}"
        if self.learning:
            base_prompt = self.learning.enrich_prompt(base_prompt, f"character {character_name}")

        # Analisar arco com Ollama
        if self.ollama and self.ollama.default_model and dialogues:
            sample_dialogue = "\n".join(dialogues[:5])  # Primeiros 5 diálogos

            prompt = f"""{base_prompt}

            Sample dialogue:
            {sample_dialogue}

            Identify:
            1. WANT (external goal)
            2. NEED (internal growth)
            3. GHOST (backstory/wound)
            4. LIE (false belief)
            5. TRUTH (realization)

            Format: JSON object with keys: want, need, ghost, lie, truth"""

            response = self.ollama.generate(
                prompt,
                temperature=0.7,
                max_tokens=200,
                timeout=10
            )

            if response.success:
                try:
                    import json
                    arc_data = json.loads(response.completion)
                    analysis.update(arc_data)
                    analysis["arc_detected"] = True
                except:
                    pass

        return analysis

    def get_learning_stats(self) -> Dict:
        """Retorna estatísticas do aprendizado"""
        if self.learning:
            return self.learning.get_statistics()
        return {"message": "Learning not enabled"}

# Função de compatibilidade
def analyze_script(text: str) -> ScriptAnalysis:
    """Análise rápida (compatibilidade)"""
    doctor = ScriptDoctorEnhanced(use_ollama=False, use_learning=False)
    return doctor.analyze_script(text)

# Teste
if __name__ == "__main__":
    print("Script Doctor Enhanced com Learning - Teste")

    # Texto de exemplo
    sample = """INT. CAFÉ - DAY

    JOHN enters the busy café.

    JOHN
    I need to find her before it's too late.

    MARY appears at the door.

    MARY
    You're already too late, John.

    EXT. STREET - CONTINUOUS

    They run into the rain."""

    doctor = ScriptDoctorEnhanced()

    # Análise básica
    analysis = doctor.analyze_script(sample, "Sample_Script")
    print(f"\n📊 Análise Básica:")
    print(f"  Cenas: {analysis.scenes}")
    print(f"  Personagens: {analysis.top_characters}")
    print(f"  Diálogo: {analysis.dialogue_ratio:.1%}")

    # Save the Cat
    stc = doctor.analyze_save_the_cat(sample)
    print(f"\n🎬 Save the Cat:")
    print(f"  Score: {stc.structure_score:.1%}")
    print(f"  Beats encontrados: {len(stc.beats)}")

    # Learning stats
    stats = doctor.get_learning_stats()
    print(f"\n📚 Learning Stats:")
    print(f"  Total conceitos: {stats.get('total_concepts', 0)}")

    print("\n✅ Script Doctor Enhanced com Learning funcionando!")