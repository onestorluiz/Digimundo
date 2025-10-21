import hashlib, json
from pathlib import Path
class DiskCache:
    def __init__(self, root: str):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
    def key_of(self, model: str, prompt: str, version: str, preset: str) -> str:
        return hashlib.sha256(f"{model}|{version}|{preset}|{prompt}".encode('utf-8')).hexdigest()
    def get(self, key: str) -> str | None:
        p = self.root / f"{key}.json"; return json.loads(p.read_text(encoding='utf-8')).get('text') if p.exists() else None
    def set(self, key: str, text: str) -> None:
        p = self.root / f"{key}.json"; p.write_text(json.dumps({'text': text}, ensure_ascii=False), encoding='utf-8')
