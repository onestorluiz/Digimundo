# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import re, subprocess, os, sys
def ensure_html():
    if not Path("reports/index.html").exists():
        subprocess.run([os.environ.get("PYTHON", sys.executable), "scripts/generate_report_html.py"], check=True)
        subprocess.run([os.environ.get("PYTHON", sys.executable), "scripts/patch_report_with_strategy.py"], check=True)
def extract_section(html:str, sec_id:str)->str:
    m=re.search(r'<section[^>]+id=["\']' + re.escape(sec_id) + r'["\'][^>]*>[\s\S]*?</section>', html, re.I)
    return m.group(0) if m else ""
def main():
    ensure_html()
    s=Path("reports/index.html").read_text(encoding="utf-8", errors="ignore")
    parts=[]
    for sec in ["production-strategy","ultimate-ui","ultimate-performance","ultimate-grid"]:
        frag=extract_section(s, sec)
        if frag: parts.append(frag)
    if not parts:
        print("[WARN] no sections found"); return
    doc=f"""<!DOCTYPE html>
<html><head><meta charset='utf-8'><title>Ultimate Panel</title>
<style>body{{font-family:system-ui,Arial,sans-serif;margin:16px;color:#111}} a{{text-decoration:none}} nav a{{margin-right:10px}}</style>
</head><body>
<nav><a href="#production-strategy">Strategy</a><a href="#ultimate-ui">Ultimate</a><a href="#ultimate-performance">Performance</a><a href="#ultimate-grid">Grid</a></nav>
{''.join(parts)}
</body></html>"""
    Path("reports/ultimate_panel.html").write_text(doc, encoding="utf-8")
    print("[OK] reports/ultimate_panel.html")
if __name__=="__main__": main()