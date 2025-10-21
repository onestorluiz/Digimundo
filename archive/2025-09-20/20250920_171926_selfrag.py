from typing import Dict, Any, List
import yaml
from ..models.ollama_client import OllamaLLM
from ..storage.memory_layers import read_l1_core
from ..config import load_config

_cfg = load_config()
_llm = OllamaLLM()

def selfrag_plan(query: str) -> Dict[str, Any]:
    with open(_cfg.paths.prompts_template, "r", encoding="utf-8") as f:
        T = yaml.safe_load(f)
    plan_prompt = T["selfrag"]["plan"].replace("{query}", query)
    out = _llm.generate(plan_prompt, system=read_l1_core())
    return {"raw": out}

def selfrag_critique(answer: str) -> str:
    with open(_cfg.paths.prompts_template, "r", encoding="utf-8") as f:
        T = yaml.safe_load(f)
    crit = T["selfrag"]["critique"]
    return _llm.generate(crit + "\n\n[DRAFT]\n" + answer, system=read_l1_core())

def cove_questions(draft: str) -> List[str]:
    with open(_cfg.paths.prompts_template, "r", encoding="utf-8") as f:
        T = yaml.safe_load(f)
    q = _llm.generate(T["cove"]["questions"] + "\n\n[DRAFT]\n" + draft)
    return [line.strip("-• ").strip() for line in q.splitlines() if line.strip()]

def cove_answer(questions: List[str], citations: List[str]) -> str:
    with open(_cfg.paths.prompts_template, "r", encoding="utf-8") as f:
        T = yaml.safe_load(f)
    joined = "\n".join(f"- {qq}" for qq in questions)
    return _llm.generate(T["cove"]["answer"] + f"\n\n[PERGUNTAS]\n{joined}\n\n[CITAÇÕES]\n" + "\n".join(citations))
