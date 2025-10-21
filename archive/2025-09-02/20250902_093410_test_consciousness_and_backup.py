# -*- coding: utf-8 -*-
from apps.scripturemon.consciousness import evolve, read
from apps.scripturemon.backup import backup_once
from apps.scripturemon.membridge import promote, counts

def test_consciousness_evolve_and_backup(tmp_path, monkeypatch):
    # isola HOME p/ não tocar usuário
    monkeypatch.setenv("HOME", str(tmp_path))
    lvl=evolve(0.001)
    assert lvl>=1.0
    promote({"kind":"note","text":"ok"}, importance=0.6)
    c=counts()
    assert "L1" in c and "L2" in c
    p=backup_once()
    assert p.endswith("checkpoint_" + p.split("_")[-1])