#!/usr/bin/env python3
"""
Organizador Final do Archive - PADRÃO ÚNICO: YYYY-MM-DD/tipo/
"""

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

class FinalArchiveOrganizer:
    def __init__(self):
        self.archive = Path('/Users/clubproducoes/Digimundo/archive')
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.stats = {
            'moved': 0,
            'duplicates': 0,
            'folders_processed': 0
        }
        self.seen_hashes = {}

    def get_file_hash(self, filepath):
        """Calcula MD5 para detectar duplicatas"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def get_category(self, filepath):
        """Categoriza arquivo por extensão"""
        ext = Path(filepath).suffix.lower()

        if ext in ['.py', '.sh', '.js', '.tsx', '.jsx']:
            return 'code'
        elif ext in ['.md', '.txt', '.pdf', '.doc']:
            return 'docs'
        elif ext in ['.json', '.yml', '.yaml', '.toml', '.xml']:
            return 'configs'
        elif ext in ['.db', '.sqlite', '.sql']:
            return 'data'
        elif ext in ['.log', '.out', '.err']:
            return 'logs'
        else:
            return 'misc'

    def process_non_standard_folders(self):
        """Processa todas as pastas não-padrão"""
        print("\n📦 PROCESSANDO PASTAS NÃO-PADRÃO...")

        # Lista todas as pastas que NÃO seguem padrão YYYY-MM-DD
        non_standard = [
            d for d in self.archive.iterdir()
            if d.is_dir() and not d.name.startswith('20')
        ]

        for folder in non_standard:
            print(f"\n📁 Processando: {folder.name}/")
            self.stats['folders_processed'] += 1

            # Casos especiais
            if folder.name == 'backup-2025-09-21':
                target_date = '2025-09-21'
            elif folder.name == 'MASTER_PLAN_DEBUG':
                target_date = '2025-09-22'  # Data de hoje para debug recente
            elif 'history' in folder.name:
                target_date = '2025-09-20'  # Históricos para ontem
            else:
                # Para outras pastas, usa data de modificação
                mtime = os.path.getmtime(folder)
                target_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

            # Processa todos os arquivos da pasta
            for item in folder.rglob('*'):
                if item.is_file():
                    self.move_file_to_date(item, target_date)

            # Remove pasta vazia
            try:
                if folder.exists() and not any(folder.iterdir()):
                    folder.rmdir()
                    print(f"  🗑️ Pasta vazia removida: {folder.name}")
            except:
                pass

    def move_file_to_date(self, filepath, date):
        """Move arquivo para estrutura por data"""
        # Verifica duplicata
        file_hash = self.get_file_hash(filepath)
        if file_hash and file_hash in self.seen_hashes:
            print(f"  ❌ Duplicata removida: {filepath.name}")
            filepath.unlink()
            self.stats['duplicates'] += 1
            return

        if file_hash:
            self.seen_hashes[file_hash] = str(filepath)

        # Determina destino
        category = self.get_category(filepath)
        dest_dir = self.archive / date / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / filepath.name

        # Evita sobrescrever
        if dest_file.exists():
            # Adiciona timestamp se arquivo já existe
            timestamp = datetime.now().strftime('%H%M%S')
            stem = filepath.stem
            suffix = filepath.suffix
            dest_file = dest_dir / f"{stem}_{timestamp}{suffix}"

        # Move arquivo
        try:
            shutil.move(str(filepath), str(dest_file))
            print(f"  ✅ {filepath.name} → {date}/{category}/")
            self.stats['moved'] += 1
        except Exception as e:
            print(f"  ❌ Erro: {e}")

    def cleanup_empty_folders(self):
        """Remove pastas vazias"""
        print("\n🧹 LIMPANDO PASTAS VAZIAS...")

        for folder in self.archive.iterdir():
            if folder.is_dir() and not any(folder.rglob('*')):
                try:
                    folder.rmdir()
                    print(f"  🗑️ Removida: {folder.name}/")
                except:
                    pass

    def generate_report(self):
        """Relatório final"""
        print("\n" + "="*50)
        print("📊 RELATÓRIO FINAL DE ORGANIZAÇÃO")
        print("="*50)

        print(f"\n📈 Estatísticas:")
        print(f"  Pastas processadas: {self.stats['folders_processed']}")
        print(f"  Arquivos movidos: {self.stats['moved']}")
        print(f"  Duplicatas removidas: {self.stats['duplicates']}")

        print(f"\n📅 Estrutura Final (apenas datas):")
        date_folders = sorted([
            d for d in self.archive.iterdir()
            if d.is_dir() and d.name.startswith('20')
        ])

        for date_dir in date_folders:
            total_files = sum(1 for _ in date_dir.rglob('*') if _.is_file())
            if total_files > 0:
                print(f"  {date_dir.name}/  ({total_files} arquivos)")

                # Mostra subcategorias
                for subdir in sorted(date_dir.iterdir()):
                    if subdir.is_dir():
                        count = sum(1 for _ in subdir.rglob('*') if _.is_file())
                        if count > 0:
                            print(f"    └── {subdir.name}/  ({count} arquivos)")

    def run(self):
        """Executa organização completa"""
        print("🚀 ORGANIZADOR FINAL DO ARCHIVE")
        print("================================")
        print("PADRÃO ÚNICO: YYYY-MM-DD/categoria/arquivo")

        # Processa pastas não-padrão
        self.process_non_standard_folders()

        # Limpa pastas vazias
        self.cleanup_empty_folders()

        # Relatório
        self.generate_report()

        print("\n✅ ARCHIVE TOTALMENTE ORGANIZADO!")
        print("📁 Padrão único estabelecido: YYYY-MM-DD/categoria/")
        print("🔍 Para navegar: /Users/clubproducoes/Digimundo/archive/YYYY-MM-DD/")

if __name__ == '__main__':
    organizer = FinalArchiveOrganizer()
    organizer.run()