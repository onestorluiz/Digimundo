#!/usr/bin/env python3
"""
🔌 ADAPTERS - Conectores para sistemas existentes
Permite que todos os sistemas falem com o UNIFIED_SYSTEM
"""

import sys
import json
import sqlite3
from pathlib import Path
from typing import Any, Optional, Dict

# Importa o sistema unificado
try:
    from .UNIFIED_SYSTEM import UnifiedMemorySystem
except ImportError:
    # Para execução direta
    from UNIFIED_SYSTEM import UnifiedMemorySystem

class MemoryAdapters:
    """Adaptadores para conectar diferentes sistemas de memória"""

    def __init__(self):
        self.unified = UnifiedMemorySystem()
        self.base_path = Path('/Users/clubproducoes/Digimundo')

    def adapt_scripturemon_ultimate(self, db_path: Optional[Path] = None):
        """Adapta o sistema minimalista do scripturemon-ultimate"""
        if not db_path:
            db_path = self.base_path / 'scripturemon-ultimate/data/learning/ollama_knowledge.db'

        if not db_path.exists():
            return {"status": "not_found", "insights": 0}

        try:
            conn = sqlite3.connect(db_path)
            insights = conn.execute("SELECT COUNT(*) FROM insights").fetchone()[0]

            # Sincroniza com unified
            rows = conn.execute("SELECT * FROM insights LIMIT 10").fetchall()
            for row in rows:
                self.unified.remember(
                    f"Insight from scripturemon: {row[1] if len(row) > 1 else 'data'}",
                    'scripturemon_insights'
                )

            conn.close()
            return {"status": "synced", "insights": insights}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def adapt_crystal_memory(self):
        """Adapta o sistema Crystal Memory"""
        crystal_path = self.base_path / 'claude_code/memory/crystal_memory.json'

        if crystal_path.exists():
            with open(crystal_path) as f:
                data = json.load(f)

            # Sincroniza compliance e patterns
            if 'compliance' in data:
                self.unified.remember(
                    f"Crystal compliance: {data['compliance']}",
                    'crystal_metrics'
                )

            return {"status": "synced", "data": data}
        return {"status": "not_found"}

    def adapt_genjutsu(self):
        """Conecta com o Genjutsu para detecção de compactação"""
        import subprocess

        try:
            # Verifica se Genjutsu está rodando
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )

            genjutsu_running = "GENJUTSU" in result.stdout

            if genjutsu_running:
                # Salva estado no unified
                self.unified.remember(
                    "Genjutsu ATIVO - Proteção contra compactação",
                    'system_status'
                )
                return {"status": "active", "protection": True}
            else:
                self.unified.remember(
                    "Genjutsu INATIVO - Sistema vulnerável",
                    'system_status'
                )
                return {"status": "inactive", "protection": False}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def adapt_ollama_api(self):
        """Adapta chamadas para API do Ollama (não CLI!)"""
        import requests

        def generate(prompt: str, model: str = "mixtral-cpu-force:latest") -> str:
            """USA API, NÃO SUBPROCESS!"""
            try:
                response = requests.post(
                    "http://127.0.0.1:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json().get("response", "")

                    # Salva interação
                    self.unified.remember(
                        f"Ollama API: {prompt[:50]}... -> {result[:50]}...",
                        'ollama_interactions'
                    )

                    return result

            except Exception as e:
                self.unified.remember(
                    f"Ollama API error: {e}",
                    'system_errors'
                )
                return f"Error: {e}"

        return generate

    def sync_all(self):
        """Sincroniza todos os sistemas"""
        results = {
            'scripturemon': self.adapt_scripturemon_ultimate(),
            'crystal': self.adapt_crystal_memory(),
            'genjutsu': self.adapt_genjutsu(),
            'timestamp': self.unified.get_timestamp() if hasattr(self.unified, 'get_timestamp') else 'now'
        }

        # Salva resultado da sincronização
        self.unified.remember(
            f"Full sync completed: {json.dumps(results)}",
            'sync_logs'
        )

        return results

# Singleton para uso global
_adapters = None

def get_adapters() -> MemoryAdapters:
    """Retorna instância única dos adapters"""
    global _adapters
    if _adapters is None:
        _adapters = MemoryAdapters()
    return _adapters

if __name__ == "__main__":
    # Teste de sincronização
    adapters = get_adapters()
    print("🔄 Sincronizando todos os sistemas...")
    results = adapters.sync_all()
    print(json.dumps(results, indent=2))
    print("✅ Sincronização completa!")