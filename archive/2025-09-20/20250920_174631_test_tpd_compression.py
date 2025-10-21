#!/usr/bin/env python3
"""
Test TPD compression improvement
Compare compression with and without Token Pattern Dictionary
"""

import json
import tiktoken
from pathlib import Path

# Test text (screenplay sample)
test_text = """INT. COFFEE SHOP - DAY

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

FADE OUT.
"""

def test_without_tpd():
    """Test compression without TPD (current state)."""
    # Simple replacements
    simple_replacements = {
        "INT.": "⟦I⟧",
        "EXT.": "⟦E⟧",
        "DAY": "⟦D⟧",
        "NIGHT": "⟦N⟧",
        "CUT TO:": "⟦CT⟧",
        "FADE OUT": "⟦FO⟧",
    }

    compressed = test_text
    for pattern, replacement in simple_replacements.items():
        compressed = compressed.replace(pattern, replacement)

    # Count tokens
    enc = tiktoken.get_encoding("cl100k_base")
    original_tokens = len(enc.encode(test_text))
    compressed_tokens = len(enc.encode(compressed))

    print("WITHOUT TPD:")
    print(f"  Original: {original_tokens} tokens")
    print(f"  Compressed: {compressed_tokens} tokens")
    print(f"  Reduction: {original_tokens - compressed_tokens} tokens")
    print(f"  Ratio: {(1 - compressed_tokens/original_tokens)*100:.1f}%")

    return original_tokens, compressed_tokens

def test_with_tpd():
    """Test compression with TPD from validation."""
    # Load TPD
    tpd_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/data/tpd/greedy_lazy/token_dict.json")
    with open(tpd_path) as f:
        tpd_data = json.load(f)

    # Extract the actual token mappings
    token_map = tpd_data.get("map", {})

    # Tokenize the text
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(test_text)
    original_tokens = len(tokens)

    # Apply TPD compression
    compressed_tokens = []
    i = 0
    replacements_made = 0

    while i < len(tokens):
        matched = False

        # Try to match patterns of different lengths (8 down to 2)
        for length in range(8, 1, -1):
            if i + length > len(tokens):
                continue

            # Check if this token sequence exists in TPD
            for symbol, token_pattern in token_map.items():
                if len(token_pattern) == length and tokens[i:i+length] == token_pattern:
                    # Replace with single-character symbol
                    symbol_token = enc.encode(symbol)
                    compressed_tokens.extend(symbol_token)
                    i += length
                    matched = True
                    replacements_made += 1
                    break

            if matched:
                break

        if not matched:
            compressed_tokens.append(tokens[i])
            i += 1

    compressed_token_count = len(compressed_tokens)

    print("\nWITH TPD:")
    print(f"  Original: {original_tokens} tokens")
    print(f"  Compressed: {compressed_token_count} tokens")
    print(f"  Reduction: {original_tokens - compressed_token_count} tokens")
    print(f"  Ratio: {(1 - compressed_token_count/original_tokens)*100:.1f}%")
    print(f"  Replacements made: {replacements_made}")

    return original_tokens, compressed_token_count

def main():
    print("=" * 60)
    print("TPD COMPRESSION COMPARISON TEST")
    print("=" * 60)
    print(f"\nTest text length: {len(test_text)} characters")
    print("=" * 60)

    # Test without TPD
    orig1, comp1 = test_without_tpd()

    # Test with TPD
    orig2, comp2 = test_with_tpd()

    # Compare
    print("\n" + "=" * 60)
    print("COMPARISON:")
    improvement = (comp1 - comp2) / orig1 * 100
    print(f"TPD improvement: {improvement:.1f}% additional compression")
    print(f"Total with TPD: {(1 - comp2/orig1)*100:.1f}% compression")
    print("=" * 60)

    if improvement > 0:
        print("\n✅ TPD MELHORA SIGNIFICATIVAMENTE A COMPRESSÃO!")
    else:
        print("\n❌ TPD não melhorou (pode precisar de ajustes)")

if __name__ == "__main__":
    main()