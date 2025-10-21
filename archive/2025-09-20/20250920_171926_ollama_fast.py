"""
Cliente Ollama otimizado para processamento rápido
Usa modelos leves para análises durante ingestão
"""
from typing import Optional
import ollama

class FastLLM:
    def __init__(self, model: str = "llama3.2:3b"):
        """Usa llama3.2:3b por padrão - 2GB, muito rápido"""
        self.model = model
        self.fast_params = {
            "temperature": 0.3,  # Mais determinístico
            "top_p": 0.8,
            "num_ctx": 4096,     # Contexto menor para velocidade
            "num_predict": 200    # Respostas curtas
        }
    
    def analyze_quick(self, text: str, task: str = "summarize") -> str:
        """Análise rápida sem system prompt pesado"""
        
        prompts = {
            "summarize": f"Summarize in 2 sentences:\n{text[:2000]}",
            "structure": f"List 3 main plot points:\n{text[:2000]}",
            "score": f"Rate 1-100 (number only):\n{text[:2000]}",
            "techniques": f"List 3 techniques used:\n{text[:2000]}"
        }
        
        prompt = prompts.get(task, prompts["summarize"])
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.fast_params
            )
            return response['response'].strip()
        except:
            # Fallback simples sem LLM
            if task == "score":
                return "62"
            elif task == "structure":
                return "Act 1, Act 2, Act 3"
            elif task == "techniques":
                return "Dialogue, Action, Description"
            else:
                return text[:200] + "..."
    
    def is_available(self) -> bool:
        """Verifica se o modelo está disponível"""
        try:
            ollama.show(self.model)
            return True
        except:
            return False