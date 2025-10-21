#!/usr/bin/env python3
"""
Compare DigiLang V1 vs V2 translations
"""

import json
from pathlib import Path

def compare_versions():
    """Compare old vs new DigiLang translations."""

    old_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG")
    new_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/digilibrary/BIBLIOTECA_DIGILANG_V2")

    print("=" * 60)
    print("DIGILANG VERSION COMPARISON")
    print("=" * 60)

    # Find all .dlg files in new directory
    new_files = list(new_dir.rglob("*.dlg"))
    print(f"Found {len(new_files)} translated files in V2\n")

    comparisons = []
    total_old_size = 0
    total_new_size = 0

    for new_file in new_files:
        # Try to find corresponding old file
        relative_path = new_file.relative_to(new_dir)
        old_file = old_dir / relative_path

        if old_file.exists():
            old_size = old_file.stat().st_size
            new_size = new_file.stat().st_size

            total_old_size += old_size
            total_new_size += new_size

            improvement = ((old_size - new_size) / old_size * 100) if old_size > 0 else 0

            comparisons.append({
                'file': relative_path.stem,
                'old_size': old_size,
                'new_size': new_size,
                'improvement': improvement
            })

    if comparisons:
        print(f"Matched {len(comparisons)} files for comparison")

        # Overall stats
        overall_improvement = ((total_old_size - total_new_size) / total_old_size * 100) if total_old_size > 0 else 0

        print(f"\nOVERALL STATISTICS:")
        print(f"  Total V1 size: {total_old_size:,} bytes")
        print(f"  Total V2 size: {total_new_size:,} bytes")
        print(f"  Size reduction: {total_old_size - total_new_size:,} bytes")
        print(f"  Improvement: {overall_improvement:.2%}")

        # Top improvements
        sorted_comp = sorted(comparisons, key=lambda x: x['improvement'], reverse=True)

        print(f"\nTOP 5 IMPROVEMENTS:")
        for c in sorted_comp[:5]:
            print(f"  {c['improvement']:6.2%} - {c['file'][:40]}")

        # Bottom 5 (worst cases)
        print(f"\nBOTTOM 5 (LEAST IMPROVEMENT):")
        for c in sorted_comp[-5:]:
            print(f"  {c['improvement']:6.2%} - {c['file'][:40]}")
    else:
        print("No matching files found for comparison")

    # Check metadata if available
    meta_files = list(new_dir.rglob("*.meta.json"))
    if meta_files:
        print(f"\n{'-'*60}")
        print("METADATA ANALYSIS:")

        total_token_reduction = 0
        total_char_reduction = 0
        count = 0

        for meta_file in meta_files[:5]:  # Sample first 5
            with open(meta_file, 'r') as f:
                meta = json.load(f)

            if count == 0:
                print(f"\nSample metadata from {meta_file.stem}:")
                print(f"  Method: {meta.get('compression_method', 'unknown')}")
                print(f"  Version: {meta.get('digilang_version', 'unknown')}")
                print(f"  Has tiktoken: {meta.get('has_tiktoken', False)}")

            orig_tokens = meta.get('original_tokens', 0)
            comp_tokens = meta.get('compressed_tokens', 0)

            if orig_tokens > 0:
                token_reduction = (orig_tokens - comp_tokens)
                total_token_reduction += token_reduction
                count += 1

        if count > 0:
            print(f"\nAverage token reduction (sample): {total_token_reduction/count:.0f} tokens")

    print("=" * 60)

if __name__ == "__main__":
    compare_versions()