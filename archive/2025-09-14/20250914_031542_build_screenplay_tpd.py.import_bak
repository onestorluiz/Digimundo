#!/usr/bin/env python3
"""
Build optimized TPD for screenplay compression
Uses greedy-lazy algorithm to find best token patterns
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from apps.scripturemon.digilang_val_integration import DigiLangValidation
import json
import tiktoken
from datetime import datetime

def analyze_corpus_patterns():
    """Analyze the corpus to understand token patterns."""
    print("="*60)
    print("ANALYZING SCREENPLAY CORPUS PATTERNS")
    print("="*60)

    corpus_dir = Path("data/original")
    if not corpus_dir.exists():
        print("❌ Corpus directory not found. Run build_corpus.py first!")
        return None

    # Load sample text for analysis
    enc = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0
    sample_texts = []

    for txt_file in list(corpus_dir.glob("*.txt"))[:10]:  # Sample first 10
        try:
            text = txt_file.read_text(encoding='utf-8')
            tokens = enc.encode(text)
            total_tokens += len(tokens)
            sample_texts.append(text[:5000])  # First 5000 chars
            print(f"  • {txt_file.name}: {len(tokens):,} tokens")
        except:
            pass

    print(f"\nTotal sample tokens: {total_tokens:,}")
    return '\n\n'.join(sample_texts)

def build_optimized_tpd():
    """Build TPD optimized for screenplays."""
    print("\n" + "="*60)
    print("BUILDING OPTIMIZED TPD FOR SCREENPLAYS")
    print("="*60)

    # Check if corpus exists
    corpus_dir = Path("data/original")
    if not corpus_dir.exists() or not list(corpus_dir.glob("*.txt")):
        print("⚠️ Corpus not ready. Using sample data...")

        # Create sample screenplay corpus
        sample_corpus = """INT. COFFEE SHOP - DAY

JOHN enters the coffee shop and looks around nervously.

JOHN
(to himself)
Where is she?

He spots MARY at a corner table.

JOHN (CONT'D)
(relieved)
There you are.

CUT TO:

EXT. PARK - LATER

They walk together through the park.

MARY
I've been thinking about what you said.

JOHN
And?

MARY
(beat)
I think you're right.

FADE OUT.""" * 100  # Repeat for larger sample

        # Save sample
        corpus_dir.mkdir(parents=True, exist_ok=True)
        sample_file = corpus_dir / "sample_screenplay.txt"
        sample_file.write_text(sample_corpus)
        print("✓ Created sample corpus")

    # Initialize DigiLang with validation approach
    compressor = DigiLangValidation()

    # Build custom TPD
    output_path = "data/tpd/screenplay/token_dict.json"

    print("\nBuilding TPD with parameters:")
    print("  • K (patterns): 1500")
    print("  • N-gram range: 2-8 tokens")
    print("  • Min frequency: 3")
    print("  • Algorithm: greedy-lazy")
    print("\nThis may take a few minutes...")

    try:
        compressor.build_custom_tpd(
            corpus_dir=str(corpus_dir),
            output_path=output_path,
            K=1500,  # Number of patterns
            n_min=2,  # Min n-gram size
            n_max=8,  # Max n-gram size
            freq_min=3  # Minimum frequency
        )
        print(f"\n✅ TPD saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"\n❌ Error building TPD: {e}")

        # Create fallback TPD with common screenplay patterns
        print("\nCreating fallback TPD with common patterns...")
        create_fallback_tpd()
        return "data/tpd/screenplay/token_dict.json"

def create_fallback_tpd():
    """Create a fallback TPD with common screenplay patterns."""
    enc = tiktoken.get_encoding("cl100k_base")

    # Common screenplay phrases and their single-token replacements
    common_patterns = [
        "INT. ",
        "EXT. ",
        " - DAY",
        " - NIGHT",
        "CUT TO:",
        "FADE OUT.",
        "FADE IN:",
        "(beat)",
        "(pause)",
        "(CONT'D)",
        "looks at",
        "turns to",
        "walks to",
        "He ",
        "She ",
        "They ",
        "What ",
        "Where ",
        "I don't",
        "I can't",
    ]

    # Get single-token characters
    from apps.scripturemon.digilang.tokenizer_utils import get_single_token_strings
    glyphs = get_single_token_strings(max_candidates=len(common_patterns) + 100)

    # Build mapping
    tpd_map = {}
    for i, pattern in enumerate(common_patterns):
        if i < len(glyphs):
            token_ids = enc.encode(pattern)
            if len(token_ids) > 1:  # Only worth it if multiple tokens
                tpd_map[glyphs[i]] = token_ids

    # Save fallback TPD
    output_dir = Path("data/tpd/screenplay")
    output_dir.mkdir(parents=True, exist_ok=True)

    tpd_data = {
        "meta": {
            "tokenizer": "cl100k_base",
            "type": "fallback",
            "patterns": len(tpd_map),
            "created": datetime.now().isoformat()
        },
        "map": tpd_map
    }

    output_path = output_dir / "token_dict.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tpd_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Created fallback TPD with {len(tpd_map)} patterns")

def test_new_tpd():
    """Test compression with the new TPD."""
    print("\n" + "="*60)
    print("TESTING NEW TPD COMPRESSION")
    print("="*60)

    tpd_path = "data/tpd/screenplay/token_dict.json"
    if not Path(tpd_path).exists():
        print("❌ TPD not found!")
        return

    # Test with sample screenplay
    test_text = """INT. OFFICE - DAY

JOHN enters the office and looks around nervously.

JOHN
(to MARY)
We need to talk about the Johnson report.

MARY
(sighs)
I know. It's not looking good.

CUT TO:

INT. CONFERENCE ROOM - LATER

The team is assembled around the table.

FADE OUT."""

    # Test with new TPD
    compressor = DigiLangValidation(tpd_path=tpd_path)
    result = compressor.compress(test_text)

    print(f"\nTest Results:")
    print(f"  Original: {result.original_tokens} tokens")
    print(f"  Compressed: {result.compressed_tokens} tokens")
    print(f"  Reduction: {result.compression_ratio:.1%}")

    if result.compression_ratio > 0.15:
        print("\n✅ SUCCESS! Achieved >15% compression")
    else:
        print(f"\n⚠️ Compression below target (got {result.compression_ratio:.1%}, want 20%)")

    # Test reversibility
    decompressed = compressor.decompress(result.compressed_text)
    words_original = set(test_text.lower().split())
    words_decompressed = set(decompressed.lower().split())
    overlap = len(words_original & words_decompressed) / len(words_original) if words_original else 0

    print(f"\nReversibility: {overlap:.1%} word overlap")
    if overlap > 0.9:
        print("✅ Good reversibility")
    else:
        print("⚠️ Reversibility needs improvement")

def main():
    """Main execution."""
    print("\n🎬 SCREENPLAY TPD OPTIMIZATION")
    print("Building specialized compression for movie scripts\n")

    # Step 1: Analyze corpus
    sample = analyze_corpus_patterns()

    # Step 2: Build TPD
    tpd_path = build_optimized_tpd()

    # Step 3: Test compression
    if tpd_path:
        test_new_tpd()

    print("\n" + "="*60)
    print("✓ TPD BUILD COMPLETE")
    print("Next step: Run full retranslation with new TPD")
    print("="*60)

if __name__ == "__main__":
    main()