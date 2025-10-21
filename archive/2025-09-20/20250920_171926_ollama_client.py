from typing import List, Optional, Dict, Any
from ollama import Client
from ..config import load_config

_cfg = load_config()

class OllamaLLM:
    def __init__(self, model: Optional[str] = None):
        self.client = Client(host='http://localhost:11434')
        self.model = model or _cfg.ollama.model
        self.params = {
            "temperature": _cfg.ollama.temperature,
            "top_p": _cfg.ollama.top_p,
            "repeat_penalty": _cfg.ollama.repeat_penalty,
            "num_ctx": _cfg.ollama.num_ctx
        }

    def generate(self, prompt: str, system: Optional[str] = None, stream: bool = False) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.client.chat(model=self.model, messages=messages, options=self.params, stream=stream)
        if stream:
            out = []
            for chunk in resp:
                if "message" in chunk and "content" in chunk["message"]:
                    out.append(chunk["message"]["content"])
            return "".join(out)
        else:
            return resp["message"]["content"]

    def template(self, tpl: str, **kwargs):
        return tpl.format(**kwargs)
