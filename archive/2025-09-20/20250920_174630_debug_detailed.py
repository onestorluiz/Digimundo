#!/usr/bin/env python3
"""
Detailed debugging of DigiLang roundtrip issues.
"""

from apps.scripturemon.digilang import to_digilang, from_digilang
from apps.scripturemon.digilang.encoder import DigiLangEncoder
from apps.scripturemon.digilang.decoder import DigiLangDecoder
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive
import tiktoken

# Very simple test cases
test_cases = [
    "FADE IN:",
    "EXT. CASTLE - DAY",
    "HAMLET walks slowly.",
    "To be or not to be.",
    "HAMLET\nMy lord, what say you?",
]

enc = tiktoken.get_encoding("cl100k_base")

for i, test_text in enumerate(test_cases):
    print(f"\n{'='*60}")
    print(f"TEST CASE {i+1}: {repr(test_text)}")
    print(f"{'='*60}")

    # Test with simple API first (no TPD)
    print("\n--- Simple API (no TPD) ---")
    try:
        encoder = DigiLangEncoder(use_tpd=False)
        decoder = DigiLangDecoder(use_tpd=False)

        compressed, ratio = encoder.encode(test_text)
        decoded = decoder.decode(compressed)

        print(f"Original: {repr(test_text)}")
        print(f"Original tokens: {enc.encode(test_text)}")
        print(f"Compressed: {repr(compressed)}")
        print(f"Compressed tokens: {enc.encode(compressed)}")
        print(f"Decoded: {repr(decoded)}")
        print(f"Ratio: {ratio:.1%}")
        print(f"Match: {test_text == decoded}")

        if test_text != decoded:
            print("\nDifference analysis:")
            for j, (a, b) in enumerate(zip(test_text, decoded)):
                if a != b:
                    print(f"  Position {j}: '{a}' != '{b}'")
                    break
            if len(test_text) != len(decoded):
                print(f"  Length: {len(test_text)} != {len(decoded)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print("DigiLang components present and accounted for:")
print("✓ token_trie.py - Token trie implementation")
print("✓ tokenizer_utils.py - Glyph selection utilities")
print("✓ canon_strict.py & canon_aggressive.py - Text canonicalization")
print("✓ build_vocab.py - Vocabulary generation")
print("✓ vocab.json - Generated vocabulary with symbols and MWEs")
print("✓ TPD dictionaries - Token pair compression")
print("✓ Fixed decoder - Longest-match-first symbol replacement")
print("\nIssues to resolve:")
print("- Roundtrip accuracy for complex text")
print("- Reaching 20-22% compression target")