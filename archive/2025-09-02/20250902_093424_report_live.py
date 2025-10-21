# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import os, sys, time, subprocess

PY = os.environ.get("PYTHON", sys.executable)

def run(cmd:list[str]):
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def main():
    interval = int(os.environ.get("UI_LIVE_INTERVAL", "10"))  # segundos
    one_shot = bool(os.environ.get("UI_LIVE_ONESHOT", ""))     # se definido, roda uma vez
    while True:
        run([PY, "scripts/collect_ultimate_history.py"])
        run([PY, "scripts/aggregate_perf.py"])
        run([PY, "scripts/generate_report_html.py"])
        run([PY, "scripts/patch_report_with_strategy.py"])
        run([PY, "scripts/patch_live_reload.py"])
        # export do painel isolado (se existir util)
        if Path("scripts/export_ultimate_panel.py").exists():
            run([PY, "scripts/export_ultimate_panel.py"])
        print(f"[OK] report live tick ({interval}s)")
        if one_shot: break
        time.sleep(max(2, interval))

if __name__=="__main__": main()