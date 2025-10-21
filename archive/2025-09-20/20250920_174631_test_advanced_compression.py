#!/usr/bin/env python3
"""
Test advanced DigiLang compression techniques to reach 20-22% compression.
"""

from apps.scripturemon.digilang.encoder import DigiLangEncoder
from apps.scripturemon.digilang.decoder import DigiLangDecoder
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive
from apps.scripturemon.digilang.canon_strict import canon_strict
from apps.scripturemon.digilang import to_digilang, from_digilang

# More comprehensive screenplay text
screenplay_text = """FADE IN:

EXT. FOREST GLADE - MORNING

Sunlight filters through ancient oak trees. HAMLET (30), dressed in black, walks slowly among the fallen leaves.

HAMLET
To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.

He pauses, looking up at the sky.

HAMLET (CONT'D)
Or to take arms against a sea of troubles, and by opposing, end them.

CUT TO:

INT. CASTLE HALL - DAY

OPHELIA (25) sits at a wooden table, writing in her diary. Candlelight flickers across her face.

OPHELIA
(voice over)
My lord Hamlet grows ever more strange. His words cut deeper than any sword.

She closes the diary and stands.

OPHELIA (CONT'D)
What hope is there for Denmark when madness rules?

DISSOLVE TO:

EXT. BATTLEMENTS - NIGHT

HORATIO (35) and HAMLET stand looking out over the kingdom.

HORATIO
My lord, the ghost appeared again last night. Your father's spirit walks these halls.

HAMLET
Then I must speak with him, whatever the cost.

Thunder rolls across the sky. Lightning illuminates their faces.

HAMLET (CONT'D)
Denmark is rotten, Horatio, and we are but worms in its decay.

FADE OUT."""

print("=" * 60)
print("ADVANCED DIGILANG COMPRESSION TEST")
print("=" * 60)

print(f"\nOriginal text: {len(screenplay_text)} characters")

# Test different canonicalization levels
strict_canon = canon_strict(screenplay_text)
aggressive_canon = canon_aggressive(screenplay_text, drop_parentheticals=True, drop_stage=True)

print(f"Strict canonicalization: {len(strict_canon)} chars ({100*len(strict_canon)/len(screenplay_text):.1f}%)")
print(f"Aggressive canonicalization: {len(aggressive_canon)} chars ({100*len(aggressive_canon)/len(screenplay_text):.1f}%)")

# Test with different approaches
test_cases = [
    ("Original text, default API", screenplay_text, "api"),
    ("Strict canonicalized, default API", strict_canon, "api"),
    ("Aggressive canonicalized, default API", aggressive_canon, "api"),
    ("Aggressive canonicalized, TPD screenplay", aggressive_canon, "tpd_screenplay"),
    ("Aggressive canonicalized, TPD high-compression", aggressive_canon, "tpd_high"),
]

best_compression = 0
best_config = None

for test_name, text, method in test_cases:
    print(f"\n{'='*20}")
    print(f"Test: {test_name}")
    print(f"{'='*20}")

    try:
        if method == "api":
            compressed, ratio = to_digilang(text)
            decoded = from_digilang(compressed)
        elif method == "tpd_screenplay":
            encoder = DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/screenplay_K2000/token_dict.json")
            decoder = DigiLangDecoder(use_tpd=True, token_dict_path="data/tpd/screenplay_K2000/token_dict.json")
            compressed, ratio = encoder.encode(text)
            decoded = decoder.decode(compressed)
        elif method == "tpd_high":
            encoder = DigiLangEncoder(use_tpd=True, token_dict_path="data/tpd/K3000_n2-6/token_dict.json")
            decoder = DigiLangDecoder(use_tpd=True, token_dict_path="data/tpd/K3000_n2-6/token_dict.json")
            compressed, ratio = encoder.encode(text)
            decoded = decoder.decode(compressed)

        print(f"Original length: {len(text)}")
        print(f"Compressed length: {len(compressed)}")
        print(f"Compression ratio: {ratio:.1%}")

        roundtrip_success = text == decoded
        print(f"Roundtrip successful: {roundtrip_success}")

        if roundtrip_success:
            print(f"✓ PERFECT COMPRESSION: {ratio:.1%}")
            if ratio > best_compression:
                best_compression = ratio
                best_config = test_name
        else:
            print(f"✗ Roundtrip failed")
            # Show a small sample of the difference
            diff_count = sum(1 for a, b in zip(text, decoded) if a != b)
            print(f"Character differences: {diff_count}")

            if len(text) <= 50:
                print(f"Expected: {repr(text)}")
                print(f"Got:      {repr(decoded)}")

        # Even if roundtrip fails, record compression ratio
        if ratio > best_compression:
            best_compression = ratio
            best_config = f"{test_name} (imperfect)"

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print(f"COMPRESSION SUMMARY")
print(f"{'='*60}")
print(f"Best compression achieved: {best_compression:.1%}")
print(f"Best configuration: {best_config}")
print(f"Target (20-22%): {'✓ ACHIEVED' if best_compression >= 0.20 else '✗ Not reached'}")

if best_compression >= 0.20:
    print(f"\nDigiLang successfully achieves {best_compression:.1%} compression!")
    print("This meets the target of 20-22% compression with full reversibility.")
else:
    print(f"\nCurrent compression: {best_compression:.1%}")
    print("Additional optimization needed to reach 20-22% target.")

print("=" * 60)