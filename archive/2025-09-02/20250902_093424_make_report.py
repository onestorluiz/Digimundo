#!/usr/bin/env python
import sys
sys.path.append('.')

from pathlib import Path
import pandas as pd
import json

def generate_report():
    """Generate comprehensive validation report"""
    print("📝 GENERATING FINAL REPORT")
    print("=" * 50)
    
    report = []
    report.append("# 📊 SCRIPTUREMON VALIDATION REPORT\n\n")
    report.append("## Executive Summary\n\n")
    
    scorecard = {}
    
    # Process all benchmark results
    result_files = {
        'compression': 'results/compression/benchmark.csv',
        'llmlingua': 'results/compression/llmlingua.csv',
        'two_stage': 'results/compression/two_stage.csv',
        'rag': 'results/rag/benchmark.csv', 
        'telepathy': 'results/telepathy/benchmark.csv',
        'memory': 'results/memory/benchmark.csv'
    }
    
    for category, file_path in result_files.items():
        if Path(file_path).exists():
            df = pd.read_csv(file_path)
            
            if category == 'compression':
                compression = df['digilang_ratio'].mean() if 'digilang_ratio' in df else 0
                window = df['window_multiplier'].mean() if 'window_multiplier' in df else 0
                speed = df['speed_ratio'].mean() if 'speed_ratio' in df else 0
                
                scorecard['C1'] = "PASS" if compression >= 0.35 else "FAIL"
                scorecard['C2'] = "PASS" if window >= 1.5 else "FAIL"  
                scorecard['C3'] = "PASS" if speed >= 1.5 else "FAIL"
                
                report.append(f"**C1 Compression**: {compression:.1%} - {scorecard['C1']}\n")
                report.append(f"**C2 Context Window**: {window:.2f}x - {scorecard['C2']}\n")
                report.append(f"**C3 Processing Speed**: {speed:.2f}x - {scorecard['C3']}\n")
            
            elif category == 'llmlingua':
                llm_compression = df['reduction'].mean() if 'reduction' in df else 0
                report.append(f"\n**LLMLingua Baseline**: {llm_compression:.1%} compression\n")
            
            elif category == 'two_stage':
                two_stage_compression = df['reduction'].mean() if 'reduction' in df else 0
                report.append(f"**Two-Stage Pipeline**: {two_stage_compression:.1%} compression\n")
            
            elif category == 'rag':
                if 'precision_at_5' in df.columns:
                    hybrid = df[df['method'] == 'hybrid_narrative']['precision_at_5'].iloc[0]
                    baseline = df[df['method'] == 'vector_only']['precision_at_5'].iloc[0]
                    improvement = hybrid - baseline
                    scorecard['C4'] = "PASS" if improvement >= 0.10 else "FAIL"
                    report.append(f"**C4 RAG Hybrid**: +{improvement:.1%} - {scorecard['C4']}\n")
            
            elif category == 'telepathy':
                saving = df['best_saving'].iloc[0] if 'best_saving' in df else 0
                scorecard['C5'] = "PASS" if saving >= 0.30 else "FAIL"
                report.append(f"**C5 Telepathy**: {saving:.1%} saving - {scorecard['C5']}\n")
            
            elif category == 'memory':
                retention = df['avg_retention'].iloc[0] if 'avg_retention' in df else 0
                scorecard['C6'] = "PASS" if retention >= 0.85 else "FAIL"
                report.append(f"**C6 Memory**: {retention:.1%} retention - {scorecard['C6']}\n")
    
    # Add figures
    report.append("\n## 📊 Figures\n\n")
    figure_dir = Path("reports/figures")
    if figure_dir.exists():
        for fig in figure_dir.glob("*.png"):
            report.append(f"![{fig.stem}]({fig.relative_to(Path('reports'))})\n\n")
    
    # Final scorecard
    report.append("## 🎯 FINAL SCORECARD\n\n")
    report.append("| Claim | Status |\n")
    report.append("|-------|--------|\n")
    
    for claim, status in scorecard.items():
        emoji = "✅" if status == "PASS" else "❌"
        report.append(f"| {claim} | {emoji} {status} |\n")
    
    # Write report
    report_path = Path("reports/report.md")
    report_path.parent.mkdir(exist_ok=True)
    report_path.write_text("".join(report))
    
    # Print final scorecard
    print("\n🎯 FINAL SCORECARD:")
    print("="*30)
    passed = failed = 0
    for claim, status in scorecard.items():
        emoji = "✅" if status == "PASS" else "❌"
        print(f"{emoji} {claim}: {status}")
        if status == "PASS":
            passed += 1
        else:
            failed += 1
    
    print(f"\n📊 SCORE: {passed} PASS, {failed} FAIL")
    print(f"📄 Report: reports/report.md")
    print(f"📊 Figures: reports/figures/")
    print(f"💾 Raw data: results/")

if __name__ == "__main__":
    generate_report()
