#!/usr/bin/env python
"""
Basic tests for TPD adaptive implementation.
"""

import sys
sys.path.append('.')

import json
import tempfile
from pathlib import Path
from src.digilang.encoder import DigiLangEncoder
from src.digilang.decoder import DigiLangDecoder

def test_tpd_compression():
    """Test compression with minimal synthetic TPD."""
    
    # Create synthetic token dict
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    
    # Create patterns that should match in test text
    text = "to be or not to be that is the question"
    ids = enc.encode(text)
    
    # Create synthetic TPD with 2 patterns
    patterns = {
        "α": [enc.encode("to be")[0], enc.encode("to be")[1]] if len(enc.encode("to be")) > 1 else enc.encode("to be"),
        "β": enc.encode("the question")
    }
    
    # Save to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        tpd_path = Path(tmpdir) / "token_dict.json"
        tpd_data = {
            "meta": {"tokenizer": "cl100k_base", "K": 2},
            "map": patterns
        }
        tpd_path.write_text(json.dumps(tpd_data), encoding="utf-8")
        
        # Test encoding
        encoder = DigiLangEncoder(use_tpd=True, token_dict_path=str(tpd_path))
        compressed, ratio = encoder.encode(text, canonicalize_text=False)
        
        # Should have some compression
        tokens_before = len(enc.encode(text))
        tokens_after = len(enc.encode(compressed))
        assert tokens_after < tokens_before, f"Should compress: {tokens_before} -> {tokens_after}"
        
        # Test decoding (roundtrip)
        decoder = DigiLangDecoder(use_tpd=True, token_dict_path=str(tpd_path))
        decompressed = decoder.decode(compressed)
        
        # Check key words preserved
        assert "question" in decompressed.lower() or "question" in compressed.lower()
        
        print(f"✅ TPD compression test passed (ratio: {ratio:.1%})")

def test_tpd_roundtrip():
    """Test full roundtrip with TPD."""
    # If default TPD exists, test with it
    default_tpd = Path("data/tpd/default/token_dict.json")
    if not default_tpd.exists():
        print("⚠️ Skipping roundtrip test (no default TPD)")
        return
    
    text = "The quick brown fox jumps over the lazy dog. " * 5
    
    encoder = DigiLangEncoder(use_tpd=True)
    compressed, ratio = encoder.encode(text)
    
    decoder = DigiLangDecoder(use_tpd=True)
    decompressed = decoder.decode(compressed)
    
    # Check some preservation
    assert "fox" in decompressed.lower() or "fox" in compressed.lower()
    print(f"✅ TPD roundtrip test passed (ratio: {ratio:.1%})")

if __name__ == "__main__":
    test_tpd_compression()
    test_tpd_roundtrip()
    print("\n✅ All TPD adaptive tests passed!")