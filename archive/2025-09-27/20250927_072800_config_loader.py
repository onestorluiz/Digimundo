
import json, os
from pathlib import Path
DEFAULTS_PATH = Path(__file__).resolve().parent.parent / "config" / "defaults.json"
def load_config(overrides: dict | None = None) -> dict:
    with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
        base = json.load(f)
    for k, v in os.environ.items():
        if k.startswith("SC_"):
            base[k[3:].lower()] = v
    if overrides: base.update(overrides)
    repo_root = Path(__file__).resolve().parents[1]
    base["paths"] = {
        "repo": str(repo_root),
        "data": str(repo_root / "data"),
        "outputs": str(repo_root / base.get("outputs_dir","outputs")),
        "specialists": str(repo_root / base.get("specialists_dir","specialists")),
        "config": str(repo_root / "config")
    }
    return base
