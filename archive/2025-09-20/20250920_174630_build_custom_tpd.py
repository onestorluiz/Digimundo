#!/usr/bin/env python3
"""
Build a custom TPD dictionary optimized for screenplay content.
"""

from apps.scripturemon.digilang.tpd_builder import *
from apps.scripturemon.digilang.tokenizer_utils import get_single_token_strings
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive
import json
import tiktoken
from pathlib import Path

def build_screenplay_tpd():
    """Build a TPD optimized for screenplay content."""

    # Load all corpus files
    corpus_dir = Path("data/original")
    all_text = ""

    for txt_file in corpus_dir.glob("*.txt"):
        print(f"Loading {txt_file.name}...")
        with open(txt_file, 'r', encoding='utf-8') as f:
            text = f.read()
            # Apply aggressive canonicalization to match compression use
            canon_text = canon_aggressive(text, drop_parentheticals=True, drop_stage=True)
            all_text += canon_text + "\n\n"

    print(f"Total corpus size: {len(all_text)} characters")

    # Tokenize the entire corpus
    print("Tokenizing corpus...")
    token_ids = tokenize(all_text)
    print(f"Total tokens: {len(token_ids)}")

    # Mine n-grams with higher n_max for better compression
    print("Mining token n-grams...")
    ngrams = mine_token_ngrams(token_ids, n_min=2, n_max=12)  # Increased max length
    print(f"Found {len(ngrams)} unique n-grams")

    # Score candidates
    print("Scoring candidates...")
    candidates = score_candidates(ngrams)

    # Filter to high-value candidates
    min_freq = 3  # Must appear at least 3 times
    min_gain = 10  # Must save at least 10 tokens total
    good_candidates = [
        (ngram, freq, gain) for ngram, freq, gain in candidates
        if freq >= min_freq and gain >= min_gain
    ]

    print(f"High-value candidates: {len(good_candidates)}")

    # Get single-token strings for glyphs
    glyph_chars = get_single_token_strings(max_candidates=5000)
    print(f"Available glyph characters: {len(glyph_chars)}")

    # Build dictionary - take top candidates up to available glyphs
    num_patterns = min(len(good_candidates), len(glyph_chars))
    print(f"Building dictionary with {num_patterns} patterns...")

    tpd_map = {}
    for i in range(num_patterns):
        ngram, freq, gain = good_candidates[i]
        glyph = glyph_chars[i]
        tpd_map[glyph] = list(ngram)

    # Calculate expected compression
    total_savings = sum(gain for ngram, freq, gain in good_candidates[:num_patterns])
    total_tokens = len(token_ids)
    expected_compression = total_savings / total_tokens * 100

    print(f"Expected token savings: {total_savings} / {total_tokens} = {expected_compression:.1f}%")

    # Save TPD dictionary
    output_dir = Path("data/tpd/custom_screenplay")
    output_dir.mkdir(parents=True, exist_ok=True)

    tpd_data = {
        "layers": [{"map": tpd_map}],
        "meta": {
            "built_at": datetime.now().isoformat(),
            "corpus_tokens": total_tokens,
            "patterns": num_patterns,
            "expected_compression": f"{expected_compression:.1f}%",
            "min_freq": min_freq,
            "min_gain": min_gain
        }
    }

    output_file = output_dir / "token_dict.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tpd_data, f, ensure_ascii=False, indent=2)

    print(f"TPD dictionary saved to {output_file}")
    print(f"Dictionary contains {num_patterns} patterns")

    return str(output_file)

if __name__ == "__main__":
    tpd_path = build_screenplay_tpd()
    print(f"Custom TPD built at: {tpd_path}")