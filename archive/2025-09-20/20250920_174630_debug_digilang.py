#!/usr/bin/env python3
"""
Debug DigiLang encoding/decoding process to identify issues.
"""

from apps.scripturemon.digilang.encoder import DigiLangEncoder
from apps.scripturemon.digilang.decoder import DigiLangDecoder
from apps.scripturemon.digilang.canon_aggressive import canon_aggressive
import tiktoken

# Simple test text
test_text = "FADE IN:"

print("=" * 50)
print("DIGILANG DEBUG")
print("=" * 50)

print(f"Original: '{test_text}'")

# Test with no TPD first
encoder = DigiLangEncoder(use_tpd=False)
decoder = DigiLangDecoder(use_tpd=False)

enc = tiktoken.get_encoding("cl100k_base")

print(f"\nToken IDs of original: {enc.encode(test_text)}")

# Encode
compressed, ratio = encoder.encode(test_text)
print(f"Compressed: '{compressed}' (ratio: {ratio:.1%})")
print(f"Token IDs of compressed: {enc.encode(compressed)}")

# Check vocabulary symbols
print(f"\nVocabulary symbols that might apply:")
for symbol, glyph in encoder.vocab.symbols.items():
    if symbol in test_text or symbol.replace('_', ' ') in test_text:
        print(f"  {symbol} -> {repr(glyph)}")

# Check MWE map
print(f"\nMWE mappings that might apply:")
for phrase, glyph in encoder.vocab.mwe_map.items():
    if phrase in test_text:
        print(f"  '{phrase}' -> {repr(glyph)}")

# Decode step by step
print(f"\nDecoding process:")

# Get decoder's reverse mappings
print(f"Symbol reverse mappings:")
for glyph, symbol in decoder.symbol_reverse.items():
    if glyph in compressed:
        print(f"  {repr(glyph)} -> {symbol}")

print(f"MWE reverse mappings:")
for glyph, phrase in decoder.mwe_reverse.items():
    if glyph in compressed:
        print(f"  {repr(glyph)} -> '{phrase}'")

# Decode
decoded = decoder.decode(compressed)
print(f"Decoded: '{decoded}'")

print(f"\nMatch: {test_text == decoded}")
if test_text != decoded:
    print(f"Expected: {repr(test_text)}")
    print(f"Got:      {repr(decoded)}")

# Check what "FADE IN" maps to
print(f"\n=== FADE IN Analysis ===")
fade_in_tokens = enc.encode("FADE IN")
print(f"'FADE IN' tokens: {fade_in_tokens}")

# Check if it's in vocab symbols
for symbol, glyph in encoder.vocab.symbols.items():
    if "FADE" in symbol or "IN" in symbol:
        print(f"Symbol {symbol} -> {repr(glyph)}")

# Check if it's in MWE
for phrase, glyph in encoder.vocab.mwe_map.items():
    if "FADE" in phrase:
        print(f"MWE '{phrase}' -> {repr(glyph)}")

print("=" * 50)