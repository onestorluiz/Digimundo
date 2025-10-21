import os, json, hashlib, platform, time
from pathlib import Path
ROOT=Path("."); OUT=ROOT/"dist"; OUT.mkdir(parents=True, exist_ok=True)
ts=time.strftime("%Y%m%d-%H%M%S")
bundle=OUT/f"scripturemon_artifacts_{ts}.zip"
manifest={"created_utc":ts,"git":os.popen("git rev-parse HEAD").read().strip(),"files":[],"system":{"os":platform.platform()}}
import zipfile
with zipfile.ZipFile(bundle,"w",zipfile.ZIP_DEFLATED) as z:
  for p in ["reports/scorecard.json","reports/index.html","reports/debug/debug_summary.md"]:
    if Path(p).exists():
      z.write(p); manifest["files"].append({"path":p})
  for p in Path("results").rglob("*.csv"):
    z.write(p); manifest["files"].append({"path":str(p)})
# hash de cada arquivo incluído
for f in manifest["files"]:
  h=hashlib.sha256(Path(f["path"]).read_bytes()).hexdigest()
  f["sha256"]=h
(Path("dist/manifest.json")).write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print("[OK] bundle ->", bundle)