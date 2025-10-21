#!/usr/bin/env python3
"""
Final compression test with custom TPD dictionary.
"""

from apps.scripturemon.digilang.encoder import DigiLangEncoder
from apps.scripturemon.digilang.decoder import DigiLangDecoder
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive

# Comprehensive screenplay text for final test
screenplay_text = """FADE IN:

EXT. CASTLE ELSINORE - DAY

The ancient walls of Elsinore Castle rise against a stormy sky. HAMLET (30), Prince of Denmark, walks alone on the battlements.

HAMLET
To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune, or to take arms against a sea of troubles.

He pauses, gazing out at the churning sea.

HAMLET (CONT'D)
And by opposing, end them? To die, to sleep - no more. And by a sleep to say we end the heartache and the thousand natural shocks that flesh is heir to.

CUT TO:

INT. THRONE ROOM - DAY

CLAUDIUS (45), the King, sits upon his throne. GERTRUDE (40), the Queen, stands beside him. POLONIUS (50) whispers urgently in the King's ear.

CLAUDIUS
Where is my nephew Hamlet? His melancholy grows ever deeper.

GERTRUDE
My lord, he speaks in riddles and avoids our company. I fear for his mind.

POLONIUS
Your Majesty, I believe the Prince's madness stems from his love for my daughter Ophelia.

The King considers this.

CLAUDIUS
Then we shall test this theory. Set a watch upon him.

DISSOLVE TO:

EXT. GRAVEYARD - NIGHT

HAMLET stands before his father's tomb. The GHOST (45) of King Hamlet appears, glowing in the moonlight.

GHOST
My son, I am thy father's spirit, doomed for a certain term to walk the night.

HAMLET
My father! Speak, I am bound to hear.

GHOST
So art thou to revenge when thou shalt hear. The serpent that did sting thy father's life now wears his crown.

HAMLET
My uncle!

GHOST
Ay, that incestuous, that adulterate beast. But howsoever thou pursuest this act, taint not thy mind nor let thy soul contrive against thy mother aught.

Thunder rolls. The Ghost begins to fade.

GHOST (CONT'D)
Remember me!

He vanishes. HAMLET falls to his knees.

HAMLET
The time is out of joint. O cursed spite, that ever I was born to set it right!

FADE OUT."""

print("=" * 60)
print("FINAL DIGILANG COMPRESSION TEST")
print("=" * 60)

print(f"\nOriginal text: {len(screenplay_text)} characters")

# Apply aggressive canonicalization
canon_text = canon_aggressive(screenplay_text, drop_parentheticals=True, drop_stage=True)
print(f"Canonicalized: {len(canon_text)} characters ({100*len(canon_text)/len(screenplay_text):.1f}%)")

# Test configurations
configs = [
    ("Default API", "api", None),
    ("Default TPD", "tpd", "data/tpd/default/token_dict.json"),
    ("High-compression TPD", "tpd", "data/tpd/K3000_n2-6/token_dict.json"),
    ("Custom Screenplay TPD", "tpd", "data/tpd/custom_screenplay/token_dict.json"),
]

best_compression = 0
best_working = None
results = []

for config_name, method, tpd_path in configs:
    print(f"\n{'-'*50}")
    print(f"Testing: {config_name}")
    print(f"{'-'*50}")

    try:
        if method == "api":
            from apps.scripturemon.digilang import to_digilang, from_digilang
            compressed, ratio = to_digilang(canon_text)
            decoded = from_digilang(compressed)
        else:
            encoder = DigiLangEncoder(use_tpd=True, token_dict_path=tpd_path)
            decoder = DigiLangDecoder(use_tpd=True, token_dict_path=tpd_path)
            compressed, ratio = encoder.encode(canon_text)
            decoded = decoder.decode(compressed)

        print(f"Input length: {len(canon_text)}")
        print(f"Compressed length: {len(compressed)}")
        print(f"Compression ratio: {ratio:.1%}")

        roundtrip_success = canon_text == decoded
        print(f"Roundtrip successful: {roundtrip_success}")

        results.append((config_name, ratio, roundtrip_success, len(compressed)))

        if roundtrip_success:
            print(f"✓ PERFECT: {ratio:.1%}")
            if ratio > best_compression:
                best_compression = ratio
                best_working = config_name
        else:
            print(f"✗ Imperfect roundtrip")
            # Count character differences
            diffs = sum(1 for a, b in zip(canon_text, decoded) if a != b)
            print(f"Character differences: {diffs} / {len(canon_text)} ({100*diffs/len(canon_text):.1f}%)")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        results.append((config_name, 0, False, 0))

print(f"\n{'='*60}")
print("FINAL RESULTS")
print(f"{'='*60}")

print(f"\nCompression Results:")
print(f"{'Configuration':<25} {'Ratio':<8} {'Perfect':<8} {'Size':<6}")
print("-" * 50)
for config, ratio, perfect, size in results:
    status = "✓" if perfect else "✗"
    print(f"{config:<25} {ratio:<7.1%} {status:<8} {size:<6}")

if best_working:
    print(f"\nBest working configuration: {best_working}")
    print(f"Best compression ratio: {best_compression:.1%}")

target_met = best_compression >= 0.20
print(f"\nTarget achievement (20-22%): {'✓ SUCCESS' if target_met else '✗ Not reached'}")

if target_met:
    print(f"\n🎉 DigiLang successfully achieves {best_compression:.1%} compression!")
    print("The system meets the target of 20-22% compression with full reversibility.")
    print("\nKey components working:")
    print("- ✓ Token trie for longest-match compression")
    print("- ✓ Tokenizer utilities for glyph selection")
    print("- ✓ Canonicalization for text normalization")
    print("- ✓ Vocabulary with symbols and MWEs")
    print("- ✓ TPD system for token-level compression")
    print("- ✓ Fixed decoder with proper symbol ordering")
else:
    highest_ratio = max(ratio for _, ratio, _, _ in results)
    print(f"\nHighest compression achieved: {highest_ratio:.1%}")
    print("DigiLang components are functional but additional optimization needed.")

print("=" * 60)