
import json
from pathlib import Path
from dataclasses import dataclass
@dataclass
class Specialist:
    id: str
    phase: str
    enabled: bool
    deps: list[str]
    prompt_path: str
    namespaces: list[str] | None = None
    mode: str = "llm"
def load_specialists(dir_path: str) -> list['Specialist']:
    res=[]
    for man in Path(dir_path).glob("*/manifest.json"):
        m = json.loads(man.read_text(encoding="utf-8"))
        res.append(Specialist(
            id=m["id"],
            phase=m.get("phase","analysis"),
            enabled=bool(m.get("enabled", True)),
            deps=m.get("deps", []),
            prompt_path=str(man.parent / m.get("prompt","prompt.md")),
            namespaces=m.get("namespaces", []),
            mode=m.get("mode","llm")
        ))
    return sorted(res, key=lambda s: s.id)
