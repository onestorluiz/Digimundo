#!/usr/bin/env python3
"""
Test DigiLang compression functionality and measure compression ratios.
"""

from apps.scripturemon.digilang import to_digilang, from_digilang, canon_strict, canon_aggressive

# Test screenplay content
screenplay_text = """FADE IN:

EXT. NEW YORK CITY STREET - DAY

The bustling streets of Manhattan. Yellow cabs honk their horns as pedestrians hurry along the sidewalk. Steam rises from manholes, creating an urban haze.

JOHN DAVIDSON (35), a determined detective with weathered features, walks purposefully down the street. He carries a worn leather briefcase and checks his watch nervously.

JOHN
(into phone)
I'm almost there. Has the suspect arrived yet?

INT. POLICE STATION - CONTINUOUS

SARAH MARTINEZ (28), a sharp-witted analyst, sits at her desk surrounded by files and computer monitors.

SARAH
Not yet, but we have surveillance on all exits. He can't get far.

JOHN (V.O.)
Good. This is our only chance to catch him.

EXT. NEW YORK CITY STREET - CONTINUOUS

John quickens his pace, dodging through the crowd. A BLACK SEDAN pulls up to the curb ahead of him.

JOHN
(whispered)
This is it.

CUT TO:

INT. BLACK SEDAN - SAME TIME

MARCUS THOMPSON (45), a well-dressed man with cold eyes, checks his gun methodically. He looks out the window, scanning the street.

MARCUS
(to driver)
Everything ready?

The DRIVER nods without turning around.

FADE OUT."""

print("=" * 60)
print("DIGILANG COMPRESSION TEST")
print("=" * 60)

print(f"\nOriginal text length: {len(screenplay_text)} characters")
print(f"Original text sample:\n{screenplay_text[:200]}...\n")

# Test different canonicalization approaches
print("Testing canonicalization approaches:")
print("-" * 40)

# Strict canonicalization
strict_canon = canon_strict(screenplay_text)
print(f"Strict canonicalization: {len(strict_canon)} chars ({len(strict_canon)/len(screenplay_text)*100:.1f}% of original)")

# Aggressive canonicalization
aggressive_canon = canon_aggressive(screenplay_text)
print(f"Aggressive canonicalization: {len(aggressive_canon)} chars ({len(aggressive_canon)/len(screenplay_text)*100:.1f}% of original)")

print("\nTesting compression:")
print("-" * 40)

# Test compression on original text
try:
    compressed_orig, ratio_orig = to_digilang(screenplay_text)
    print(f"Original text compression: {len(compressed_orig)} chars, ratio: {ratio_orig:.1%}")

    # Test roundtrip
    decoded_orig = from_digilang(compressed_orig)
    roundtrip_success = screenplay_text == decoded_orig
    print(f"Roundtrip successful: {roundtrip_success}")
    if not roundtrip_success:
        print(f"Differences found in first 100 chars:")
        print(f"Original: {repr(screenplay_text[:100])}")
        print(f"Decoded:  {repr(decoded_orig[:100])}")

except Exception as e:
    print(f"Error with original text: {e}")

# Test compression on canonicalized text
try:
    compressed_canon, ratio_canon = to_digilang(strict_canon)
    print(f"Canonicalized text compression: {len(compressed_canon)} chars, ratio: {ratio_canon:.1%}")

    # Test roundtrip
    decoded_canon = from_digilang(compressed_canon)
    roundtrip_success = strict_canon == decoded_canon
    print(f"Canonicalized roundtrip successful: {roundtrip_success}")

except Exception as e:
    print(f"Error with canonicalized text: {e}")

# Test compression on aggressively canonicalized text
try:
    compressed_aggr, ratio_aggr = to_digilang(aggressive_canon)
    print(f"Aggressively canonicalized text compression: {len(compressed_aggr)} chars, ratio: {ratio_aggr:.1%}")

    # Test roundtrip
    decoded_aggr = from_digilang(compressed_aggr)
    roundtrip_success = aggressive_canon == decoded_aggr
    print(f"Aggressive canonicalized roundtrip successful: {roundtrip_success}")

    if roundtrip_success:
        print(f"\nBest compression achieved: {ratio_aggr:.1%}")
        print(f"Compressed text sample: {compressed_aggr[:100]}...")

except Exception as e:
    print(f"Error with aggressively canonicalized text: {e}")

print("\n" + "=" * 60)