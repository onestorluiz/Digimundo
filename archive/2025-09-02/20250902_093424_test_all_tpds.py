#!/usr/bin/env python
"""Test all TPD configurations to find the best."""
import sys
sys.path.append('.')
import subprocess
from pathlib import Path
import json

configs = [
    ("K800_n2-6", "data/tpd/K800_n2-6/token_dict.json"),
    ("K800_n2-8", "data/tpd/K800_n2-8/token_dict.json"),
    ("K1200_n2-6", "data/tpd/K1200_n2-6/token_dict.json"),
    ("K1200_n2-8", "data/tpd/K1200_n2-8/token_dict.json"),
    ("K2000_n2-6", "data/tpd/K2000_n2-6/token_dict.json"),
    ("K2000_n2-8", "data/tpd/K2000_n2-8/token_dict.json"),
]

results = []
print("=" * 60)
print("TPD CONFIGURATION COMPARISON")
print("=" * 60)

for name, path in configs:
    if not Path(path).exists():
        print(f"⚠️ Skipping {name} (not found)")
        continue
    
    # Load TPD info
    with open(path, 'r') as f:
        tpd = json.load(f)
    n_patterns = len(tpd.get("map", {}))
    
    # Quick test on first file only for speed
    cmd = f"./.venv/bin/python -c \"import sys; sys.path.append('.'); from src.digilang.encoder import DigiLangEncoder; from pathlib import Path; enc = DigiLangEncoder(use_tpd=True, token_dict_path='{path}'); text = Path('data/original/macbeth.txt').read_text()[:10000]; _, ratio = enc.encode(text); print(f'{{ratio:.1%}}')\""
    
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE, text=True)
        compression = result.strip().split('\n')[-1]  # Get last line only
        comp_value = float(compression.strip('%'))/100
        results.append((name, n_patterns, comp_value, compression))
        print(f"{name:15} | Patterns: {n_patterns:4} | Compression: {compression}")
    except:
        print(f"{name:15} | Failed to test")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if results:
    # Sort by compression ratio
    results.sort(key=lambda x: x[2], reverse=True)
    print("\nTop 3 configurations:")
    for i, (name, patterns, comp_val, comp_str) in enumerate(results[:3], 1):
        print(f"{i}. {name:15} - {comp_str} compression ({patterns} patterns)")
    
    best = results[0]
    print(f"\n✅ BEST: {best[0]} with {best[3]} compression")
    
    # Save recommendation
    rec_path = Path("results/tpd_recommendation.txt")
    rec_path.parent.mkdir(exist_ok=True)
    rec_path.write_text(f"Best TPD: {best[0]}\nPath: data/tpd/{best[0]}/token_dict.json\nCompression: {best[2]}\nPatterns: {best[1]}\n")