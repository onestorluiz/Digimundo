#!/usr/bin/env python
"""Test screenplay-optimized TPD."""
import sys
sys.path.append('.')
from pathlib import Path
from src.digilang.encoder import DigiLangEncoder
import tiktoken

enc_tk = tiktoken.get_encoding("cl100k_base")

# Test on synthetic screenplay
screenplay_file = Path("data/screenplay_synthetic/macbeth_screenplay.txt")
if not screenplay_file.exists():
    print("❌ No screenplay data. Run build_screenplay_synthetic.py first")
    exit(1)

text = screenplay_file.read_text()[:20000]

# Test different TPDs
configs = [
    ("Shakespeare TPD (K3000)", "data/tpd/default/token_dict.json"),
    ("Screenplay TPD (K2000)", "data/tpd/screenplay_K2000/token_dict.json"),
]

print("=" * 60)
print("SCREENPLAY COMPRESSION TEST")
print("=" * 60)
print(f"Test file: {screenplay_file.name}")
print(f"Original tokens: {len(enc_tk.encode(text))}")
print()

for name, tpd_path in configs:
    if not Path(tpd_path).exists():
        print(f"❌ {name}: Not found")
        continue
    
    encoder = DigiLangEncoder(use_tpd=True, token_dict_path=tpd_path)
    compressed, ratio = encoder.encode(text, canonicalize_text=True)
    
    tokens_after = len(enc_tk.encode(compressed))
    print(f"{name:25} | {ratio:.1%} compression | {tokens_after} tokens")

print("\n" + "=" * 60)
print("PREVIEW OF COMPRESSED TEXT")
print("=" * 60)
print(compressed[:500] + "...")