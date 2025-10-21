import re, statistics
from dataclasses import dataclass
from typing import List, Dict, Any

SCENE_RE = re.compile(r"^(INT\.|EXT\.|INT/EXT\.)\s+.+", re.I | re.M)
CHAR_RE = re.compile(r"^[A-Z][A-Z0-9\- ]+$", re.M)  # linhas de personagem (simplificado)

@dataclass
class ScriptAnalysis:
    scenes: int
    characters: int
    words: int
    avg_scene_len: float
    top_characters: List[str]
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenes": self.scenes,
            "characters": self.characters,
            "words": self.words,
            "avg_scene_len": self.avg_scene_len,
            "top_characters": self.top_characters,
            "notes": self.notes,
        }

def analyze_script(text: str) -> ScriptAnalysis:
    scenes = [m.group(0) for m in SCENE_RE.finditer(text)]
    scene_spans = [m.span() for m in SCENE_RE.finditer(text)]
    scene_lengths = []
    for i, (a, b) in enumerate(scene_spans):
        end = scene_spans[i+1][0] if i+1 < len(scene_spans) else len(text)
        scene_lengths.append(len(text[a:end].split()))
    chars = [m.group(0).strip() for m in CHAR_RE.finditer(text)]
    # Filtra cabeçalhos e CAPs comuns
    blacklist = {"INT", "EXT", "INT/EXT"}
    char_counts = {}
    for c in chars:
        if len(c) < 3 or c in blacklist or c.endswith("."):
            continue
        char_counts[c] = char_counts.get(c, 0) + 1

    words = len(text.split())
    avg_len = statistics.mean(scene_lengths) if scene_lengths else 0.0
    top_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    notes = []
    if len(scenes) < 5:
        notes.append("Poucas cenas detectadas — verifique formatação de headings (INT./EXT.).")
    if avg_len > 400:
        notes.append("Cenas longas — considere respiros/variações de ritmo.")

    return ScriptAnalysis(
        scenes=len(scenes),
        characters=len(top_chars),
        words=words,
        avg_scene_len=avg_len,
        top_characters=[n for n,_ in top_chars],
        notes=notes,
    )
