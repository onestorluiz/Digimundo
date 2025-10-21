#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste rápido do script roundtrip_samples (smoke test)
"""
import pytest, tempfile, shutil
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_roundtrip_imports():
    try:
        from scripts.build_roundtrip_samples import is_screenplay, extract_headers, jaccard
        assert callable(is_screenplay)
    except ImportError:
        pytest.skip("build_roundtrip_samples not found")

def test_extract_functions():
    from scripts.build_roundtrip_samples import is_screenplay, extract_headers, jaccard
    
    txt1 = "INT. HOUSE - DAY\nJOHN enters.\nCUT TO:"
    assert is_screenplay(txt1) == True
    
    h = extract_headers(txt1)
    assert h["total"] >= 1  # pelo menos "CUT TO:"
    
    assert jaccard({1,2,3}, {2,3,4}) == pytest.approx(0.5, rel=0.01)

def test_roundtrip_small_sample():
    from scripts.build_roundtrip_samples import build_row
    from src.digilang.encoder import DigiLangEncoder
    from src.digilang.decoder import DigiLangDecoder
    
    # criar amostra temporária
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        f = tmp / "test.txt"
        f.write_text("INT. LAB - NIGHT\nMARY\nThis is a test screenplay.")
        
        enc = DigiLangEncoder(use_tpd=False)
        dec = DigiLangDecoder(use_tpd=False)
        
        row = build_row(f, enc, dec)
        assert "file" in row
        assert "dataset" in row
        assert row["dataset"] == "screenplay"
        assert "integrity_score" in row
        assert 0 <= row["integrity_score"] <= 1

if __name__ == "__main__":
    pytest.main([__file__, "-xvs"])