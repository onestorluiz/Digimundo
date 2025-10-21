#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, zipfile, time, os

ROOT = Path(".")
REPORTS = ROOT/"reports"
AGG = REPORTS/"aggregates"
FIGS = REPORTS/"figures"
DIST = ROOT/"dist"

KEEP_PNG = {
    "integrity_boxplot.png",
    "entity_retain_hist.png",
    "reduction_canon+tpd.png",
    "telepathy_bytes_mean.png",
    "telepathy_throughput.png"
}

def sha256sum(p: Path, bufsize=1<<20):
    import hashlib
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(bufsize)
            if not b: break
            h.update(b)
    return h.hexdigest()

def collect_files():
    files=[]
    def add(rel):
        p=ROOT/rel
        if p.exists(): files.append(p)
    # reports principais
    for rel in ["reports/index.html","reports/report.md","reports/report.pdf","reports/scorecard.json"]:
        add(rel)
    # aggregates
    if AGG.exists():
        for p in AGG.glob("*.csv"): files.append(p)
        add("reports/aggregates/manifest.json")
    # figuras selecionadas
    if FIGS.exists():
        for p in FIGS.glob("*.png"):
            if p.name in KEEP_PNG:
                files.append(p)
    # docs raiz
    for rel in ["README.md","RESULTS.md","LICENSE"]:
        add(rel)
    # dedup
    uniq=[]; seen=set()
    for p in files:
        rp=p.relative_to(ROOT)
        if rp not in seen:
            uniq.append(rp); seen.add(rp)
    return uniq

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--prefix", default="scripturemon_release")
    args=ap.parse_args()

    DIST.mkdir(parents=True, exist_ok=True)
    ts=time.strftime("%Y%m%d-%H%M%S")
    zip_name=f"{args.prefix}_{ts}.zip"
    zip_path=DIST/zip_name

    files=collect_files()
    manifest={"created_at":ts,"zip":zip_name,"counts":{"total":len(files),"aggregates":sum(1 for p in files if str(p).startswith('reports/aggregates/')),"figures":sum(1 for p in files if str(p).startswith('reports/figures/'))},"files":[]}

    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for rp in files:
            src=ROOT/rp; z.write(src, arcname=str(rp))
            manifest["files"].append({"path":str(rp), "bytes":src.stat().st_size, "sha256":sha256sum(src)})

    sums_path=DIST/f"SHA256SUMS_{ts}.txt"; sums_path.write_text(f"{sha256sum(zip_path)}  {zip_name}\n", encoding="utf-8")
    mani_path=DIST/f"manifest_release_{ts}.json"; mani_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    latest=DIST/f"{args.prefix}_latest.zip"
    try:
        if latest.exists() or latest.is_symlink(): latest.unlink()
        os.symlink(zip_path.name, latest)
    except Exception:
        try:
            import shutil; shutil.copy2(zip_path, latest)
        except Exception:
            pass

    print(f"[OK] release zip -> {zip_path.name} | total={manifest['counts']['total']}")
    print(f"[OK] manifest -> {mani_path.name}")
    print(f"[OK] checksums -> {sums_path.name}")
    print(f"[OK] latest -> {latest.name}")

if __name__=="__main__":
    main()