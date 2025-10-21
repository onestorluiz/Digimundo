#!/usr/bin/env python3
"""
Test DigiLang Advanced Integration
Tests the imported DigiLang system from validation
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_manager import (
    get_digilang_manager,
    compress_text,
    decompress_text
)
from apps.scripturemon.digilang_advanced import DigiLangEncoder


def test_basic_compression():
    """Test basic compression functionality."""
    print("\n=== Testing Basic Compression ===")

    text = """INT. COFFEE SHOP - DAY

    JOHN enters the coffee shop and looks around. He sees MARY sitting at a table.

    JOHN
    (smiling)
    Hey there! Mind if I join you?

    MARY
    (looking up)
    Not at all. Please, sit down.

    CUT TO:

    EXT. PARK - NIGHT

    The moon shines brightly over the empty park.
    """

    # Test with manager
    manager = get_digilang_manager(mode="auto")
    result = manager.compress(text)

    print(f"Original length: {len(text)} chars")
    print(f"Compressed length: {len(result.compressed_text)} chars")
    print(f"Original tokens: {result.original_tokens}")
    print(f"Compressed tokens: {result.compressed_tokens}")
    print(f"Compression ratio: {result.compression_ratio:.2%}")
    print(f"Method used: {result.method_used}")

    # Test decompression
    decompressed = manager.decompress(result.compressed_text, method=result.method_used)
    print(f"\nDecompression successful: {text in decompressed or decompressed in text}")

    return result.compression_ratio > 0


def test_convenience_functions():
    """Test convenience functions."""
    print("\n=== Testing Convenience Functions ===")

    text = "FADE IN: INT. HOUSE - DAY - The house is empty."

    # Compress
    compressed, ratio = compress_text(text)
    print(f"Original: {text}")
    print(f"Compressed: {compressed}")
    print(f"Ratio: {ratio:.2%}")

    # Decompress
    decompressed = decompress_text(compressed)
    print(f"Decompressed matches: {text in decompressed or decompressed in text}")

    return ratio > 0


def test_mode_comparison():
    """Compare simple vs advanced modes."""
    print("\n=== Testing Mode Comparison ===")

    text = """
    INT. OFFICE - DAY

    The office is busy with people working at their desks.
    SARAH walks in with a stack of papers.

    SARAH
    (to the room)
    Has anyone seen the quarterly reports?

    Several people shake their heads. She sighs and continues walking.

    CUT TO:

    INT. CONFERENCE ROOM - CONTINUOUS

    A meeting is in progress. The CEO stands at the front.
    """

    manager = get_digilang_manager()

    # Test simple mode
    simple_result = manager.compress(text, mode="simple")
    print(f"Simple compression: {simple_result.compression_ratio:.2%}")
    print(f"  Tokens: {simple_result.original_tokens} -> {simple_result.compressed_tokens}")

    # Test advanced mode if available
    if manager.has_advanced:
        advanced_result = manager.compress(text, mode="advanced")
        print(f"Advanced compression: {advanced_result.compression_ratio:.2%}")
        print(f"  Tokens: {advanced_result.original_tokens} -> {advanced_result.compressed_tokens}")

        # Compare
        improvement = advanced_result.compression_ratio - simple_result.compression_ratio
        print(f"\nAdvanced improvement: {improvement:.2%}")
    else:
        print("Advanced mode not available (tiktoken missing)")

    return True


def test_screenplay_patterns():
    """Test screenplay-specific patterns."""
    print("\n=== Testing Screenplay Patterns ===")

    patterns = [
        "FADE IN:",
        "FADE OUT:",
        "CUT TO:",
        "INT. LOCATION - DAY",
        "EXT. LOCATION - NIGHT",
        "(V.O.)",
        "(O.S.)",
        "(CONT'D)",
    ]

    manager = get_digilang_manager()

    for pattern in patterns:
        result = manager.compress(pattern)
        print(f"{pattern:25} -> {result.compressed_text:20} ({result.compression_ratio:.1%})")

    return True


def test_statistics():
    """Test statistics tracking."""
    print("\n=== Testing Statistics ===")

    manager = get_digilang_manager()

    # Process some texts
    texts = [
        "INT. ROOM - DAY",
        "The character enters.",
        "FADE OUT:",
        "CUT TO:",
        "EXT. STREET - NIGHT"
    ]

    for text in texts:
        manager.compress(text)

    stats = manager.get_statistics()
    print(f"Total processed: {stats['total_processed']}")
    print(f"Cache hits: {stats['cache_hits']}")
    print(f"Simple compressions: {stats['simple_count']}")
    print(f"Advanced compressions: {stats['advanced_count']}")
    print(f"Average compression ratio: {stats['average_ratio']:.2%}")
    print(f"Has advanced mode: {stats['has_advanced']}")

    return stats['total_processed'] == len(texts)


def test_context_optimization():
    """Test context window optimization."""
    print("\n=== Testing Context Optimization ===")

    # Create a long text
    text = """INT. MANSION - NIGHT

    A grand ballroom filled with guests in formal attire.
    """ * 100  # Repeat to make it long

    manager = get_digilang_manager()

    # Optimize for small context
    optimized = manager.optimize_for_context(text, max_tokens=100)

    print(f"Original length: {len(text)} chars")
    print(f"Optimized length: {len(optimized)} chars")
    print(f"Estimated tokens: {len(optimized) // 4}")

    return len(optimized) < len(text)


def main():
    """Run all tests."""
    print("=" * 60)
    print("DIGILANG ADVANCED INTEGRATION TESTS")
    print("=" * 60)

    tests = [
        ("Basic Compression", test_basic_compression),
        ("Convenience Functions", test_convenience_functions),
        ("Mode Comparison", test_mode_comparison),
        ("Screenplay Patterns", test_screenplay_patterns),
        ("Statistics", test_statistics),
        ("Context Optimization", test_context_optimization),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                print(f"✓ {name} passed\n")
                passed += 1
            else:
                print(f"✗ {name} failed\n")
                failed += 1
        except Exception as e:
            print(f"✗ {name} failed with error: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)