# -*- coding: utf-8 -*-
from scripts.ui_prefs import set_anchor, get_anchor
from pathlib import Path
def test_anchor_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    set_anchor("ultimate-performance")
    assert get_anchor()=="ultimate-performance"
    set_anchor("")
    assert get_anchor()=="" or get_anchor()==""  # tolerant