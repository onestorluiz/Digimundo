#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera um corpus 'screenplay sintético' a partir de textos domínio público (ex.: Shakespeare),
convertendo em formato canônico de roteiro:
  INT./EXT. <LOCAL> - <DAY/NIGHT>
  AÇÃO
  PERSONAGEM
  Diálogo...
Objetivo: aumentar repetição de n-gramas de tokens e facilitar compressão por TPD.
Determinístico (seed=42), sem usar conteúdo protegido por copyright.
"""
import re, random, os
from pathlib import Path

SEED = 42
random.seed(SEED)

LOCATIONS = [
    "APARTMENT", "BACK ALLEY", "CITY STREET", "COUNTRYSIDE ROAD", "SMALL THEATER",
    "KITCHEN", "BEDROOM", "POLICE STATION", "HOSPITAL CORRIDOR", "ABANDONED WAREHOUSE",
    "SUBWAY PLATFORM", "RIVERSIDE", "ROOFTOP", "DINER", "SCHOOL HALLWAY"
]
TIMES = ["DAY", "NIGHT", "DAWN", "DUSK"]

def clean_text(t: str) -> str:
    t = t.replace("—","-").replace("–","-").replace(""","\"").replace(""","\"").replace("'","'")
    t = re.sub(r"\r\n?", "\n", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()

def guess_characters(text: str, k: int = 8):
    # Heurística: palavras MAIÚSCULAS com 3–14 chars e freq alta
    words = re.findall(r"\b[A-Z][A-Z\-]{2,14}\b", text.upper())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    chars = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:k]
    names = [c[0] for c in chars]
    # fallback se pouco material:
    while len(names) < k:
        names.append(f"CHAR_{len(names)+1:02d}")
    return names[:k]

def chunk_sentences(text: str, max_len: int = 240):
    # divide por parágrafos e linhas curtas
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]
    out = []
    for p in paras:
        sents = re.split(r"(?<=[\.\!\?])\s+", p)
        buf = ""
        for s in sents:
            if len(buf) + len(s) < max_len:
                buf += ((" " if buf else "") + s)
            else:
                if buf: out.append(buf.strip())
                buf = s
        if buf: out.append(buf.strip())
    # se não deu nada, cai para linhas:
    if not out:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return lines
    return out

def to_screenplay(sent_blocks, chars):
    scenes = []
    scene_count = max(8, min(40, len(sent_blocks)//10 + 1))
    i = 0
    for idx in range(scene_count):
        loc = random.choice(LOCATIONS)
        time = random.choice(TIMES)
        header = f"{'INT.' if idx % 2 == 0 else 'EXT.'} {loc} - {time}"
        body = []
        # Ação (1–3 blocos)
        act_n = random.randint(1,3)
        for _ in range(act_n):
            if i < len(sent_blocks):
                body.append(sent_blocks[i])
                i += 1
        # 2–4 falas
        talk_n = random.randint(2,4)
        for _ in range(talk_n):
            spk = random.choice(chars)
            text = ""
            if i < len(sent_blocks):
                text = sent_blocks[i]; i += 1
            else:
                text = "..."
            body.append(spk)
            body.append(text)
        scenes.append((header, body))
    return scenes

def write_screenplay(scenes, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        act = 1
        per_act = max(5, len(scenes)//3)
        for idx, (header, body) in enumerate(scenes, start=1):
            if idx == 1 or (idx-1) % per_act == 0:
                f.write(f"\n\n# ACT {act}\n")
                act += 1
            f.write("\n" + header + "\n")
            for line in body:
                if line.isupper() and len(line) <= 18:
                    # personagem
                    f.write(line + "\n")
                else:
                    f.write(line + "\n")

def main():
    in_dir = Path("data/original")
    out_dir = Path("data/screenplay_synth")
    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in in_dir.rglob("*.txt"):
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except:
            continue
        text = clean_text(raw)
        if not text: continue
        chars = guess_characters(text, k=8)
        blocks = chunk_sentences(text, max_len=220)
        scenes = to_screenplay(blocks, chars)
        out_path = out_dir / (p.stem + "_screenplay.txt")
        write_screenplay(scenes, out_path)
        count += 1
    print(f"[OK] Screenplay synthetic built: {count} files -> {out_dir}")

if __name__ == "__main__":
    main()