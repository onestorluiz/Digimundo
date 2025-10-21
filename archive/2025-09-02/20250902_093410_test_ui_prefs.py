# -*- coding: utf-8 -*-
from scripts.ui_prefs import set_live, get_live
from scripts.patch_live_reload import _inject_or_replace, INJECT_ID
from pathlib import Path
def test_set_get_live(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    set_live("10s")
    assert get_live()=="10s"
    set_live("off")
    assert get_live()=="off"
def test_inject_has_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("reports").mkdir(parents=True, exist_ok=True)
    Path("reports/index.html").write_text("<html><body>ok</body></html>", encoding="utf-8")
    # simula default "15s"
    from scripts.patch_live_reload import _template
    html = _template("15s")
    assert "DEFAULT = '15s'" in html