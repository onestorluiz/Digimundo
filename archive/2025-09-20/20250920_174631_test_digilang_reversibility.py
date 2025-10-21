#!/usr/bin/env python3
"""
Comprehensive DigiLang Reversibility Test Suite
Tests full round-trip compression/decompression with various text types
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang import encoder, decoder
import tiktoken
from typing import Tuple, List
import json

# Test cases covering different scenarios
TEST_CASES = [
    # 1. Simple screenplay
    ("simple_screenplay", """INT. OFFICE - DAY

JOHN enters the room.

JOHN
Hello, Mary.

MARY
Hi, John."""),

    # 2. Complex screenplay with transitions
    ("complex_screenplay", """INT. COFFEE SHOP - DAY

The bustling coffee shop is filled with morning customers. SARAH (30s, professional) sits alone at a corner table, typing on her laptop.

JAMES (35, casual) enters, spots her, and approaches.

JAMES
(nervous)
Is this seat taken?

SARAH
(looking up, smiling)
Not at all. Please, sit.

James sits. They share an awkward moment.

JAMES
I've been meaning to ask you something...

SARAH
(interested)
Yes?

CUT TO:

EXT. PARK - LATER

They walk together through the park.

FADE OUT."""),

    # 3. Portuguese screenplay
    ("portuguese_screenplay", """INT. CASA - DIA

JOÃO entra na sala e vê MARIA sentada no sofá.

JOÃO
(sussurrando)
Precisamos conversar sobre ontem.

MARIA
(pausa)
Eu sei. Senta aqui.

João caminha lentamente e senta ao lado dela.

CORTA PARA:

EXT. PRAIA - NOITE

A lua brilha sobre as ondas.

FADE OUT."""),

    # 4. Mixed language
    ("mixed_language", """INT. RESTAURANT - NIGHT

CARLOS speaks in Portuguese while JENNIFER responds in English.

CARLOS
Você está linda hoje.

JENNIFER
Thank you. You look great too.

CARLOS
(smiling)
Obrigado. Shall we order?

JENNIFER
Sim, let's do it."""),

    # 5. Technical dialogue
    ("technical_dialogue", """INT. LAB - DAY

DR. SMITH examines the data.

DR. SMITH
The quantum entanglement coefficient is 0.987, which means the particles are maintaining coherence across 1,000 kilometers.

ASSISTANT
That's impossible according to the Copenhagen interpretation!

DR. SMITH
(grinning)
Exactly. We've just proven Einstein wrong about "spooky action at a distance"."""),

    # 6. Special characters and formatting
    ("special_chars", """INT. STUDIO - DAY

The sign reads: "José's Café & Bar"

MARÍA
¿Cómo estás? I haven't seen you in años!

JOSÉ
¡Bien! It's been too long, amiga.

[They embrace]

MARÍA (V.O.)
(thinking)
Some things never change...

FADE TO BLACK."""),
]


