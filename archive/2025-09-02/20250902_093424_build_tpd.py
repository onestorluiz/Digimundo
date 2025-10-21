#!/usr/bin/env python
"""
Build Token Phrase Dictionary from corpus.
Mines token n-grams and creates optimal mappings to single-token glyphs.
"""

import sys
sys.path.append('.')

from src.digilang.tpd_builder import (
    build_tpd_from_corpus, 
    save_token_dict
)
from pathlib import Path
import json
import time
from datetime import datetime

# Hyperparameters
K = 1800  # Number of n-gram patterns to select (optimized for 25% target)
N_MIN = 2  # Minimum n-gram length
N_MAX = 6  # Maximum n-gram length (reduced for more frequent patterns)
FREQ_MIN = 2  # Minimum frequency threshold (lowered to catch more patterns)
OVERLAP_GUARD = 0.6  # Maximum overlap fraction allowed

def main():
    print("=" * 60)
    print("🔨 BUILDING TOKEN PHRASE DICTIONARY")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  K={K} patterns")
    print(f"  N-gram range: {N_MIN}-{N_MAX}")
    print(f"  Min frequency: {FREQ_MIN}")
    print(f"  Overlap guard: {OVERLAP_GUARD}")
    print()
    
    start_time = time.time()
    
    # Build TPD
    tpd_map = build_tpd_from_corpus(
        corpus_dir="data/original",
        K=K,
        n_min=N_MIN,
        n_max=N_MAX,
        freq_min=FREQ_MIN,
        overlap_guard=OVERLAP_GUARD
    )
    
    # Prepare metadata
    meta = {
        "tokenizer": "cl100k_base",
        "K": K,
        "n_range": [N_MIN, N_MAX],
        "freq_min": FREQ_MIN,
        "overlap_guard": OVERLAP_GUARD,
        "built_at": datetime.utcnow().isoformat() + "Z",
        "entries": len(tpd_map)
    }
    
    # Save token dictionary
    data = {
        "meta": meta,
        "map": tpd_map
    }
    
    save_token_dict(data, "src/digilang/token_dict.json")
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 60)
    print(f"✅ TOKEN DICTIONARY BUILT SUCCESSFULLY")
    print(f"  Entries: {len(tpd_map)}")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Saved to: src/digilang/token_dict.json")
    
    # Sample some entries for inspection
    if tpd_map:
        print("\n📝 Sample entries (first 5):")
        for i, (glyph, ids) in enumerate(list(tpd_map.items())[:5]):
            print(f"  {glyph} → {ids[:8]}{'...' if len(ids) > 8 else ''}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())