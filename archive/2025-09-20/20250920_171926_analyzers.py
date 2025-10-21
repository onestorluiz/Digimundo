from typing import Dict, List, Any
import json, yaml
from ..models.ollama_client import OllamaLLM
from ..storage.memory_layers import read_l1_core
from ..config import load_config

_cfg = load_config()
_llm = OllamaLLM()

def _load_templates():
    with open(_cfg.paths.prompts_template, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

_TPL = _load_templates()

def detect_structure(text: str) -> Dict[str, Any]:
    prompt = _TPL["analysis_prompts"]["detect_structure"] + "\n\n" + text[:6000]
    out = _llm.generate(prompt, system=read_l1_core())
    try:
        return json.loads(out)
    except:
        return {"raw": out}

def extract_techniques(text: str) -> List[Dict[str, Any]]:
    prompt = _TPL["analysis_prompts"]["extract_techniques"] + "\n\n" + text[:6000]
    out = _llm.generate(prompt, system=read_l1_core())
    try:
        data = json.loads(out)
        if isinstance(data, list):
            return data
    except:
        pass
    return [{"raw": out}]

def brutal_score(text: str) -> Dict[str, Any]:
    prompt = _TPL["analysis_prompts"]["brutal_score"] + "\n\n" + text[:6000]
    out = _llm.generate(prompt, system=read_l1_core())
    try:
        return json.loads(out)
    except:
        return {"raw": out}

def compare_to_masters(snippet: str) -> Dict[str, Any]:
    prompt = _TPL["analysis_prompts"]["compare_to_masters"] + "\n\nTrecho:\n" + snippet[:4000]
    out = _llm.generate(prompt, system=read_l1_core())
    try:
        return json.loads(out)
    except:
        return {"raw": out}