class ReversibilityTester:
    """Comprehensive reversibility testing for DigiLang."""

    def __init__(self):
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.encoder = encoder.DigiLangEncoder()
        self.decoder = decoder.DigiLangDecoder()
        self.results = []

    def test_exact_reversibility(self, text: str, name: str) -> dict:
        """Test if text can be perfectly reversed."""
        try:
            # Encode
            encoded, ratio = self.encoder.encode(text)

            # Decode
            decoded = self.decoder.decode(encoded)

            # Calculate metrics
            original_tokens = len(self.enc.encode(text))
            encoded_tokens = len(self.enc.encode(encoded))
            compression = 1 - (encoded_tokens / original_tokens) if original_tokens > 0 else 0

            # Check exact match
            exact_match = (text == decoded)

            # Check word-level similarity
            original_words = set(text.lower().split())
            decoded_words = set(decoded.lower().split())
            word_overlap = len(original_words & decoded_words) / len(original_words) if original_words else 1.0

            # Check character-level similarity
            char_match = sum(1 for a, b in zip(text, decoded) if a == b) / max(len(text), len(decoded))

            return {
                'name': name,
                'exact_match': exact_match,
                'word_overlap': word_overlap,
                'char_match': char_match,
                'compression': compression,
                'original_tokens': original_tokens,
                'encoded_tokens': encoded_tokens,
                'original_length': len(text),
                'encoded_length': len(encoded),
                'decoded_length': len(decoded),
                'success': exact_match or word_overlap > 0.95
            }
        except Exception as e:
            return {
                'name': name,
                'error': str(e),
                'success': False
            }

    def test_incremental_compression(self, text: str, rounds: int = 3) -> List[dict]:
        """Test multiple rounds of compression/decompression."""
        results = []
        current = text

        for round_num in range(rounds):
            try:
                # Compress
                compressed, _ = self.encoder.encode(current)
                tokens_before = len(self.enc.encode(current))
                tokens_after = len(self.enc.encode(compressed))

                # Decompress
                decompressed = self.decoder.decode(compressed)

                # Check if we can continue
                can_continue = (decompressed.strip() != "")

                results.append({
                    'round': round_num + 1,
                    'tokens_before': tokens_before,
                    'tokens_after': tokens_after,
                    'compression': 1 - (tokens_after / tokens_before) if tokens_before > 0 else 0,
                    'text_preserved': current.strip() == decompressed.strip(),
                    'can_continue': can_continue
                })

                if not can_continue:
                    break

                current = compressed  # Try compressing the already compressed text

            except Exception as e:
                results.append({
                    'round': round_num + 1,
                    'error': str(e)
                })
                break

        return results

    def test_edge_cases(self) -> List[dict]:
        """Test edge cases."""
        edge_cases = [
            ("empty", ""),
            ("single_char", "A"),
            ("single_word", "Hello"),
            ("numbers", "123 456 789.01"),
            ("punctuation", "!@#$%^&*()_+-=[]{}|;:,.<>?"),
            ("unicode", "😀 🎬 🎭 🎪"),
            ("whitespace", "   \n\n\t  \r\n  "),
            ("repeated", "test " * 100),
            ("long_word", "a" * 1000),
        ]

        results = []
        for name, text in edge_cases:
            result = self.test_exact_reversibility(text, f"edge_{name}")
            results.append(result)

        return results

    def run_all_tests(self):
        """Run comprehensive test suite."""
        print("=" * 70)
        print("DIGILANG REVERSIBILITY TEST SUITE")
        print("=" * 70)

        # Test main cases
        print("\n1. TESTING MAIN SCENARIOS:")
        print("-" * 50)

        for name, text in TEST_CASES:
            result = self.test_exact_reversibility(text, name)
            self.results.append(result)

            status = "✅" if result.get('success') else "❌"
            compression = result.get('compression', 0) * 100

            print(f"{status} {name:20} | Compression: {compression:6.2f}% | ", end="")

            if result.get('exact_match'):
                print("EXACT MATCH")
            elif result.get('word_overlap'):
                print(f"Word overlap: {result['word_overlap']:.1%}")
            else:
                print(f"ERROR: {result.get('error', 'Unknown')}")

        # Test edge cases
        print("\n2. TESTING EDGE CASES:")
        print("-" * 50)

        edge_results = self.test_edge_cases()
        for result in edge_results:
            status = "✅" if result.get('success') else "❌"
            print(f"{status} {result['name']:20} | ", end="")

            if result.get('error'):
                print(f"ERROR: {result['error']}")
            elif result.get('exact_match'):
                print("EXACT MATCH")
            else:
                print(f"Partial match: {result.get('word_overlap', 0):.1%}")

        # Test incremental compression
        print("\n3. TESTING INCREMENTAL COMPRESSION:")
        print("-" * 50)

        sample_text = TEST_CASES[1][1]  # Complex screenplay
        incremental = self.test_incremental_compression(sample_text, rounds=3)

        for round_result in incremental:
            if 'error' in round_result:
                print(f"Round {round_result['round']}: ERROR - {round_result['error']}")
            else:
                print(f"Round {round_result['round']}: "
                      f"Compression {round_result['compression']:.1%}, "
                      f"Preserved: {round_result['text_preserved']}")

        # Summary statistics
        print("\n4. SUMMARY STATISTICS:")
        print("-" * 50)

        successful = sum(1 for r in self.results if r.get('success'))
        total = len(self.results)
        avg_compression = sum(r.get('compression', 0) for r in self.results) / total if total > 0 else 0
        exact_matches = sum(1 for r in self.results if r.get('exact_match'))

        print(f"Total tests: {total}")
        print(f"Successful: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"Exact matches: {exact_matches}/{total} ({exact_matches/total*100:.1f}%)")
        print(f"Average compression: {avg_compression:.1%}")

        # Performance analysis
        print("\n5. PERFORMANCE BY CATEGORY:")
        print("-" * 50)

        categories = {
            'screenplay': ['simple_screenplay', 'complex_screenplay'],
            'portuguese': ['portuguese_screenplay', 'mixed_language'],
            'technical': ['technical_dialogue', 'special_chars']
        }

        for category, names in categories.items():
            cat_results = [r for r in self.results if r.get('name') in names]
            if cat_results:
                avg_comp = sum(r.get('compression', 0) for r in cat_results) / len(cat_results)
                success_rate = sum(1 for r in cat_results if r.get('success')) / len(cat_results)
                print(f"{category:12} | Compression: {avg_comp:6.1%} | Success: {success_rate:.0%}")

        return {
            'total_tests': total,
            'successful': successful,
            'exact_matches': exact_matches,
            'average_compression': avg_compression,
            'results': self.results
        }


def save_test_results(results: dict):
    """Save test results to file."""
    output_path = Path("tests/digilang_reversibility_results.json")
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Results saved to {output_path}")


def main():
    """Run the complete test suite."""
    tester = ReversibilityTester()
    results = tester.run_all_tests()

    # Save results
    save_test_results(results)

    # Final verdict
    print("\n" + "=" * 70)
    if results['successful'] >= results['total_tests'] * 0.9:
        print("✅ DIGILANG REVERSIBILITY: EXCELLENT (>90% success)")
    elif results['successful'] >= results['total_tests'] * 0.7:
        print("⚠️ DIGILANG REVERSIBILITY: GOOD (>70% success)")
    else:
        print("❌ DIGILANG REVERSIBILITY: NEEDS IMPROVEMENT (<70% success)")

    print(f"   Average compression achieved: {results['average_compression']:.1%}")
    print("=" * 70)

    return results['successful'] >= results['total_tests'] * 0.7


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)