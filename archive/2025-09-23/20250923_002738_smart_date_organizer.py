#!/usr/bin/env python3
"""
Organizador Inteligente por Data
Extrai data do nome do arquivo (formato: YYYYMMDD_HHMMSS_nome.ext)
E move para a pasta correta (YYYY-MM-DD)
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class SmartDateOrganizer:
    def __init__(self):
        self.archive = Path('/Users/clubproducoes/Digimundo/archive')
        self.stats = {
            'processed': 0,
            'moved': 0,
            'errors': 0
        }

        # Regex para capturar data no formato YYYYMMDD no início do nome
        self.date_pattern = re.compile(r'^(\d{4})(\d{2})(\d{2})_')

    def extract_date_from_name(self, filename):
        """Extrai data do nome do arquivo"""
        match = self.date_pattern.match(filename)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month}-{day}"
        return None

    def get_category(self, filepath):
        """Categoriza arquivo por extensão"""
        ext = filepath.suffix.lower()

        if ext in ['.py', '.sh', '.js']:
            return 'code'
        elif ext in ['.md', '.txt', '.pdf']:
            return 'docs'
        elif ext in ['.json', '.yml', '.yaml']:
            return 'configs'
        elif ext in ['.db', '.sqlite']:
            return 'data'
        else:
            return 'misc'

    def process_history_folders(self):
        """Processa as pastas history que têm arquivos com datas"""

        history_folders = [
            self.archive / 'digimundo-history',
            self.archive / 'scripturemon-history',
            self.archive / 'backup-2025-09-21',
            self.archive / 'ultimate-history'
        ]

        for folder in history_folders:
            if not folder.exists():
                print(f"  ⚠️ Pasta não encontrada: {folder.name}")
                continue

            print(f"\n📁 Processando: {folder.name}/")

            # Processa recursivamente todos os arquivos
            for filepath in folder.rglob('*'):
                if filepath.is_file():
                    self.stats['processed'] += 1

                    # Tenta extrair data do nome
                    filename = filepath.name
                    date = self.extract_date_from_name(filename)

                    if date:
                        # Move para pasta da data correta
                        category = self.get_category(filepath)
                        dest_dir = self.archive / date / category
                        dest_dir.mkdir(parents=True, exist_ok=True)

                        dest_file = dest_dir / filename

                        # Evita sobrescrever
                        if dest_file.exists():
                            print(f"  ⚠️ Já existe: {filename}")
                            continue

                        try:
                            shutil.move(str(filepath), str(dest_file))
                            print(f"  ✅ {filename} → {date}/{category}/")
                            self.stats['moved'] += 1

                            # A cada 100 arquivos, mostra progresso
                            if self.stats['moved'] % 100 == 0:
                                print(f"  📊 Progresso: {self.stats['moved']} arquivos movidos...")
                        except Exception as e:
                            print(f"  ❌ Erro movendo {filename}: {e}")
                            self.stats['errors'] += 1
                    else:
                        # Se não tem data no nome, usa data de modificação
                        mtime = os.path.getmtime(filepath)
                        date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

                        if self.stats['processed'] % 100 == 0:
                            print(f"  📅 Usando data de modificação para: {filename} → {date}")

    def cleanup_empty_folders(self):
        """Remove pastas vazias após mover arquivos"""
        print("\n🧹 Removendo pastas vazias...")

        folders_to_check = [
            'digimundo-history',
            'scripturemon-history',
            'backup-2025-09-21',
            'ultimate-history'
        ]

        for folder_name in folders_to_check:
            folder = self.archive / folder_name
            if folder.exists():
                # Remove recursivamente pastas vazias
                for root, dirs, files in os.walk(folder, topdown=False):
                    for dir_name in dirs:
                        dir_path = Path(root) / dir_name
                        try:
                            if not any(dir_path.iterdir()):
                                dir_path.rmdir()
                                print(f"  🗑️ Removida pasta vazia: {dir_path.relative_to(self.archive)}")
                        except:
                            pass

                # Tenta remover a pasta principal se estiver vazia
                try:
                    if not any(folder.iterdir()):
                        folder.rmdir()
                        print(f"  🗑️ Removida: {folder_name}/")
                except:
                    pass

    def generate_report(self):
        """Relatório final"""
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE ORGANIZAÇÃO POR DATA")
        print("="*50)

        print(f"\n📈 Estatísticas:")
        print(f"  Arquivos processados: {self.stats['processed']}")
        print(f"  Arquivos movidos: {self.stats['moved']}")
        print(f"  Erros: {self.stats['errors']}")

        print(f"\n📅 Pastas por data no archive:")
        date_folders = sorted([
            d for d in self.archive.iterdir()
            if d.is_dir() and d.name.startswith('20')
        ])

        for date_dir in date_folders[-10:]:  # Últimas 10 datas
            total = sum(1 for _ in date_dir.rglob('*') if _.is_file())
            if total > 0:
                print(f"  {date_dir.name}/  ({total} arquivos)")

    def run(self):
        """Executa organização inteligente"""
        print("🚀 ORGANIZADOR INTELIGENTE POR DATA")
        print("====================================")
        print("Extrai datas do formato: YYYYMMDD_HHMMSS_nome.ext")
        print("Move para: YYYY-MM-DD/categoria/\n")

        # Processa pastas history
        self.process_history_folders()

        # Remove pastas vazias
        self.cleanup_empty_folders()

        # Relatório
        self.generate_report()

        print("\n✅ Organização concluída!")
        print("📁 Archive organizado por data extraída dos nomes!")

if __name__ == '__main__':
    # Confirma antes de executar
    print("⚠️ ATENÇÃO: Este script vai mover milhares de arquivos!")
    print("Pastas a processar:")
    print("  - digimundo-history/")
    print("  - scripturemon-history/")
    print("  - backup-2025-09-21/")
    print("  - ultimate-history/")
    print("\nDeseja continuar? (s/n): ", end='')

    response = input().strip().lower()
    if response == 's':
        organizer = SmartDateOrganizer()
        organizer.run()
    else:
        print("❌ Operação cancelada")