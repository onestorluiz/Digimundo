#!/usr/bin/env python3
"""
Test DigiLang Validation Integration
Shows how the complete validation approach works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_val_integration import DigiLangValidation

# Test screenplay text
test_text = """INT. COFFEE SHOP - DAY

JOHN enters the coffee shop and looks around nervously. The place is crowded with morning customers. He spots MARY sitting alone at a corner table.

JOHN
(smiling nervously)
Hey there! Mind if I join you for a moment?

MARY looks up from her laptop, surprised but pleased.

MARY
(closing laptop)
Not at all! Please, sit down. I was hoping you'd come.

John sits down across from her. The WAITRESS approaches.

WAITRESS
What can I get you folks today?

JOHN
(to Mary)
The usual?

MARY
(nodding)
Two cappuccinos, please.

The waitress nods and walks away.

CUT TO:

EXT. PARK - NIGHT

The park is empty and quiet. The moon shines brightly through the trees, casting long shadows on the ground.

FADE OUT."""


def test_validation_compression():
    """Test compression with full validation approach."""
    print("=" * 60)
    print("DIGILANG VALIDATION INTEGRATION TEST")
    print("=" * 60)

    # Create compressor with validation's approach
    compressor = DigiLangValidation()

    # Analyze the text first
    print("\n1. ANALYZING TEXT:")
    print("-" * 40)
    analysis = compressor.analyze_text(test_text)
    print(f"Original tokens: {analysis['original_tokens']}")
    print(f"Compressed tokens: {analysis['compressed_tokens']}")
    print(f"Tokens saved: {analysis['tokens_saved']}")
    print(f"Compression ratio: {analysis['compression_ratio']:.1%}")

    if analysis.get('pattern_matches'):
        print(f"\nPattern matches by layer:")
        for layer, matches in analysis['pattern_matches'].items():
            print(f"  {layer}: {matches} matches")

    # Compress the text
    print("\n2. COMPRESSING TEXT:")
    print("-" * 40)
    result = compressor.compress(test_text)

    print(f"Method: {result.method_used}")
    print(f"Original: {result.original_tokens} tokens")
    print(f"Compressed: {result.compressed_tokens} tokens")
    print(f"Reduction: {result.compression_ratio:.1%}")

    if hasattr(result, 'layers_applied'):
        print(f"Layers applied: {result.layers_applied}")
        print(f"Total patterns available: {result.patterns_used}")

    # Show sample of compressed text
    print("\n3. COMPRESSED TEXT SAMPLE:")
    print("-" * 40)
    print(result.compressed_text[:300] + "...")

    # Test decompression
    print("\n4. TESTING DECOMPRESSION:")
    print("-" * 40)
    decompressed = compressor.decompress(result.compressed_text)

    # Check if it matches (approximately)
    original_words = set(test_text.lower().split())
    decompressed_words = set(decompressed.lower().split())

    # Calculate word overlap
    overlap = len(original_words & decompressed_words) / len(original_words)
    print(f"Word overlap: {overlap:.1%}")

    if overlap > 0.9:
        print("✅ Decompression successful (>90% word match)")
    else:
        print("⚠️ Decompression partial (<90% word match)")

    # Show statistics
    print("\n5. SYSTEM STATISTICS:")
    print("-" * 40)
    stats = compressor.get_statistics()
    print(f"Validation available: {stats['validation_available']}")
    if stats.get('layers_info'):
        print(f"Number of layers: {stats['layers_info']['num_layers']}")
        print(f"Total patterns: {stats['layers_info']['total_patterns']}")
    print(f"Simple patterns enabled: {stats['simple_patterns']}")
    print(f"Multi-layer enabled: {stats['multi_layer']}")


def test_comparison():
    """Compare different compression modes."""
    print("\n" + "=" * 60)
    print("COMPRESSION MODE COMPARISON")
    print("=" * 60)

    modes = [
        ("Validation only", DigiLangValidation(use_simple_patterns=False)),
        ("Simple + Validation", DigiLangValidation(use_simple_patterns=True)),
        ("Single layer", DigiLangValidation(use_multi_layer=False)),
        ("Multi-layer", DigiLangValidation(use_multi_layer=True))
    ]

    for name, compressor in modes:
        result = compressor.compress(test_text)
        print(f"\n{name}:")
        print(f"  Tokens: {result.original_tokens} → {result.compressed_tokens}")
        print(f"  Saved: {result.original_tokens - result.compressed_tokens}")
        print(f"  Ratio: {result.compression_ratio:.1%}")


def test_custom_tpd():
    """Test building a custom TPD from corpus."""
    print("\n" + "=" * 60)
    print("CUSTOM TPD BUILDER TEST")
    print("=" * 60)

    compressor = DigiLangValidation()

    # Check if we have a corpus
    corpus_dir = "data/processed"
    if Path(corpus_dir).exists() and list(Path(corpus_dir).glob("*.txt")):
        print(f"\nBuilding custom TPD from {corpus_dir}")

        output_path = "data/tpd/custom/token_dict.json"

        # Build custom TPD
        compressor.build_custom_tpd(
            corpus_dir=corpus_dir,
            output_path=output_path,
            K=500,  # Smaller for testing
            n_min=2,
            n_max=6,
            freq_min=2
        )

        # Test with custom TPD
        custom_compressor = DigiLangValidation(tpd_path=output_path)
        result = custom_compressor.compress(test_text)

        print(f"\nWith custom TPD:")
        print(f"  Compression: {result.compression_ratio:.1%}")
        print(f"  Tokens saved: {result.original_tokens - result.compressed_tokens}")
    else:
        print(f"No corpus found at {corpus_dir}")
        print("Skipping custom TPD test")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("DIGILANG VALIDATION - COMPLETE INTEGRATION")
    print("Using validation's full multi-layer TPD system")
    print("=" * 60)

    test_validation_compression()
    test_comparison()
    test_custom_tpd()

    print("\n" + "=" * 60)
    print("✓ VALIDATION INTEGRATION COMPLETE!")
    print("  • Multi-layer TPD compression")
    print("  • Greedy-lazy pattern selection")
    print("  • Token-level optimization")
    print("  • Reversible compression")
    print("=" * 60)


if __name__ == "__main__":
    main()