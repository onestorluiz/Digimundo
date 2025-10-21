#!/usr/bin/env python3
"""
Teste do Mixtral com contexto expandido
"""
from ollama_with_memory import OllamaWithMemory

# Usar o novo modelo 128K
analyzer = OllamaWithMemory(model="scripturemon-mixtral-128k")

script = """
INT. LABORATORY - DAY
AURORA (V.O.)
Why did you create me?

DR. SARAH CHEN hesitates.
"""

result = analyzer.analyze_with_context(script)
print(f"Resultado: {result.get('metadata', {})}")
