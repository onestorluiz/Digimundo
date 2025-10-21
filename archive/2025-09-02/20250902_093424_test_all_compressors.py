#!/usr/bin/env python
"""
Test all compression methods and generate comprehensive report.
"""

import sys
sys.path.append('.')

import time
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import tiktoken

# Import all compressors
from src.compressors.pctoolkit import PCToolkit, CompressionPipeline, CompressionMethod

def test_all_methods():
    """Test all compression methods on Shakespeare texts."""
    print("🔬 TESTING ALL COMPRESSION METHODS")
    print("=" * 60)
    
    # Load test data
    test_files = list(Path("data/original").glob("*.txt"))[:3]
    if not test_files:
        print("❌ No test data found")
        return
    
    toolkit = PCToolkit()
    encoder = tiktoken.get_encoding("cl100k_base")
    results = []
    
    for filepath in test_files:
        print(f"\n📄 Testing: {filepath.name}")
        text = filepath.read_text()[:10000]  # Use first 10KB
        
        # Test each method
        for method in CompressionMethod:
            if method == CompressionMethod.AUTO:
                continue
                
            print(f"  {method.value}...", end=" ")
            
            try:
                result = toolkit.compress(text, method=method)
                
                results.append({
                    'file': filepath.name,
                    'method': method.value,
                    'original_tokens': result.original_tokens,
                    'compressed_tokens': result.compressed_tokens,
                    'compression_ratio': result.compression_ratio,
                    'context_multiplier': result.context_multiplier,
                    'latency_ms': result.latency_ms,
                    'semantic_score': result.semantic_score,
                    'tokens_saved': result.tokens_saved
                })
                
                print(f"✅ {result.compression_ratio:.1%} in {result.latency_ms:.1f}ms")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save results
    Path("results/advanced").mkdir(parents=True, exist_ok=True)
    df.to_csv("results/advanced/all_methods.csv", index=False)
    
    # Generate report
    generate_report(df)
    
    return df

def generate_report(df):
    """Generate comprehensive comparison report."""
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE COMPARISON REPORT\n")
    
    # Summary by method
    summary = df.groupby('method').agg({
        'compression_ratio': 'mean',
        'context_multiplier': 'mean',
        'latency_ms': 'mean',
        'semantic_score': 'mean',
        'tokens_saved': 'mean'
    }).round(3)
    
    print("Average Performance by Method:")
    print(summary.to_string())
    
    # Best methods for different criteria
    print("\n🏆 BEST METHODS:")
    print(f"  Highest Compression: {df.loc[df['compression_ratio'].idxmax(), 'method']} ({df['compression_ratio'].max():.1%})")
    print(f"  Fastest: {df.loc[df['latency_ms'].idxmin(), 'method']} ({df['latency_ms'].min():.1f}ms)")
    print(f"  Best Semantic: {df.loc[df['semantic_score'].idxmax(), 'method']} ({df['semantic_score'].max():.1%})")
    print(f"  Most Tokens Saved: {df.loc[df['tokens_saved'].idxmax(), 'method']} ({df['tokens_saved'].max()} tokens)")
    
    # Create visualizations
    create_advanced_plots(df)

