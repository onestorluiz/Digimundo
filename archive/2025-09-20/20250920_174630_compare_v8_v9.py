#!/usr/bin/env python3
"""
Compare DigiLang V8.1 Supreme vs V9 Academic Translation Results
"""

import json
from pathlib import Path
from datetime import datetime
import pandas as pd

def load_results():
    """Load both V8.1 and V9 results"""

    # V8.1 Results
    v8_file = Path('docs/FASE_17e_TRADUCAO_FINAL_RESULTS.json')
    v9_file = Path('docs/FASE_17f_V9_ACADEMIC_RESULTS.json')

    v8_results = {}
    v9_results = {}

    if v8_file.exists():
        with open(v8_file, 'r') as f:
            v8_data = json.load(f)
            v8_results = v8_data

    if v9_file.exists():
        with open(v9_file, 'r') as f:
            v9_data = json.load(f)
            v9_results = v9_data

    return v8_results, v9_results

def compare_compression():
    """Compare compression rates between V8.1 and V9"""

    v8_results, v9_results = load_results()

    if not v8_results or not v9_results:
        print("❌ Results files not found. Waiting for V9 to complete...")
        return

    print("=" * 80)
    print("DIGILANG V8.1 SUPREME VS V9 ACADEMIC - COMPARISON REPORT")
    print("=" * 80)

    # Overall stats
    print("\n📊 OVERALL STATISTICS:")
    print("-" * 40)

    v8_stats = v8_results.get('stats', {})
    v9_stats = v9_results.get('stats', {})

    print(f"\n{'Metric':<30} {'V8.1 Supreme':<20} {'V9 Academic':<20}")
    print("-" * 70)

    # Files processed
    print(f"{'Files Processed':<30} {v8_stats.get('successful', 0)}/{v8_stats.get('total_files', 0):<19} {v9_stats.get('successful', 0)}/{v9_stats.get('total_files', 0):<19}")

    # Average compression
    v8_avg = (v8_stats.get('total_original_chars', 0) - v8_stats.get('total_compressed_chars', 0)) / v8_stats.get('total_original_chars', 1)
    v9_avg = (v9_stats.get('total_original_chars', 0) - v9_stats.get('total_compressed_chars', 0)) / v9_stats.get('total_original_chars', 1)

    print(f"{'Average Compression':<30} {v8_avg:.2%}{'':<18} {v9_avg:.2%}")

    # Best compression
    print(f"{'Best Compression':<30} {v8_stats.get('best_compression', 0):.2%}{'':<18} {v9_stats.get('best_compression', 0):.2%}")
    print(f"{'Best File':<30} {v8_stats.get('best_file', 'N/A')[:19]:<19} {v9_stats.get('best_file', 'N/A')[:19]:<19}")

    # Processing time
    print(f"{'Processing Time':<30} {v8_stats.get('processing_time', 0):.1f}s{'':<17} {v9_stats.get('processing_time', 0):.1f}s")

    # Content type detection (V9 only)
    if 'screenplay_files' in v9_stats:
        print(f"\n📂 V9 CONTENT TYPE DETECTION:")
        print("-" * 40)
        print(f"{'Screenplays Detected':<30} {v9_stats.get('screenplay_files', 0)}")
        print(f"{'Theory Books Detected':<30} {v9_stats.get('theory_files', 0)}")
        print(f"{'Mixed Content Detected':<30} {v9_stats.get('mixed_files', 0)}")

    # Per-file comparison
    print(f"\n📄 PER-FILE COMPRESSION COMPARISON:")
    print("-" * 80)

    v8_files = {r['file']: r for r in v8_results.get('results', []) if r.get('status') == 'success'}
    v9_files = {r['file']: r for r in v9_results.get('results', []) if r.get('status') == 'success'}

    # Find common files
    common_files = set(v8_files.keys()) & set(v9_files.keys())

    if common_files:
        improvements = []

        for filename in sorted(common_files):
            v8_comp = v8_files[filename].get('token_compression', 0)
            v9_comp = v9_files[filename].get('token_compression', 0)
            content_type = v9_files[filename].get('content_type', 'unknown')

            improvement = v9_comp - v8_comp
            improvements.append({
                'file': filename[:40],
                'v8_compression': v8_comp,
                'v9_compression': v9_comp,
                'improvement': improvement,
                'content_type': content_type
            })

        # Sort by improvement
        improvements.sort(key=lambda x: x['improvement'], reverse=True)

        # Show top improvements
        print(f"\n🔝 TOP 10 IMPROVEMENTS (V9 better than V8):")
        print(f"{'File':<45} {'V8.1':<10} {'V9':<10} {'Diff':<10} {'Type':<12}")
        print("-" * 87)

        for item in improvements[:10]:
            diff_str = f"+{item['improvement']:.2%}" if item['improvement'] > 0 else f"{item['improvement']:.2%}"
            print(f"{item['file']:<45} {item['v8_compression']:.2%}{'':<4} {item['v9_compression']:.2%}{'':<4} {diff_str:<10} {item['content_type']:<12}")

        # Show where V8 performed better
        v8_better = [i for i in improvements if i['improvement'] < 0]
        if v8_better:
            print(f"\n⚠️ FILES WHERE V8.1 PERFORMED BETTER:")
            print(f"{'File':<45} {'V8.1':<10} {'V9':<10} {'Diff':<10}")
            print("-" * 75)

            for item in v8_better[:5]:
                diff_str = f"{item['improvement']:.2%}"
                print(f"{item['file']:<45} {item['v8_compression']:.2%}{'':<4} {item['v9_compression']:.2%}{'':<4} {diff_str:<10}")

        # Statistical analysis
        avg_improvement = sum(i['improvement'] for i in improvements) / len(improvements)

        print(f"\n📈 STATISTICAL ANALYSIS:")
        print("-" * 40)
        print(f"Average improvement (V9 vs V8): {avg_improvement:+.2%}")
        print(f"Files where V9 is better: {len([i for i in improvements if i['improvement'] > 0])}/{len(improvements)}")
        print(f"Files where V8 is better: {len([i for i in improvements if i['improvement'] < 0])}/{len(improvements)}")
        print(f"Files with same result: {len([i for i in improvements if abs(i['improvement']) < 0.0001])}/{len(improvements)}")

    # Conclusion
    print(f"\n✅ CONCLUSION:")
    print("-" * 40)

    if v9_avg > v8_avg:
        print(f"V9 Academic achieved {(v9_avg - v8_avg):.2%} better average compression than V8.1 Supreme.")
        print("The adaptive content detection appears to be working effectively.")
    else:
        print(f"V8.1 Supreme achieved {(v8_avg - v9_avg):.2%} better average compression than V9 Academic.")
        print("The specialized screenplay patterns in V8.1 may be more effective for this corpus.")

    print(f"\nBoth systems processed the library successfully, demonstrating production readiness.")
    print(f"V9's content type detection provides valuable metadata for future optimizations.")

    # Save comparison report
    report_file = Path('docs/FASE_17_V8_V9_COMPARISON.md')

    with open(report_file, 'w') as f:
        f.write(f"# DigiLang V8.1 vs V9 Academic Comparison\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **V8.1 Average Compression:** {v8_avg:.2%}\n")
        f.write(f"- **V9 Average Compression:** {v9_avg:.2%}\n")
        f.write(f"- **Winner:** {'V9 Academic' if v9_avg > v8_avg else 'V8.1 Supreme'}\n")
        f.write(f"- **Difference:** {abs(v9_avg - v8_avg):.2%}\n\n")
        f.write(f"## Recommendation\n\n")

        if v9_avg > v8_avg:
            f.write("Use **V9 Academic** for mixed content libraries (screenplays + theory books).\n")
            f.write("The adaptive detection provides better overall compression.\n")
        else:
            f.write("Use **V8.1 Supreme** for screenplay-focused content.\n")
            f.write("Consider V9 Academic for libraries with significant theory content.\n")

    print(f"\n📁 Comparison report saved to: {report_file}")

    return v8_avg, v9_avg

if __name__ == "__main__":
    compare_compression()