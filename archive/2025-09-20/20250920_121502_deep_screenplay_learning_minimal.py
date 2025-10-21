#!/usr/bin/env python3
"""
🧠 DEEP SCREENPLAY LEARNING - Versão Minimalista
Processa livros + roteiros com 128K tokens
"""

import sys
import json
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.unified_memory_system import get_unified_memory, MemoryType
from src.core.screenplay_library import get_screenplay_library

class DeepLearning:
    def __init__(self):
        self.memory = get_unified_memory()
        self.library = get_screenplay_library()
        self.model = "mixtral-dedicated-q5"

        # Config corrigida (24 threads como documentado)
        self.config = {
            'num_ctx': 131072,     # 128K tokens
            'num_thread': 24,      # CORRIGIDO: 24 cores
            'num_gpu': -1,         # Auto-detect
            'num_batch': 4096,     # CORRIGIDO: como documentado
            'temperature': 0.3
        }

    def analyze(self, book_path: Path, screenplay_title: str):
        """Análise direta e simples"""

        # Ler conteúdos
        book = book_path.read_text(encoding='utf-8', errors='ignore')[:320000]
        screenplay = self.library.get_screenplay(screenplay_title)

        if not screenplay:
            return None

        screenplay = screenplay[:120000]

        # Prompt simplificado
        prompt = f"""BOOK: {book[:80000]}

SCREENPLAY ({screenplay_title}): {screenplay[:30000]}

Extract 10 key concepts from book with examples from screenplay.
Output JSON: {{"concepts": [{{"name": "...", "theory": "...", "example": "..."}}]}}"""

        # Chamar ollama direto
        try:
            import ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=self.config,
                stream=False
            )

            # Parse simples
            result = response.get('response', '{}')
            if '{' in result and '}' in result:
                start = result.find('{')
                end = result.rfind('}') + 1
                data = json.loads(result[start:end])

                # Salvar direto
                for c in data.get('concepts', []):
                    self.memory.store(
                        MemoryType.KNOWLEDGE,
                        f"concept:{c.get('name', 'unknown')}",
                        c,
                        confidence=0.9,
                        source='deep_learning'
                    )

                return data

        except Exception as e:
            print(f"Erro: {e}")
            return None

def main():
    """Interface simples"""
    dl = DeepLearning()

    # Análises prioritárias
    books = [
        ("Save The Cat.txt", "Inception"),
        ("S•T• O • R • Y.txt", "The Matrix"),
        ("The Anatomy of Story_ 22 Steps to Becoming a Master  -  John Truby.txt", "Pulp Fiction")
    ]

    teoria = Path("digilibrary/BIBLIOTECA_ROTEIROS/teoria")

    for book, screenplay in books:
        book_path = teoria / book
        if book_path.exists():
            print(f"\n📚 {book[:20]}... + 🎬 {screenplay}")
            result = dl.analyze(book_path, screenplay)
            if result:
                print(f"✅ {len(result.get('concepts', []))} conceitos extraídos")
            time.sleep(2)

if __name__ == "__main__":
    main()