def create_advanced_plots(df):
    """Create advanced comparison visualizations."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Plot 1: Compression ratios
    ax1 = axes[0, 0]
    methods = df.groupby('method')['compression_ratio'].mean().sort_values()
    ax1.barh(methods.index, methods.values, color='steelblue')
    ax1.set_xlabel('Compression Ratio')
    ax1.set_title('Average Compression by Method')
    ax1.set_xlim(0, 1)
    
    # Plot 2: Context multiplier
    ax2 = axes[0, 1]
    multipliers = df.groupby('method')['context_multiplier'].mean().sort_values()
    ax2.barh(multipliers.index, multipliers.values, color='green')
    ax2.set_xlabel('Context Multiplier')
    ax2.set_title('Context Window Expansion')
    
    # Plot 3: Speed comparison
    ax3 = axes[0, 2]
    speed = df.groupby('method')['latency_ms'].mean().sort_values()
    ax3.barh(speed.index, speed.values, color='orange')
    ax3.set_xlabel('Latency (ms)')
    ax3.set_title('Compression Speed')
    ax3.set_xscale('log')
    
    # Plot 4: Semantic preservation
    ax4 = axes[1, 0]
    semantic = df.groupby('method')['semantic_score'].mean().sort_values()
    ax4.barh(semantic.index, semantic.values, color='purple')
    ax4.set_xlabel('Semantic Score')
    ax4.set_title('Semantic Preservation')
    ax4.set_xlim(0, 1)
    
    # Plot 5: Efficiency frontier
    ax5 = axes[1, 1]
    for method in df['method'].unique():
        method_data = df[df['method'] == method]
        ax5.scatter(method_data['compression_ratio'], 
                   method_data['semantic_score'],
                   label=method, s=100, alpha=0.7)
    ax5.set_xlabel('Compression Ratio')
    ax5.set_ylabel('Semantic Score')
    ax5.set_title('Compression vs Quality Trade-off')
    ax5.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Speed vs Compression
    ax6 = axes[1, 2]
    for method in df['method'].unique():
        method_data = df[df['method'] == method]
        avg_compression = method_data['compression_ratio'].mean()
        avg_speed = method_data['latency_ms'].mean()
        ax6.scatter(avg_speed, avg_compression, label=method, s=200, alpha=0.7)
        ax6.annotate(method[:4], (avg_speed, avg_compression), fontsize=8)
    ax6.set_xlabel('Latency (ms)')
    ax6.set_ylabel('Compression Ratio')
    ax6.set_title('Speed vs Compression')
    ax6.set_xscale('log')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("reports/figures/advanced_comparison.png", dpi=150, bbox_inches='tight')
    print(f"\n📊 Advanced plots saved to reports/figures/advanced_comparison.png")

def test_cascade_compression():
    """Test cascade compression pipeline."""
    print("\n" + "=" * 60)
    print("🔄 TESTING CASCADE COMPRESSION\n")
    
    # Load a test file
    test_file = list(Path("data/original").glob("*.txt"))[0]
    text = test_file.read_text()[:20000]
    
    pipeline = CompressionPipeline()
    
    # Test different cascade configurations
    cascades = [
        ("Entity → LLMLingua", [CompressionMethod.ENTITY, CompressionMethod.LLMLINGUA]),
        ("Entity → TCRA", [CompressionMethod.ENTITY, CompressionMethod.TCRA]),
        ("TCRA → Hierarchical", [CompressionMethod.TCRA, CompressionMethod.HIERARCHICAL]),
        ("Entity → TCRA → LLMLingua", [CompressionMethod.ENTITY, CompressionMethod.TCRA, CompressionMethod.LLMLINGUA])
    ]
    
    results = []
    for name, stages in cascades:
        print(f"Testing: {name}")
        compressed, stats = pipeline.cascade_compress(text, stages, target_ratio=0.1)
        
        print(f"  Total compression: {stats['total_compression']:.1%}")
        print(f"  Total latency: {stats['total_latency']:.1f}ms")
        print(f"  Stages: {len(stats['stages'])}")
        
        results.append({
            'cascade': name,
            'compression': stats['total_compression'],
            'latency': stats['total_latency'],
            'stages': len(stats['stages']),
            'final_tokens': stats['final_tokens']
        })
    
    # Save cascade results
    cascade_df = pd.DataFrame(results)
    cascade_df.to_csv("results/advanced/cascade_results.csv", index=False)
    
    print("\n🏆 Best Cascade:")
    best = cascade_df.loc[cascade_df['compression'].idxmax()]
    print(f"  {best['cascade']}: {best['compression']:.1%} compression")

def test_adaptive_compression():
    """Test adaptive compression based on text type."""
    print("\n" + "=" * 60)
    print("🤖 TESTING ADAPTIVE COMPRESSION\n")
    
    toolkit = PCToolkit()
    
    # Different text types
    texts = {
        "narrative": """
        INT. CASTLE - NIGHT
        HAMLET confronts his mother GERTRUDE about her marriage.
        
        HAMLET
        Mother, you have my father much offended.
        """,
        
        "structured": '{"name": "Hamlet", "act": 3, "scene": 4, "location": "Castle"}',
        
        "mixed": """
        The play contains 5 acts:
        - Act 1: Ghost appears (3 scenes)
        - Act 2: Play within play (2 scenes)
        - Act 3: To be or not to be (4 scenes)
        """,
        
        "dialogue": """
        ROMEO: But soft, what light through yonder window breaks?
        JULIET: Romeo, Romeo, wherefore art thou Romeo?
        ROMEO: I take thee at thy word.
        """
    }
    
    for text_type, text in texts.items():
        result = toolkit.compress(text, method=CompressionMethod.AUTO)
        print(f"{text_type.upper()}:")
        print(f"  Auto-selected: {result.method.value}")
        print(f"  Compression: {result.compression_ratio:.1%}")
        print(f"  Latency: {result.latency_ms:.1f}ms")
        print()

if __name__ == "__main__":
    # Run all tests
    df = test_all_methods()
    test_cascade_compression()
    test_adaptive_compression()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("\nGenerated files:")
    print("  • results/advanced/all_methods.csv")
    print("  • results/advanced/cascade_results.csv")
    print("  • reports/figures/advanced_comparison.png")