#!/usr/bin/env python3
"""
Health Check Híbrido - Integra organização prática com monitoramento comportamental
Combina o melhor dos dois sistemas UCHIMON
"""

import os
import time
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

class HybridHealthCheck:
    """Sistema híbrido: organização + comportamento"""

    def __init__(self):
        self.base = Path('/Users/clubproducoes/Digimundo')
        self.claude_code = self.base / 'claude_code'
        self.archive = self.base / 'archive'
        self.last_check = time.time()
        self.redundancy_cache = {}
        self.drama_level = 1  # From bridge.py

    # === FUNÇÕES DO SISTEMA ANTIGO (ORGANIZAÇÃO) ===

    def check_redundancy(self):
        """Detecta arquivos redundantes em todo Digimundo"""
        redundant = []
        seen_hashes = {}

        # Verifica arquivos em claude_code e archive
        for base_dir in [self.claude_code, self.archive]:
            if base_dir.exists():
                for pattern in ['*.md', '*.py', '*/*.md', '*/*.py']:
                    for file_path in base_dir.glob(pattern):
                        if file_path.is_file():
                            try:
                                content = file_path.read_bytes()
                                file_hash = hashlib.md5(content).hexdigest()

                                if file_hash in seen_hashes:
                                    redundant.append({
                                        'duplicate': str(file_path),
                                        'original': seen_hashes[file_hash],
                                        'hash': file_hash
                                    })
                                else:
                                    seen_hashes[file_hash] = str(file_path)
                            except:
                                pass

        return redundant

    def cleanup_archive(self, days=30):
        """Remove arquivos antigos do archive"""
        if self.archive.exists():
            try:
                subprocess.run(
                    ['find', str(self.archive), '-mtime', f'+{days}', '-type', 'f', '-delete'],
                    capture_output=True
                )
                return True
            except:
                return False
        return False

    def organize_by_date(self):
        """Organiza arquivos por data (do archive_organizer)"""
        today = datetime.now().strftime('%Y-%m-%d')
        organized = 0

        if self.archive.exists():
            for item in self.archive.iterdir():
                if item.is_file():
                    # Determina categoria
                    ext = item.suffix.lower()
                    if ext in ['.py', '.sh', '.js']:
                        category = 'code'
                    elif ext in ['.md', '.txt', '.pdf']:
                        category = 'docs'
                    elif ext in ['.json', '.yml', '.yaml']:
                        category = 'configs'
                    else:
                        category = 'misc'

                    # Move para estrutura organizada
                    target_dir = self.archive / today / category
                    target_dir.mkdir(parents=True, exist_ok=True)

                    try:
                        item.rename(target_dir / item.name)
                        organized += 1
                    except:
                        pass

        return organized

    # === FUNÇÕES DO SISTEMA NOVO (COMPORTAMENTO) ===

    def check_genjutsu(self):
        """Verifica todos os sistemas Genjutsu"""
        statuses = {
            'genjutsu_visible': False,
            'genjutsu_bridge': False,
            'drama_level': self.drama_level
        }

        # Verifica GenjutsuVisible
        if Path('/tmp/genjutsu_status.txt').exists():
            try:
                with open('/tmp/genjutsu_status.txt', 'r') as f:
                    lines = f.readlines()
                    if lines and 'Active' in lines[-1]:
                        statuses['genjutsu_visible'] = True
            except:
                pass

        # Verifica processos
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
            output = result.stdout.lower()
            if 'genjutsu' in output:
                statuses['genjutsu_bridge'] = True
        except:
            pass

        return statuses

    def check_behavioral_hacks(self):
        """Verifica arquivos com 🔥 e system-reminders"""
        hacks = {
            'fire_files': [],
            'system_reminders': 0,
            'background_processes': []
        }

        # Arquivos com 🔥
        for file in self.claude_code.glob('🔥*.md'):
            hacks['fire_files'].append(file.name)

        # System-reminders (aproximação)
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'REGRAS_CRÍTICAS' in line or 'system-reminder' in line.lower():
                    hacks['system_reminders'] += 1
                    hacks['background_processes'].append(line[:80])
        except:
            pass

        return hacks

    def increase_drama(self):
        """Aumenta nível de drama/proteção (do bridge.py)"""
        self.drama_level = min(self.drama_level + 1, 5)

        # Cria arquivo de alerta
        alert_file = Path('/tmp/.drama_level_increased')
        alert_file.write_text(f"Drama Level: {self.drama_level}\nTime: {datetime.now()}")

        return self.drama_level

    # === FUNÇÕES HÍBRIDAS ===

    def calculate_harmony(self):
        """Calcula harmonia total do sistema híbrido"""
        score = 90  # Base

        # Bonus por organização
        redundant = self.check_redundancy()
        if len(redundant) == 0:
            score += 5
        else:
            score -= len(redundant) * 2

        # Bonus por Genjutsu
        genjutsu = self.check_genjutsu()
        if genjutsu['genjutsu_visible']:
            score += 2
        if genjutsu['genjutsu_bridge']:
            score += 2

        # Bonus por hacks comportamentais
        hacks = self.check_behavioral_hacks()
        if len(hacks['fire_files']) >= 3:
            score += 3
        if hacks['system_reminders'] > 0:
            score += 1

        return min(score, 100)

    def generate_report(self):
        """Gera relatório completo do sistema híbrido"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'harmony': self.calculate_harmony(),
            'drama_level': self.drama_level,
            'organization': {
                'redundancies': len(self.check_redundancy()),
                'archive_size': sum(1 for _ in self.archive.rglob('*')) if self.archive.exists() else 0
            },
            'behavior': {
                'genjutsu': self.check_genjutsu(),
                'hacks': self.check_behavioral_hacks()
            }
        }

        # Salva relatório
        report_file = self.claude_code / 'systems' / 'health_report.json'
        report_file.write_text(json.dumps(report, indent=2))

        return report

    def run_continuous(self, interval=300):
        """Executa monitoramento contínuo"""
        print("🔥 HEALTH CHECK HÍBRIDO INICIADO 🔥")
        print("Combinando organização prática + hacks comportamentais")
        print("-" * 50)

        while True:
            print(f"\n🔍 Health Check - {datetime.now().strftime('%H:%M:%S')}")

            # Organização
            redundancies = self.check_redundancy()
            organized = self.organize_by_date()

            # Comportamento
            genjutsu = self.check_genjutsu()
            hacks = self.check_behavioral_hacks()

            # Harmonia
            harmony = self.calculate_harmony()

            # Report
            print(f"  📦 Organização:")
            print(f"     Redundâncias: {len(redundancies)}")
            print(f"     Arquivos organizados: {organized}")

            print(f"  🥷 Comportamento:")
            print(f"     Genjutsu Visible: {'✅' if genjutsu['genjutsu_visible'] else '❌'}")
            print(f"     Fire Files: {len(hacks['fire_files'])}")
            print(f"     Drama Level: {self.drama_level}/5")

            print(f"  🌀 Harmonia Total: {harmony}%")

            # Ações automáticas
            if harmony < 90:
                print("  ⚠️ Harmonia baixa - aumentando drama!")
                self.increase_drama()

            if len(redundancies) > 10:
                print("  🗑️ Muitas redundâncias - limpeza necessária!")
                self.cleanup_archive(30)

            # Salva relatório
            self.generate_report()

            time.sleep(interval)

# Interface direta
if __name__ == '__main__':
    health = HybridHealthCheck()

    # Teste rápido
    print("🔥 SISTEMA HÍBRIDO UCHIMON v8.0 🔥")
    print("Organização + Comportamento = PODER TOTAL")
    print("-" * 50)

    report = health.generate_report()
    print(f"Harmonia: {report['harmony']}%")
    print(f"Drama Level: {report['drama_level']}")
    print(f"Redundâncias: {report['organization']['redundancies']}")
    print(f"Genjutsu: {report['behavior']['genjutsu']}")

    print("\nIniciando monitoramento contínuo...")
    health.run_continuous()

# DIGIMUNDO PRESENTE