
from pathlib import Path
import json, csv, re

def _tokenize(s: str):
    return [t.lower() for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", s)]

def _jaccard(a, b):
    A, B = set(a), set(b)
    if not A and not B: return 1.0
    return len(A & B) / max(1, len(A | B))

def eval_against_golden(outputs_root: str, golden_path: str, out_csv: str | None = None) -> dict:
    g = json.loads(Path(golden_path).read_text(encoding="utf-8"))
    # Expect format: {"spec": {"field": expected_value or {"contains": ["tok1","tok2"], "equals": "Drama"}}}
    # We'll evaluate the latest run
    runs = sorted(Path(outputs_root).glob("*/evaluation.json"))
    if not runs: raise FileNotFoundError("Nenhuma execução encontrada em outputs/")
    last = runs[-1].parent
    results = {"run_id": last.name, "by_spec": {}}
    for spec, spec_expect in g.items():
        f = last / f"parsed_{spec}.json"
        if not f.exists(): continue
        d = json.loads(f.read_text(encoding="utf-8"))
        payload = d.get("payload", {}) or {}
        spec_res = {"checks": [], "pass": 0, "total": 0}
        for field, exp in spec_expect.items():
            val = payload.get(field)
            ok = False
            if isinstance(exp, dict):
                if "equals" in exp:
                    ok = (str(val).strip().lower() == str(exp["equals"]).strip().lower())
                if "contains" in exp:
                    toks = _tokenize(str(val or ""))
                    ok = ok or all(e.lower() in toks for e in exp["contains"])
                if "jaccard_gte" in exp:
                    score = _jaccard(_tokenize(str(val or "")), _tokenize(str(exp.get("text",""))))
                    ok = ok or (score >= float(exp["jaccard_gte"]))
            else:
                ok = (str(val).strip().lower() == str(exp).strip().lower())
            spec_res["checks"].append({"field": field, "ok": bool(ok), "value": val, "expected": exp})
            spec_res["total"] += 1; spec_res["pass"] += int(ok)
        results["by_spec"][spec] = spec_res
    results["macro"] = {
        "accuracy": (sum(v["pass"] for v in results["by_spec"].values()) / max(1, sum(v["total"] for v in results["by_spec"].values())))
    }
    if out_csv:
        p = Path(out_csv); p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["spec","field","ok","value","expected"])
            for spec, s in results["by_spec"].items():
                for c in s["checks"]:
                    w.writerow([spec, c["field"], int(c["ok"]), str(c["value"]), json.dumps(c["expected"], ensure_ascii=False)])
    (Path(outputs_root)/"_offline_eval.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return results
