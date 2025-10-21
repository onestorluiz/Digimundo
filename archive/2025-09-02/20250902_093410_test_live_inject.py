# -*- coding: utf-8 -*-
from pathlib import Path
from scripts.patch_live_reload import inject_once, INJECT_ID

def test_inject_once(tmp_path):
    p = tmp_path/"x.html"
    p.write_text("<html><body><h1>ok</h1></body></html>", encoding="utf-8")
    assert inject_once(p) is True
    s = p.read_text(encoding="utf-8")
    assert INJECT_ID in s
    # re-injetar não duplica
    assert inject_once(p) is False