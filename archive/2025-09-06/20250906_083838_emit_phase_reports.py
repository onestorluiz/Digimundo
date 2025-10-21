#!/usr/bin/env python3
"""
V3.1 DELTA — Emite relatórios por fase a partir do agregado (full_verification.json)
e corrige nomes inconsistentes de backup em JSONs existentes (ex.: phase_03_rag.json).

Uso:
  python tools/fix_v3/emit_phase_reports.py --in reports/fix_v3/full_verification.json --out reports/fix_v3
"""
import argparse, json, sys
from pathlib import Path

PHASE_MAP = {
    "backup": "phase_08_backup.json",
    "memory": "phase_06_memory.json",
    "mixer":  "phase_07_mixer.json",
    "scoring":"phase_05_scoring.json",
}

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[emit_phase_reports] ERRO ao ler {path}: {e}", file=sys.stderr)
        return None

def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[emit_phase_reports] gravado: {path}")

def emit_from_full(full_path: Path, out_dir: Path):
    full = load_json(full_path)
    if not full:
        # Try looking at 'phases' key instead of 'checks'
        print(f"[emit_phase_reports] tentando campo 'phases' ao invés de 'checks'", file=sys.stderr)
    
    if not full or ("checks" not in full and "phases" not in full):
        print(f"[emit_phase_reports] nada a emitir de {full_path}", file=sys.stderr)
        return 1
    
    # Try both 'checks' and 'phases' keys
    checks = full.get("checks") or full.get("phases", {})
    
    for key, fname in PHASE_MAP.items():
        if key in checks:
            save_json(out_dir / fname, checks[key])
    return 0

def fix_rag_backup_name(rag_json_path: Path):
    """Corrige campo 'backup' inconsistente em phase_03_rag.json, se existir."""
    if not rag_json_path.exists():
        return 0
    data = load_json(rag_json_path)
    if not data:
        return 1
    backup = data.get("backup")
    if isinstance(backup, str) and "v3_telepathy.zip" in backup:
        data["backup"] = backup.replace("v3_telepathy.zip", "v3_rag.zip")
        save_json(rag_json_path, data)
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=False, default="reports/fix_v3/full_verification.json")
    ap.add_argument("--out", dest="out", required=False, default="reports/fix_v3")
    args = ap.parse_args()
    inp = Path(args.inp)
    out = Path(args.out)

    rc1 = emit_from_full(inp, out)
    rc2 = fix_rag_backup_name(out / "phase_03_rag.json")
    return rc1 or rc2

if __name__ == "__main__":
    import sys
    sys.exit(main())