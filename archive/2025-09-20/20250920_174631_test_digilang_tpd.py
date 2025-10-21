#!/usr/bin/env python3
"""
Test DigiLang compression with TPD (Token Pair Dictionary) system.
"""

from apps.scripturemon.digilang.encoder import DigiLangEncoder
from apps.scripturemon.digilang.decoder import DigiLangDecoder
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive
from apps.scripturemon.digilang.canon_strict import canon_strict

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
print("DIGILANG TPD COMPRESSION TEST")
print("=" * 60)

print(f"\nOriginal text length: {len(screenplay_text)} characters")

# Test different TPD configurations
tpd_configs = [
    ("No TPD", None),
    ("Default TPD", "data/tpd/default/token_dict.json"),
    ("Screenplay TPD", "data/tpd/screenplay_K2000/token_dict.json"),
    ("High-compression TPD", "data/tpd/K3000_n2-6/token_dict.json")
]

# Test canonicalization first
canon_text = canon_aggressive(screenplay_text, drop_parentheticals=True, drop_stage=True)
print(f"Canonicalized text length: {len(canon_text)} characters ({len(canon_text)/len(screenplay_text)*100:.1f}% of original)")

for config_name, tpd_path in tpd_configs:
    print(f"\n{'='*20} {config_name} {'='*20}")

    try:
        # Create encoder/decoder with this TPD configuration
        if tpd_path is None:
            encoder = DigiLangEncoder(use_tpd=False)
            decoder = DigiLangDecoder(use_tpd=False)
        else:
            encoder = DigiLangEncoder(use_tpd=True, token_dict_path=tpd_path)
            decoder = DigiLangDecoder(use_tpd=True, token_dict_path=tpd_path)

        # Test with canonicalized text (should compress better)
        compressed, ratio = encoder.encode(canon_text)
        print(f"Compressed length: {len(compressed)} chars")
        print(f"Compression ratio: {ratio:.1%}")

        # Test roundtrip
        decoded = decoder.decode(compressed)
        roundtrip_success = canon_text == decoded
        print(f"Roundtrip successful: {roundtrip_success}")

        if roundtrip_success:
            print(f"✓ Perfect compression: {ratio:.1%}")
            print(f"Sample compressed: {compressed[:80]}...")
        else:
            print(f"✗ Roundtrip failed")
            # Show first difference
            for i, (a, b) in enumerate(zip(canon_text, decoded)):
                if a != b:
                    print(f"First diff at pos {i}: '{a}' != '{b}'")
                    print(f"Context: ...{canon_text[max(0,i-20):i+20]}...")
                    break
            if len(canon_text) != len(decoded):
                print(f"Length mismatch: {len(canon_text)} -> {len(decoded)}")

    except Exception as e:
        print(f"Error with {config_name}: {e}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")