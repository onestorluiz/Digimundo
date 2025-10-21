
import json, csv
from pathlib import Path
from datetime import datetime
class ArtifactWriter:
    def __init__(self, outputs_root: str, run_id: str):
        self.dir = Path(outputs_root) / run_id; self.dir.mkdir(parents=True, exist_ok=True)
        self.root = Path(outputs_root)
    def write(self, name: str, obj):
        p = self.dir / name
        if isinstance(obj, str): p.write_text(obj, encoding="utf-8")
        else: p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    def stamp(self, status: str, extras: dict | None = None):
        run = {"ts": datetime.utcnow().isoformat()+"Z", "status": status}
        if extras: run.update(extras)
        self.write("run.json", run)
    def append_history(self, record: dict):
        jl = self.root / "_run_log.jsonl"
        with open(jl, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        csvp = self.root / "_run_log.csv"
        headers = ["ts","run_id","preset","quality","faithfulness","relevancy","locality","production_score","specialists"]
        exists = csvp.exists()
        with open(csvp, "a", newline="", encoding="utf-8") as f:
            import csv as _csv
            w = _csv.DictWriter(f, fieldnames=headers)
            if not exists: w.writeheader()
            w.writerow({k: record.get(k, "") for k in headers})
