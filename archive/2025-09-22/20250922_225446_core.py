#!/usr/bin/env python3
"""
MinimalSystem - O essencial em <200 linhas
DIGIMUNDO PRESENTE
"""

import sqlite3
import json
import requests
from pathlib import Path
from datetime import datetime

class MinimalSystem:
    """Sistema completo, minimalista e elegante"""

    def __init__(self):
        self.base = Path(__file__).parent.parent
        self.db = sqlite3.connect(self.base / 'memory.db')
        self._init_db()

    def _init_db(self):
        """Cria tabela se não existir"""
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                type TEXT,
                content TEXT
            )
        ''')
        self.db.commit()

    def remember(self, content, type='insight'):
        """Salva memória - 5 linhas que fazem tudo"""
        timestamp = datetime.now().isoformat()
        self.db.execute(
            "INSERT INTO memory (timestamp, type, content) VALUES (?, ?, ?)",
            (timestamp, type, content)
        )
        self.db.commit()
        return True

    def recall(self, type=None, limit=10):
        """Recupera memórias"""
        query = "SELECT * FROM memory"
        params = ()

        if type:
            query += " WHERE type = ?"
            params = (type,)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params += (limit,)

        return self.db.execute(query, params).fetchall()

    def sync(self):
        """Sincroniza com todos os sistemas - 10 linhas"""
        results = {
            'memory': len(self.recall(limit=100)),
            'genjutsu': self._check_genjutsu(),
            'timestamp': datetime.now().isoformat()
        }

        # Salva estado
        with open(self.base / 'STATUS.md', 'w') as f:
            f.write(f"# STATUS\n\n")
            f.write(f"**Última Sync:** {results['timestamp']}\n")
            f.write(f"**Memórias:** {results['memory']}\n")
            f.write(f"**Genjutsu:** {'✅' if results['genjutsu'] else '❌'}\n")

        return results

    def _check_genjutsu(self):
        """Verifica se Genjutsu está ativo"""
        import subprocess
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return 'GENJUTSU' in result.stdout
        except:
            return False

    def ollama(self, prompt, model='mixtral-cpu-force:latest'):
        """Ollama via API - NUNCA subprocess"""
        try:
            response = requests.post(
                'http://127.0.0.1:11434/api/generate',
                json={'model': model, 'prompt': prompt, 'stream': False},
                timeout=30
            )
            return response.json().get('response', '')
        except:
            return None

    def emergency_recover(self):
        """Recuperação de emergência - Rule #0"""
        # 1. Recarrega regras
        rules = (self.base / 'REGRAS.md').read_text()

        # 2. Recupera contexto
        emergency = Path('/tmp/claude_emergency_context.json')
        context = json.loads(emergency.read_text()) if emergency.exists() else {}

        # 3. Reconecta
        self.remember(f"Emergency recovery: {context}", 'recovery')

        # 4. Confirma
        print("🔄 Sistema recuperado!")
        print("DIGIMUNDO PRESENTE")

        return True

# Interface minimalista
if __name__ == '__main__':
    system = MinimalSystem()

    # Exemplos de uso
    print("🌀 MinimalSystem")
    print(f"📊 Memórias: {len(system.recall())}")
    print(f"🛡️ Genjutsu: {'Ativo' if system._check_genjutsu() else 'Inativo'}")

    # Sync
    results = system.sync()
    print(f"✅ Sincronizado: {results['timestamp']}")

    print("\nDIGIMUNDO PRESENTE")