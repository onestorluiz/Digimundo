"""Fallback manager para quando Ollama está offline"""
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

class OllamaFallback:

    def __init__(self):
        self.cache_dir = Path('data/ollama_cache')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.responses = {'default': 'Sistema operando em modo offline. Usando respostas em cache.', 'status': 'Ollama offline - modo cache ativo', 'search': 'Busca local disponível apenas'}

    def get_cached_response(self, prompt: str) -> str:
        """Retorna resposta em cache ou padrão"""
        cache_file = self.cache_dir / f'{hash(prompt)}.json'
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)['response']
        return self.responses.get('default', 'Modo offline ativo')

    def save_response(self, prompt: str, response: str):
        """Salva resposta para uso futuro"""
        cache_file = self.cache_dir / f'{hash(prompt)}.json'
        with open(cache_file, 'w') as f:
            json.dump({'prompt': prompt, 'response': response, 'time': time.time()}, f)
fallback_manager = OllamaFallback()