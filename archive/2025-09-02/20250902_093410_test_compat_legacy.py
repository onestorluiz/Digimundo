# -*- coding: utf-8 -*-
import os, importlib
from types import SimpleNamespace

def _reload_entry():
    if "apps.scripturemon.entrypoint" in globals():
        import sys; sys.modules.pop("apps.scripturemon.entrypoint", None)
    return importlib.import_module("apps.scripturemon.entrypoint")

def test_mode_env_fusion(monkeypatch):
    ep = _reload_entry()
    calls = {"cli":0,"compat":0}
    monkeypatch.setenv("SCRIPTUREMON_MODE","fusion")
    monkeypatch.setattr(ep, "run_cli", lambda args: calls.__setitem__("cli", calls["cli"]+1) or 0)
    monkeypatch.setattr(ep, "run_compat", lambda args: calls.__setitem__("compat", calls["compat"]+1) or 0)
    assert ep.main(["help"]) == 0
    assert calls["cli"]==1 and calls["compat"]==0

def test_mode_env_legacy(monkeypatch):
    ep = _reload_entry()
    calls = {"cli":0,"compat":0}
    monkeypatch.setenv("SCRIPTUREMON_MODE","legacy")
    monkeypatch.setattr(ep, "run_cli", lambda args: calls.__setitem__("cli", calls["cli"]+1) or 0)
    monkeypatch.setattr(ep, "run_compat", lambda args: calls.__setitem__("compat", calls["compat"]+1) or 0)
    assert ep.main(["status"]) == 0
    assert calls["compat"]==1 and calls["cli"]==0

def test_mode_file_auto_legacy_flag(monkeypatch, tmp_path):
    # Usa arquivo configs/scripturemon.mode=auto
    ep = _reload_entry()
    calls = {"cli":0,"compat":0}
    monkeypatch.delenv("SCRIPTUREMON_MODE", raising=False)
    cfg = tmp_path/"configs"; cfg.mkdir(parents=True, exist_ok=True)
    (cfg/"scripturemon.mode").write_text("auto", encoding="utf-8")
    # Monkeypatch Path to read from tmp repo for mode file
    monkeypatch.setattr(ep.Path, "read_text", lambda self, **kw: (cfg/"scripturemon.mode").read_text(**kw) if self.name=="scripturemon.mode" else "")
    # Stub runners
    monkeypatch.setattr(ep, "run_cli", lambda args: calls.__setitem__("cli", calls["cli"]+1) or 0)
    monkeypatch.setattr(ep, "run_compat", lambda args: calls.__setitem__("compat", calls["compat"]+1) or 0)
    # Flag legado (--classic) deve forçar compat
    assert ep.main(["--classic"]) == 0
    assert calls["compat"]==1 and calls["cli"]==0

def test_mode_file_auto_default_cli(monkeypatch, tmp_path):
    ep = _reload_entry()
    calls = {"cli":0,"compat":0}
    monkeypatch.delenv("SCRIPTUREMON_MODE", raising=False)
    cfg = tmp_path/"configs"; cfg.mkdir(parents=True, exist_ok=True)
    (cfg/"scripturemon.mode").write_text("auto", encoding="utf-8")
    monkeypatch.setattr(ep.Path, "read_text", lambda self, **kw: (cfg/"scripturemon.mode").read_text(**kw) if self.name=="scripturemon.mode" else "")
    monkeypatch.setattr(ep, "run_cli", lambda args: calls.__setitem__("cli", calls["cli"]+1) or 0)
    monkeypatch.setattr(ep, "run_compat", lambda args: calls.__setitem__("compat", calls["compat"]+1) or 0)
    # Sem flags legadas -> CLI
    assert ep.main(["report","--open","false"]) == 0
    assert calls["cli"]==1 and calls["compat"]==0