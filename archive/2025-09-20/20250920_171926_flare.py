from typing import Dict, Any
from ..models.ollama_client import OllamaLLM
_llm = OllamaLLM()

def flare_iterative_answer(draft: str) -> Dict[str, Any]:
    plan = _llm.generate("Você verá um rascunho de resposta. Proponha 1-3 buscas ativas para antecipar conteúdos que podem faltar. Saída: lista simples.\n\nRascunho:\n" + draft)
    return {"flare_queries": [q.strip("-• ") for q in plan.splitlines() if q.strip()]}
