#!/usr/bin/env python
"""
Compare different compression methods for narrative text.
Tests DigiLang vs LLMLingua vs other approaches.
"""

import sys
sys.path.append('.')

import time
import json
import tiktoken
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
import matplotlib.pyplot as plt

from src.digilang.encoder import DigiLangEncoder
from src.compressors.llmlingua import LLMLinguaCompressor, HierarchicalCompressor, CompressionConfig
from src.compressors.naive_tiktoken import NaiveTiktokenCompressor

def benchmark_compressor(name: str, compressor, text: str) -> Dict:
    """Benchmark a single compressor."""
    encoder = tiktoken.get_encoding("cl100k_base")
    original_tokens = len(encoder.encode(text))
    
    # Time the compression
    times = []
    for _ in range(10):
        start = time.perf_counter()
        
        if name == "DigiLang":
            compressed, ratio = compressor.encode(text)
            stats = {}
        elif name.startswith("LLMLingua"):
            compressed, ratio, stats = compressor.compress(text)
        elif name == "Hierarchical":
            compressed, stats = compressor.compress_narrative(text, max_tokens=2000)
            ratio = stats.get('compression_ratio', 0)
        elif name == "Naive":
            compressed, ratio = compressor.compress(text)
            stats = {}
        else:
            compressed = text
            ratio = 0
            stats = {}
            
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    compressed_tokens = len(encoder.encode(compressed))
    
    # Test semantic preservation (simple check)
    key_terms = ['Hamlet', 'Romeo', 'Juliet', 'Macbeth', 'murder', 'love', 'death']
    preserved_terms = sum(1 for term in key_terms if term.lower() in compressed.lower())
    
    return {
        'name': name,
        'original_tokens': original_tokens,
        'compressed_tokens': compressed_tokens,
        'compression_ratio': ratio,
        'actual_ratio': 1 - (compressed_tokens / original_tokens),
        'mean_time': np.mean(times),
        'p95_time': np.percentile(times, 95),
        'semantic_preservation': preserved_terms / len(key_terms),
        'stats': stats
    }

def run_comparison():
    """Run comprehensive comparison of compression methods."""
    print("🔬 COMPRESSION METHOD COMPARISON")
    print("=" * 60)
    
    # Load test texts
    test_files = list(Path("data/original").glob("*.txt"))[:3]
    if not test_files:
        print("❌ No test data found")
        return
    
    # Initialize compressors
    compressors = {
        "DigiLang": DigiLangEncoder(),
        "LLMLingua": LLMLinguaCompressor(CompressionConfig(target_ratio=0.3)),
        "LLMLingua-Aggressive": LLMLinguaCompressor(CompressionConfig(target_ratio=0.1)),
        "Hierarchical": HierarchicalCompressor(),
        "Naive": NaiveTiktokenCompressor()
    }
    
    all_results = []
    
    for filepath in test_files:
        print(f"\n📄 Testing: {filepath.name}")
        text = filepath.read_text()[:20000]  # Use first 20KB
        
        for name, compressor in compressors.items():
            print(f"  Testing {name}...")
            try:
                result = benchmark_compressor(name, compressor, text)
                result['file'] = filepath.name
                all_results.append(result)
                
                print(f"    Compression: {result['actual_ratio']:.1%}")
                print(f"    Time: {result['mean_time']*1000:.1f}ms")
                print(f"    Semantic preservation: {result['semantic_preservation']:.1%}")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                continue
    
    # Create comparison dataframe
    df = pd.DataFrame(all_results)
    
    # Save results
    Path("results/comparison").mkdir(parents=True, exist_ok=True)
    df.to_csv("results/comparison/benchmark.csv", index=False)
    
    # Create visualization
    create_comparison_plots(df)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY BY METHOD\n")
    
    summary = df.groupby('name').agg({
        'actual_ratio': 'mean',
        'mean_time': 'mean',
        'semantic_preservation': 'mean'
    }).round(3)
    
    print(summary.to_string())
    
    # Determine winner
    print("\n🏆 BEST METHODS:")
    print(f"  Highest Compression: {df.loc[df['actual_ratio'].idxmax(), 'name']} ({df['actual_ratio'].max():.1%})")
    print(f"  Fastest: {df.loc[df['mean_time'].idxmin(), 'name']} ({df['mean_time'].min()*1000:.1f}ms)")
    print(f"  Best Semantic Preservation: {df.loc[df['semantic_preservation'].idxmax(), 'name']} ({df['semantic_preservation'].max():.1%})")
    
    # Calculate overall score (weighted)
    df['overall_score'] = (
        df['actual_ratio'] * 0.4 +  # 40% weight on compression
        (1 - df['mean_time'] / df['mean_time'].max()) * 0.2 +  # 20% on speed
        df['semantic_preservation'] * 0.4  # 40% on preservation
    )
    
    best_overall = df.loc[df['overall_score'].idxmax()]
    print(f"\n  Best Overall: {best_overall['name']} (score: {best_overall['overall_score']:.3f})")
    
    return df

