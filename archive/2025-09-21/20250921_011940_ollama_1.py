# Stub seguro de Ollama: não faz rede; retorna eco estruturado.
from __future__ import annotations
import os, json, time
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class OllamaResponse:
    model: str
    prompt_tokens: int
    completion: str
    latency_ms: int

def discover_models() -> list[str]:
    # Sem rede; pode ler config no futuro
    return ["mock-model"]

def generate(prompt: str, model: str = "mock-model", temperature: float = 0.2, max_tokens: int = 256, timeout: int = 30) -> OllamaResponse:
    t0 = time.time()
    # Simples "compleção" determinística para testes locais
    comp = (prompt.strip()[:max_tokens])[::-1]
    dt = int((time.time() - t0) * 1000)
    return OllamaResponse(model=model, prompt_tokens=len(prompt.split()), completion=comp, latency_ms=dt)
