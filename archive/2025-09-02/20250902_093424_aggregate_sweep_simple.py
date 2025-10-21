#!/usr/bin/env python
"""
Simple aggregate TPD sweep results.
"""
import sys
sys.path.append('.')
import json
from pathlib import Path
import subprocess

results = []

for tpd_dir in Path("data/tpd").iterdir():
    if not tpd_dir.is_dir():
        continue
    
    tpd_path = tpd_dir / "token_dict.json"
    if not tpd_path.exists():
        continue
    
    # Load pattern count
    with open(tpd_path, 'r') as f:
        data = json.load(f)
        n_patterns = len(data.get("map", {}))
    
    # Quick test
    cmd = f"""./.venv/bin/python -c "
import sys; sys.path.append('.')
from src.digilang.encoder import DigiLangEncoder
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
enc = DigiLangEncoder(use_tpd=True, token_dict_path='{tpd_path}')
text = Path('data/original/macbeth.txt').read_text()[:10000]
_, ratio = enc.encode(text)
print(ratio)
" 2>/dev/null"""
    
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        lines = result.strip().split('\n')
        # Get last line that's a number
        for line in reversed(lines):
            try:
                compression = float(line.strip())
                break
            except:
                continue
        else:
            compression = 0
        
        results.append({
            "config": tpd_dir.name,
            "patterns": n_patterns,
            "compression": compression * 100
        })
        print(f"✅ {tpd_dir.name}: {compression:.1%}")
    except Exception as e:
        print(f"❌ {tpd_dir.name}: failed")

if results:
    print("\n" + "=" * 60)
    print("TPD CONFIGURATIONS RANKED")
    print("=" * 60)
    results.sort(key=lambda x: x['compression'], reverse=True)
    for r in results:
        print(f"{r['config']:20} | {r['patterns']:5} patterns | {r['compression']:.1f}%")
    
    best = results[0]
    print(f"\n✅ BEST: {best['config']} with {best['compression']:.1f}% compression")
else:
    print("[WARN] No results")