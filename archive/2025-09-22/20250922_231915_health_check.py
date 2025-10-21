#!/usr/bin/env python3
"""
Health Check Contínuo com Detecção de Redundância
"""

import os
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime

class HealthCheck:
    def __init__(self):
        self.base = Path(__file__).parent.parent
        self.last_check = time.time()
        self.redundancy_cache = {}

    def check_genjutsu(self):
        """Verifica se Genjutsu está ativo"""
        import subprocess
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
            return 'GENJUTSU' in result.stdout
        except:
            return False

    def check_memory(self):
        """Verifica integridade da memória"""
        db_path = self.base / 'data' / 'memory.db'
        return db_path.exists() and db_path.stat().st_size > 0

    def check_redundancy(self):
        """Detecta arquivos redundantes"""
        redundant = []
        seen_hashes = {}

        # Verifica todos os arquivos .md e .py
        for pattern in ['*.md', '*.py', '*/*.md', '*/*.py']:
            for file_path in self.base.glob(pattern):
                if file_path.is_file():
                    # Calcula hash do conteúdo
                    content = file_path.read_bytes()
                    file_hash = hashlib.md5(content).hexdigest()

                    if file_hash in seen_hashes:
                        redundant.append({
                            'duplicate': str(file_path),
                            'original': seen_hashes[file_hash]
                        })
                    else:
                        seen_hashes[file_hash] = str(file_path)

        return redundant

    def check_harmony(self):
        """Calcula harmonia do sistema"""
        score = 95  # Base após limpeza

        # Penaliza por redundâncias
        redundant = self.check_redundancy()
        if redundant:
            score -= len(redundant) * 2

        # Bonus por Genjutsu ativo
        if self.check_genjutsu():
            score += 2

        # Bonus por memória íntegra
        if self.check_memory():
            score += 2

        return min(score, 100)

    def cleanup_archive(self):
        """Remove arquivos > 30 dias do archive"""
        archive = Path('/Users/clubproducoes/Digimundo/archive')
        if archive.exists():
            import subprocess
            subprocess.run(['find', str(archive), '-mtime', '+30', '-delete'])

    def run_continuous(self, interval=300):
        """Roda continuamente a cada interval segundos"""
        while True:
            print(f"\n🔍 Health Check - {datetime.now()}")

            # Checks
            genjutsu = self.check_genjutsu()
            memory = self.check_memory()
            redundancy = self.check_redundancy()
            harmony = self.check_harmony()

            # Report
            print(f"  Genjutsu: {'✅' if genjutsu else '❌'}")
            print(f"  Memory: {'✅' if memory else '❌'}")
            print(f"  Redundâncias: {len(redundancy)}")
            print(f"  Harmonia: {harmony}%")

            # Ações
            if redundancy:
                print("  ⚠️ Arquivos redundantes detectados:")
                for r in redundancy[:3]:  # Mostra até 3
                    print(f"    - {r['duplicate']}")

            if harmony < 90:
                print("  🚨 Harmonia baixa! Verificar sistema.")

            # Cleanup periódico (1x por dia)
            if time.time() - self.last_check > 86400:
                self.cleanup_archive()
                self.last_check = time.time()
                print("  🧹 Archive limpo (arquivos > 30 dias)")

            # Aguarda próximo check
            time.sleep(interval)

if __name__ == '__main__':
    health = HealthCheck()

    # Check único
    print("🏥 Health Check Único")
    print(f"  Harmonia: {health.check_harmony()}%")

    redundant = health.check_redundancy()
    if redundant:
        print(f"  ⚠️ {len(redundant)} redundâncias encontradas")

    # Para rodar contínuo, descomente:
    # health.run_continuous(300)  # A cada 5 minutos