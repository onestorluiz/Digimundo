#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
import argparse, json, os, shutil, time, hashlib, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(".")
REPORTS = ROOT/"reports"
CONF_DIR = ROOT/"configs"
DEFAULT_TPD = ROOT/"data/tpd/default/token_dict.json"

def digest(p:Path)->str:
    try:
        h=hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda:f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def load_strategy()->dict:
    sfile = REPORTS/"compression_strategy.json"
    if not sfile.exists():
        print("[ERR] reports/compression_strategy.json not found"); sys.exit(2)
    return json.loads(sfile.read_text(encoding="utf-8"))

def pick_tpd_path(strategy:dict, prefer_dataset:str)->tuple[str, Path]|tuple[None, None]:
    tpd = strategy.get("tpd",{})
    paths = tpd.get("paths",{})
    # prefer per-dataset
    per_ds = tpd.get("per_dataset",{})
    cand_id = None
    if prefer_dataset in per_ds:
        cand_id = per_ds[prefer_dataset]["tpd"]
    elif tpd.get("best_overall"):
        cand_id = tpd["best_overall"]["tpd"]
    if not cand_id:
        return None, None
    # resolve path
    p = paths.get(cand_id)
    if p:
        return cand_id, Path(p)
    # fallback: procurar no sweep/stacked
    for d in [ROOT/"data/tpd/sweep_big", ROOT/"data/tpd/stacked"]:
        cand = d/cand_id/"token_dict.json"
        if cand.exists(): return cand_id, cand
    return cand_id, None

def backup_dest(dst:Path)->Path:
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return dst.with_name(dst.stem + f".backup.{ts}" + dst.suffix)

def write_env_json(mode:str, targets:list[str], tpd_id:str, tpd_src:Path, dst:Path, backup_path:Path|None):
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    env = [
        f"STRATEGY_MODE={mode}",
        f'STRATEGY_TARGETS={" ".join(targets) if targets else ""}',
        f"TPD_ID={tpd_id}",
        f"TPD_SOURCE={tpd_src}",
        f"TPD_DEFAULT={dst}",
        f"APPLIED_AT={datetime.utcnow().isoformat()}Z",
    ]
    (CONF_DIR/"bench_default.env").write_text("\n".join(env)+"\n", encoding="utf-8")

    manifest = {
        "strategy_source": "reports/compression_strategy.json",
        "applied_at": datetime.utcnow().isoformat()+"Z",
        "mode": mode,
        "targets": targets,
        "tpd": {
            "id": tpd_id,
            "source_path": str(tpd_src),
            "dest_path": str(dst),
            "dest_sha256": digest(dst),
            "backup_path": str(backup_path) if backup_path else None
        }
    }
    (CONF_DIR/"bench_default.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def apply(prefer_dataset:str):
    strat = load_strategy()
    mode = (strat.get("recommendation") or {}).get("mode","unknown")
    targets = (strat.get("recommendation") or {}).get("make_targets",[])

    tpd_id, src = pick_tpd_path(strat, prefer_dataset)
    if not tpd_id or src is None or not src.exists():
        print("[WARN] TPD path not resolved; keeping current default")
        write_env_json(mode, targets, tpd_id or "unknown", Path("N/A"), DEFAULT_TPD, None)
        print("[OK] strategy env -> configs/bench_default.env")
        return

    DEFAULT_TPD.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if DEFAULT_TPD.exists():
        # se conteúdo igual, nada a fazer
        if digest(DEFAULT_TPD)==digest(src):
            write_env_json(mode, targets, tpd_id, src, DEFAULT_TPD, None)
            print("[OK] TPD unchanged (same digest)"); print("[OK] strategy env -> configs/bench_default.env"); return
        backup = backup_dest(DEFAULT_TPD)
        shutil.copy2(DEFAULT_TPD, backup)
    shutil.copy2(src, DEFAULT_TPD)
    write_env_json(mode, targets, tpd_id, src, DEFAULT_TPD, backup)
    print(f"[OK] TPD default <- {src}")
    print("[OK] strategy env -> configs/bench_default.env")

def reset():
    manifest = CONF_DIR/"bench_default.json"
    if not manifest.exists():
        print("[WARN] no bench_default.json; nothing to reset"); return
    info = json.loads(manifest.read_text(encoding="utf-8"))
    bkp = info.get("tpd",{}).get("backup_path")
    if not bkp or not Path(bkp).exists():
        print("[WARN] backup not found; nothing to reset"); return
    shutil.copy2(Path(bkp), DEFAULT_TPD)
    print(f"[OK] restored default TPD from backup: {bkp}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefer_dataset", default="screenplay_synth", help="prefer this dataset's TPD if available")
    ap.add_argument("--reset", action="store_true", help="restore previous default.token_dict from backup")
    args = ap.parse_args()
    if args.reset:
        reset()
    else:
        apply(args.prefer_dataset)

if __name__=="__main__":
    main()