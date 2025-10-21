from typing import Dict, Any
from .retrieval.hybrid import HybridRetriever
from .retrieval.context_builder import pack_context
from .models.ollama_client import OllamaLLM
from .storage.memory_layers import read_l1_core
from .processing.selfrag import selfrag_critique, cove_questions
from .config import load_config

_cfg = load_config()
_llm = OllamaLLM()

PROMPT_ANSWER = """Responda a pergunta usando APENAS o contexto a seguir.
Regras:
- Cite os trechos com [cit:<id>|p.:<page>]
- Se faltar evidência, diga explicitamente o que falta.
- Seja técnico e direto.

{context}

[PERGUNTA]
{query}
"""

def answer_with_rag(query: str) -> Dict[str, Any]:
    retr = HybridRetriever()
    ranked = retr.search(query)
    context = pack_context(query, ranked, max_tokens=_cfg.ollama.num_ctx, reserve_for_output=2048)
    draft = _llm.generate(PROMPT_ANSWER.format(context=context, query=query), system=read_l1_core())
    critique = selfrag_critique(draft)
    qs = cove_questions(draft)
    return {"draft": draft, "critique": critique, "verification_questions": qs, "citations": [r["id"] for r in ranked[:5]]}
