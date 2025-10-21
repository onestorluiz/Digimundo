#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick sweep - testa apenas o primeiro arquivo de cada corpus para ser mais rápido.
"""
import json
from pathlib import Path
import subprocess

def quick_test(tpd_path, corpus="data/original"):
    """Testa compressão rapidamente em um arquivo."""
    files = list(Path(corpus).glob("*.txt"))
    if not files:
        return 0
    
    test_file = files[0]
    
    cmd = f"""./.venv/bin/python -c "
import sys; sys.path.append('.')
from src.digilang.encoder import DigiLangEncoder
text = open('{test_file}', 'r').read()[:10000]
enc = DigiLangEncoder(use_tpd=True, token_dict_path='{tpd_path}')
_, ratio = enc.encode(text)
print(ratio)
" 2>/dev/null"""
    
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        lines = result.strip().split('\n')
        for line in reversed(lines):
            try:
                return float(line.strip())
            except:
                continue
    except:
        pass
    return 0

def main():
    results = []
    
    # Testar todas as configurações
    for tpd_dir in Path("data/tpd").glob("*"):
        if not tpd_dir.is_dir():
            continue
        
        tpd_path = tpd_dir / "token_dict.json"
        if not tpd_path.exists():
            continue
        
        # Teste em Shakespeare
        ratio_shakespeare = quick_test(tpd_path, "data/original")
        
        # Teste em Screenplay
        ratio_screenplay = quick_test(tpd_path, "data/screenplay_synth")
        
        # Média
        avg = (ratio_shakespeare + ratio_screenplay) / 2 if ratio_screenplay > 0 else ratio_shakespeare
        
        results.append({
            "config": tpd_dir.name,
            "shakespeare": ratio_shakespeare * 100,
            "screenplay": ratio_screenplay * 100,
            "average": avg * 100
        })
        
        print(f"{tpd_dir.name:20} | Shakespeare: {ratio_shakespeare:.1%} | Screenplay: {ratio_screenplay:.1%} | Avg: {avg:.1%}")
    
    # Ordenar por média
    results.sort(key=lambda x: x['average'], reverse=True)
    
    print("\n" + "=" * 70)
    print("TOP 3 CONFIGURATIONS")
    print("=" * 70)
    for i, r in enumerate(results[:3], 1):
        print(f"{i}. {r['config']:20} | Avg: {r['average']:.1f}% | Shakespeare: {r['shakespeare']:.1f}% | Screenplay: {r['screenplay']:.1f}%")
    
    # Salvar melhor configuração
    if results:
        best = results[0]
        print(f"\n✅ BEST: {best['config']} with {best['average']:.1f}% average compression")
        
        # Copiar para default
        src = Path("data/tpd") / best['config'] / "token_dict.json"
        dst = Path("data/tpd/default/token_dict.json")
        if src.exists() and src != dst:
            import shutil
            shutil.copy2(src, dst)
            print(f"✅ Updated default TPD to {best['config']}")
        elif src == dst:
            print(f"✅ Default TPD already optimal ({best['config']})")

if __name__ == "__main__":
    main()