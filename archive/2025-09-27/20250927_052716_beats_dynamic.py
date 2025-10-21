
from dataclasses import dataclass
from typing import List, Dict, Tuple
import re

@dataclass
class Beat:
    id: str
    scene_index: int
    idx_in_scene: int
    text: str

def _paragraphs(scene_text: str) -> List[str]:
    # Split by double newlines; keep only non-empty trimmed paragraphs
    parts = [p.strip() for p in re.split(r"\n{2,}", scene_text) if p.strip()]
    # If a part is too long, split softly every ~8 lines
    out = []
    for p in parts:
        lines = [l for l in p.splitlines()]
        if len(lines) <= 8:
            out.append("\n".join(lines))
        else:
            for i in range(0, len(lines), 8):
                out.append("\n".join(lines[i:i+8]))
    return out or ([scene_text.strip()] if scene_text.strip() else [])

def segment_beats(scenes: List, max_beats_per_scene: int = 12) -> List[Beat]:
    beats: List[Beat] = []
    for si, sc in enumerate(scenes, start=1):
        paras = _paragraphs(sc.text)[:max_beats_per_scene]
        for bi, p in enumerate(paras, start=1):
            beats.append(Beat(id=f"beat_{si}_{bi}", scene_index=si, idx_in_scene=bi, text=p))
    return beats

def acts_from_line_count(lines_total: int) -> Dict[str, Tuple[int,int]]:
    a = max(1, int(lines_total*0.25)); b = max(1, int(lines_total*0.50)); c = max(1, int(lines_total*0.75)); n=lines_total
    return {"act1": (1,a), "act2": (a+1,c), "act3": (c+1,n)}
