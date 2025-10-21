
from dataclasses import dataclass
import subprocess, json, time, urllib.request, re
@dataclass
class LLMConfig:
    backend: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 2048
    timeout: int = 60
    endpoint: str | None = None
class LLMAdapter:
    def __init__(self, cfg: LLMConfig): self.cfg = cfg
    def _retry(self, fn, attempts=3, base=0.5):
        for i in range(attempts):
            try: return fn()
            except Exception:
                if i == attempts - 1: raise
                time.sleep(base * (2 ** i))
    def generate(self, prompt: str) -> str:
        return self._retry(lambda: self._generate_once(prompt))
    def _generate_once(self, prompt: str) -> str:
        if self.cfg.backend == "mock":
            spec = re.search(r"SPECIALIST_ID:\s*([a-zA-Z0-9_]+)", prompt)
            spec_id = spec.group(1) if spec else "generic"
            dr = re.search(r"dialogue_ratio:([0-9.]+)", prompt); dialogue_ratio = float(dr.group(1)) if dr else 0.5
            evidence = {"script_offset": "p1:l1-10", "rag_doc_id": "beat:dyn_1_1", "baseline_metric": f"dialogue_ratio:{dialogue_ratio:.2f}"}
            if spec_id == "pacing":
                pace = "fast" if dialogue_ratio < 0.3 else ("medium" if dialogue_ratio < 0.6 else "slow")
                payload = {"pace": pace, "dialogue_ratio": dialogue_ratio}
            elif spec_id == "logline":
                payload = {"logline": "Um protagonista enfrenta um conflito que mudará seu destino.", "genre": "Drama"}
            elif spec_id == "theme":
                payload = {"primary_theme": "memória e responsabilidade", "motifs": ["santuário","sacrifício","aliança"]}
            elif spec_id == "market":
                payload = {"audience": "adulto jovem a adulto; drama de alto conceito", "comparables": ["A Chegada","Mr. Robot"]}
            else:
                payload = {"analysis": "mock"}
            return json.dumps({"quality": 0.90, "evidence": evidence, "payload": payload}, ensure_ascii=False)
        elif self.cfg.backend == "ollama_cli":
            p = subprocess.run(["ollama","run", self.cfg.model, prompt], capture_output=True, text=True, timeout=self.cfg.timeout)
            if p.returncode != 0: raise RuntimeError(p.stderr.strip())
            return p.stdout.strip()
        elif self.cfg.backend == "http":
            assert self.cfg.endpoint, "endpoint HTTP requerido"
            body = json.dumps({"model": self.cfg.model, "prompt": prompt, "temperature": self.cfg.temperature}).encode("utf-8")
            req = urllib.request.Request(self.cfg.endpoint, data=body, headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=self.cfg.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("text") or data.get("content") or data["choices"][0]["message"]["content"]
        else:
            raise ValueError("backend desconhecido")
