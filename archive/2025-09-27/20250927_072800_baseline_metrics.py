
import re
def ratio_dialogue(text: str) -> float:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    import re as _r
    dialogue = sum(1 for l in lines if _r.match(r"^[A-Z .'-]{2,}$", l))
    return dialogue / max(1,len(lines))
def avg_scene_len(text: str) -> float:
    scenes = re.split(r"\n(INT\.|EXT\.)", text)
    counts = [len(s.splitlines()) for s in scenes if s.strip()]
    return sum(counts)/max(1,len(counts))
