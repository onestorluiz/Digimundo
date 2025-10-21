#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Empacota artefatos de resultados e relatórios em um ZIP reprodutível.
- Saída: dist/scripturemon_report_<YYYYMMDD-HHMMSS>.zip
- Manifesto: dist/manifest_<ts>.json (paths, bytes, sha256)
- Checksums: dist/SHA256SUMS_<ts>.txt
Uso:
  python scripts/package_artifacts.py \
      --prefix scripturemon_report --history 5 \
      --include-results --include-figures --include-history
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, zipfile, time, os

ROOT = Path(".")
REPORTS = ROOT/"reports"
RESULTS = ROOT/"results"
FIGS = REPORTS/"figures"
HISTORY = REPORTS/"history"
DIST = ROOT/"dist"

def sha256sum(p: Path, bufsize: int = 1<<20) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(bufsize)
            if not b: break
            h.update(b)
    return h.hexdigest()

def collect_files(include_results: bool, include_figs: bool, include_history: bool, hist_keep: int):
    files = []
    def add_if_exists(rel):
        p = ROOT/rel
        if p.exists(): files.append(p)
    # Relatórios principais
    for rel in ["reports/index.html", "reports/report.md", "reports/report.pdf", "reports/scorecard.json"]:
        add_if_exists(rel)
    # Figuras
    if include_figs and FIGS.exists():
        for p in FIGS.glob("*.png"): files.append(p)
    # CSVs de resultados
    if include_results and RESULTS.exists():
        for sub in ["compression", "telepathy", "e2e", "rag", "memory"]:
            d = RESULTS/sub
            if d.exists():
                for p in d.glob("*.csv"): files.append(p)
    # Histórico (limitado)
    if include_history and HISTORY.exists():
        snaps = sorted(HISTORY.glob("scorecard_*.json"))[-hist_keep:]
        reps  = sorted(HISTORY.glob("report_*.md"))[-hist_keep:]
        files += snaps + reps
    # Docs de topo
    for rel in ["README.md","RESULTS.md","LICENSE"]:
        add_if_exists(rel)
    # Dedup e garantir paths relativos
    seen=set(); uniq=[]
    for p in files:
        rp = p.relative_to(ROOT)
        if rp not in seen:
            uniq.append(rp); seen.add(rp)
    return uniq

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="scripturemon_report")
    ap.add_argument("--history", type=int, default=5)
    ap.add_argument("--include-results", action="store_true", default=True)
    ap.add_argument("--include-figures", action="store_true", default=True)
    ap.add_argument("--include-history", action="store_true", default=True)
    args = ap.parse_args()

    ts = time.strftime("%Y%m%d-%H%M%S")
    DIST.mkdir(parents=True, exist_ok=True)
    zip_name = f"{args.prefix}_{ts}.zip"
    zip_path = DIST/zip_name

    files = collect_files(args.include_results, args.include_figures, args.include_history, args.history)

    manifest = {
        "created_at": ts,
        "zip": str(zip_path),
        "counts": {
            "total": len(files),
            "results_csv": sum(1 for p in files if str(p).startswith("results/") and p.suffix==".csv"),
            "figures_png": sum(1 for p in files if str(p).startswith("reports/figures/") and p.suffix==".png"),
            "history": sum(1 for p in files if str(p).startswith("reports/history/")),
        },
        "files": []
    }

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for rp in files:
            src = ROOT/rp
            z.write(src, arcname=str(rp))
            sz = src.stat().st_size
            sh = sha256sum(src)
            manifest["files"].append({"path": str(rp), "bytes": sz, "sha256": sh})

    # SHA256 do ZIP
    zip_sha = sha256sum(zip_path)
    sums_path = DIST/f"SHA256SUMS_{ts}.txt"
    sums_path.write_text(f"{zip_sha}  {zip_name}\n", encoding="utf-8")

    # Manifesto
    mani_path = DIST/f"manifest_{ts}.json"
    mani_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Symlink/cópia "latest" (idempotente)
    latest = DIST/f"{args.prefix}_latest.zip"
    try:
        if latest.exists() or latest.is_symlink(): latest.unlink()
        os.symlink(zip_path.name, latest)  # relativo dentro de dist
    except Exception:
        # fallback: copia
        try:
            import shutil; shutil.copy2(zip_path, latest)
        except Exception:
            pass

    print(f"[OK] zip -> {zip_path.name} | {manifest['counts']}")
    print(f"[OK] manifest -> {mani_path.name}")
    print(f"[OK] checksums -> {sums_path.name}")
    print(f"[OK] latest -> {latest.name}")

if __name__ == "__main__":
    main()