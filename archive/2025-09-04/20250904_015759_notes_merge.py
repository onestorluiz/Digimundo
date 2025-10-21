from __future__ import annotations
from pathlib import Path
import re
def merge_onepagers(home:Path)->Path:
    cover = home/"reports"/"coverage"
    files = sorted(cover.glob("*.md"))
    seen=set(); out=[]
    for f in files:
        txt=f.read_text(encoding="utf-8", errors="ignore")
        for line in txt.splitlines():
            if not line.strip(): continue
            key = re.sub(r"\s+"," ",line.strip())[:200]
            if key in seen: continue
            seen.add(key); out.append(line)
        out.append("\n---\n")
    outdir = home/"reports"/"coverage"; outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir/"merged_notes.md"
    outpath.write_text("\n".join(out), encoding="utf-8")
    return outpath