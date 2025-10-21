from ..models.ollama_client import OllamaLLM
_llm = OllamaLLM()

def hyde_expand_query(query: str) -> str:
    prompt = f"Crie um pequeno documento hipotético (100-150 palavras) que provavelmente conteria a resposta para: '{query}'. Foque em detalhes técnicos e termos de roteiro. Português."
    return _llm.generate(prompt)