def create_comparison_plots(df: pd.DataFrame):
    """Create comparison visualizations."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Compression ratios by method
    ax1 = axes[0, 0]
    methods = df.groupby('name')['actual_ratio'].mean().sort_values()
    ax1.barh(methods.index, methods.values)
    ax1.set_xlabel('Compression Ratio')
    ax1.set_title('Average Compression by Method')
    ax1.set_xlim(0, 1)
    for i, v in enumerate(methods.values):
        ax1.text(v + 0.01, i, f'{v:.1%}', va='center')
    
    # Plot 2: Speed comparison
    ax2 = axes[0, 1]
    speed = df.groupby('name')['mean_time'].mean().sort_values() * 1000
    ax2.barh(speed.index, speed.values, color='orange')
    ax2.set_xlabel('Mean Time (ms)')
    ax2.set_title('Compression Speed by Method')
    for i, v in enumerate(speed.values):
        ax2.text(v + 1, i, f'{v:.1f}ms', va='center')
    
    # Plot 3: Semantic preservation
    ax3 = axes[1, 0]
    preservation = df.groupby('name')['semantic_preservation'].mean().sort_values()
    ax3.barh(preservation.index, preservation.values, color='green')
    ax3.set_xlabel('Semantic Preservation Score')
    ax3.set_title('Content Preservation by Method')
    ax3.set_xlim(0, 1)
    for i, v in enumerate(preservation.values):
        ax3.text(v + 0.01, i, f'{v:.1%}', va='center')
    
    # Plot 4: Efficiency frontier (compression vs preservation)
    ax4 = axes[1, 1]
    for name in df['name'].unique():
        method_data = df[df['name'] == name]
        ax4.scatter(method_data['actual_ratio'], 
                   method_data['semantic_preservation'],
                   label=name, s=100, alpha=0.7)
    ax4.set_xlabel('Compression Ratio')
    ax4.set_ylabel('Semantic Preservation')
    ax4.set_title('Compression vs Preservation Trade-off')
    ax4.legend(loc='best', fontsize='small')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("reports/figures/compression_comparison.png", dpi=150)
    print(f"📊 Plots saved to reports/figures/compression_comparison.png")
    
def analyze_use_cases(df: pd.DataFrame):
    """Recommend best compressor for different use cases."""
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDED METHODS BY USE CASE\n")
    
    use_cases = {
        "Maximum Compression (cost-sensitive)": 
            df.loc[df['actual_ratio'].idxmax(), 'name'],
        
        "Real-time Processing (speed-critical)": 
            df.loc[df['mean_time'].idxmin(), 'name'],
        
        "Narrative Analysis (preserve meaning)": 
            df.loc[df['semantic_preservation'].idxmax(), 'name'],
        
        "Balanced Performance": 
            df.loc[df['overall_score'].idxmax(), 'name'] if 'overall_score' in df else 'Unknown'
    }
    
    for use_case, method in use_cases.items():
        method_stats = df[df['name'] == method].iloc[0]
        print(f"  {use_case}:")
        print(f"    → {method}")
        print(f"      Compression: {method_stats['actual_ratio']:.1%}")
        print(f"      Speed: {method_stats['mean_time']*1000:.1f}ms")
        print(f"      Preservation: {method_stats['semantic_preservation']:.1%}")
        print()

if __name__ == "__main__":
    df = run_comparison()
    if df is not None and not df.empty:
        analyze_use_cases(df)