
from dataclasses import dataclass
from typing import List, Dict, Tuple
import re, statistics

@dataclass
class Beat:
    id: str
    scene_index: int
    idx_in_scene: int
    text: str
    weight: float = 1.0

def _paragraphs(scene_text: str) -> List[str]:
    parts = [p.strip() for p in re.split(r"\n{2,}", scene_text) if p.strip()]
    out = []
    for p in parts:
        lines = [l for l in p.splitlines() if l.strip()]
        if len(lines) <= 8:
            out.append("\n".join(lines))
        else:
            for i in range(0, len(lines), 8):
                chunk = "\n".join(lines[i:i+8]).strip()
                if chunk: out.append(chunk)
    return out or ([scene_text.strip()] if scene_text.strip() else [])

def segment_beats_static(scenes: List, max_beats_per_scene: int = 12) -> List[Beat]:
    beats: List[Beat] = []
    for si, sc in enumerate(scenes, start=1):
        paras = _paragraphs(sc.text)[:max_beats_per_scene]
        for bi, p in enumerate(paras, start=1):
            beats.append(Beat(id=f"beat_{si}_{bi}", scene_index=si, idx_in_scene=bi, text=p, weight=1.0))
    return beats

# --- Dynamic beats ---
UPCASE = re.compile(r"^[A-Z .'-]{2,}$")
HEADER = re.compile(r"^(INT\\.|EXT\\.)")
TRIG = set(["agora","nunca","plano","prometo","sacrificio","sacrifício","fuga","ataque","verdade","segredo","decidir","decisão"])
STOP = set(["de","do","da","e","a","o","um","uma","nos","nas","dos","das","com","que","para","por","no","na","em"])

def _is_dialogue(line: str) -> bool:
    return bool(UPCASE.match(line.strip()))

def _is_header(line: str) -> bool:
    return bool(HEADER.match(line.strip()))

def _tokens(s: str) -> List[str]:
    return [t for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+", s.lower()) if len(t) > 2 and t not in STOP]

def _proper_candidates(line: str) -> List[str]:
    return re.findall(r"(?:[A-ZÁ-Ú][a-zá-ú]+(?:\\s+[A-ZÁ-Ú][a-zá-ú]+){0,2})", line)

def _change_score(prev_slice: list[str], cur_slice: list[str]) -> float:
    # vector: dialogue ratio, header presence, new proper nouns, trigger words
    def vec(slice_lines: list[str]):
        L = [l for l in slice_lines if l.strip()]
        if not L: return (0.0, 0.0, set(), 0.0)
        dlg = sum(1 for l in L if _is_dialogue(l)) / len(L)
        hdr = sum(1 for l in L if _is_header(l)) / len(L)
        proper = set()
        for l in L: proper |= set(_proper_candidates(l))
        trig = sum(1 for l in L for t in _tokens(l) if t in TRIG) / len(L)
        return (dlg, hdr, proper, trig)
    pd, ph, pp, pt = vec(prev_slice)
    cd, ch, cp, ct = vec(cur_slice)
    # distances
    dd = abs(pd - cd)
    dh = abs(ph - ch)
    dp = len(cp - pp) / max(1, len(cp | pp))
    dt = abs(pt - ct)
    return 0.5*dd + 0.2*dh + 0.2*dp + 0.1*dt

def segment_beats_dynamic(scenes: List, max_lines_per_beat: int = 10, min_lines_per_beat: int = 3) -> List[Beat]:
    beats: List[Beat] = []
    for si, sc in enumerate(scenes, start=1):
        lines = [l for l in sc.text.splitlines()]
        i = 0; bi = 1
        prev = []
        while i < len(lines):
            # grow current slice
            j = min(len(lines), i + max_lines_per_beat)
            cur = [l for l in lines[i:j]]
            # enforce minimum
            if len(cur) < min_lines_per_beat and j < len(lines):
                j = min(len(lines), j + (min_lines_per_beat - len(cur)))
                cur = [l for l in lines[i:j]]
            # compute change with lookahead window
            k = min(len(lines), j + max(3, max_lines_per_beat//2))
            nxt = [l for l in lines[j:k]]
            score = _change_score(prev or cur, nxt or cur)
            # threshold: higher when beats are too curtas; lower when long trecho
            base_thr = 0.35
            length_adj = 0.05 * max(0, (len(cur) - min_lines_per_beat))
            thr = base_thr - min(0.2, length_adj)
            # finalize beat
            text = "\n".join(cur).strip()
            if text:
                # weight: importance by dialogue switch + trigger + entity richness
                dlg = sum(1 for l in cur if _is_dialogue(l)); hdr = sum(1 for l in cur if _is_header(l))
                proper = set()
                for l in cur: proper |= set(_proper_candidates(l))
                trig = sum(1 for l in cur for t in _tokens(l) if t in TRIG)
                richness = len(proper)
                w = 1.0 + 0.4*(1 if dlg>0 else 0) + 0.3*(1 if trig>0 else 0) + 0.2*min(2, richness/3.0) + 0.1*(1 if hdr>0 else 0)
                w = max(1.0, min(3.0, w))
                beats.append(Beat(id=f"dyn_{si}_{bi}", scene_index=si, idx_in_scene=bi, text=text, weight=round(w,2)))
                bi += 1
            prev = cur
            # advance pointer: if change score high (frontier), break; else overlap a bit
            if score >= thr or j >= len(lines):
                i = j
            else:
                i = j - 2  # small overlap to avoid gaps
    return beats

def acts_from_line_count(lines_total: int) -> Dict[str, Tuple[int,int]]:
    a = max(1, int(lines_total*0.25)); b = max(1, int(lines_total*0.50)); c = max(1, int(lines_total*0.75)); n=lines_total
    return {"act1": (1,a), "act2": (a+1,c), "act3": (c+1,n)}
