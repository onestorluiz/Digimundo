
from dataclasses import dataclass
import re
@dataclass
class Beat:
    id: str
    scene_index: int
    idx_in_scene: int
    text: str
    weight: float = 1.0
UPCASE = re.compile(r"^[A-Z .'-]{2,}$")
HEADER = re.compile(r"^(INT\\.|EXT\\.)")
TRIG = set(["agora","nunca","plano","prometo","sacrificio","sacrifício","fuga","ataque","verdade","segredo","decidir","decisão"])
STOP = set(["de","do","da","e","a","o","um","uma","nos","nas","dos","das","com","que","para","por","no","na","em"])
def _is_dialogue(line: str) -> bool: return bool(UPCASE.match(line.strip()))
def _is_header(line: str) -> bool: return bool(HEADER.match(line.strip()))
def _proper_candidates(line: str): return re.findall(r"(?:[A-ZÁ-Ú][a-zá-ú]+(?:\\s+[A-ZÁ-Ú][a-zá-ú]+){0,2})", line)
def _tokens(s: str): return [t for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+", s.lower()) if len(t) > 2 and t not in STOP]
def segment_beats_dynamic(scenes, max_lines_per_beat: int = 10, min_lines_per_beat: int = 3):
    beats = []
    for si, sc in enumerate(scenes, start=1):
        lines = [l for l in sc.text.splitlines()]
        i = 0; bi = 1
        while i < len(lines):
            j = min(len(lines), i + max_lines_per_beat)
            cur = [l for l in lines[i:j]]
            if len(cur) < min_lines_per_beat and j < len(lines):
                j = min(len(lines), j + (min_lines_per_beat - len(cur)))
                cur = [l for l in lines[i:j]]
            dlg = sum(1 for l in cur if _is_dialogue(l)); hdr = sum(1 for l in cur if _is_header(l))
            proper = set()
            for l in cur: proper |= set(_proper_candidates(l))
            trig = sum(1 for l in cur for t in _tokens(l) if t in TRIG)
            richness = len(proper)
            w = 1.0 + 0.4*(1 if dlg>0 else 0) + 0.3*(1 if trig>0 else 0) + 0.2*min(2, richness/3.0) + 0.1*(1 if hdr>0 else 0)
            w = max(1.0, min(3.0, w))
            text = "\\n".join(cur).strip()
            if text:
                beats.append(Beat(id=f"dyn_{si}_{bi}", scene_index=si, idx_in_scene=bi, text=text, weight=round(w,2)))
                bi += 1
            i = j
    return beats
def acts_from_line_count(lines_total: int):
    a = max(1, int(lines_total*0.25)); b = max(1, int(lines_total*0.50)); c = max(1, int(lines_total*0.75)); n=lines_total
    return {"act1": (1,a), "act2": (a+1,c), "act3": (c+1,n)}
