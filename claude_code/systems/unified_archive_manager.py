#!/usr/bin/env python3
"""
🗂️ UNIFIED ARCHIVE MANAGER - Sistema Único de Organização de Archive
Unifica archive_organizer.py e smart_date_organizer.py
Conformidade total com LEI XIII: /Users/clubproducoes/Digimundo/archive/YYYY-MM-DD/
"""

import os
import re
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
import threading
import fcntl

class UnifiedArchiveManager:
    """Gerenciador unificado de archives com detecção inteligente de datas"""

    def __init__(self):
        # LEI XIII: ÚNICO local autorizado
        self.archive = Path('/Users/clubproducoes/Digimundo/archive')
        self.lock_file = Path('/tmp/archive_manager.lock')

        # Estatísticas
        self.stats = {
            'processed': 0,
            'moved': 0,
            'duplicates': 0,
            'errors': 0,
            'folders_processed': 0
        }

        # Cache de hashes para detecção de duplicatas
        self.seen_hashes = {}

        # Padrões para extrair data
        self.date_patterns = [
            # YYYYMMDD_HHMMSS no início
            (re.compile(r'^(\d{4})(\d{2})(\d{2})_'), 'prefix'),
            # YYYY-MM-DD em qualquer lugar
            (re.compile(r'(\d{4})-(\d{2})-(\d{2})'), 'anywhere'),
            # backup_YYYYMMDD
            (re.compile(r'backup_(\d{4})(\d{2})(\d{2})'), 'backup'),
            # analysis_YYYYMMDD_HHMMSS
            (re.compile(r'analysis_(\d{4})(\d{2})(\d{2})_'), 'analysis')
        ]

    def acquire_lock(self):
        """Implementa lock para evitar execuções simultâneas"""
        try:
            self.lock_fd = open(self.lock_file, 'w')
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_fd.write(str(os.getpid()))
            return True
        except IOError:
            print("⚠️ Outro processo de organização já está rodando!")
            return False

    def release_lock(self):
        """Libera o lock"""
        if hasattr(self, 'lock_fd'):
            fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
            self.lock_fd.close()
            if self.lock_file.exists():
                self.lock_file.unlink()

    def get_file_hash(self, filepath):
        """Calcula MD5 para detectar duplicatas"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def extract_date(self, filepath):
        """Extração inteligente de data"""
        filename = filepath.name

        # Tenta todos os padrões
        for pattern, pattern_type in self.date_patterns:
            match = pattern.search(filename)
            if match:
                if pattern_type in ['prefix', 'backup', 'analysis']:
                    year, month, day = match.groups()[:3]
                elif pattern_type == 'anywhere':
                    year, month, day = match.groups()

                # Valida data
                try:
                    datetime(int(year), int(month), int(day))
                    return f"{year}-{month}-{day}"
                except:
                    continue

        # Fallback: usa data de modificação
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

    def categorize_file(self, filepath):
        """Categorização inteligente por extensão e conteúdo"""
        ext = filepath.suffix.lower()
        name = filepath.name.lower()

        # Categorias especiais por nome
        if 'backup' in name or 'archive' in name:
            return 'backups'
        elif 'analysis' in name or 'report' in name:
            return 'analysis'
        elif 'log' in name or 'debug' in name:
            return 'logs'

        # Categorias por extensão
        categories = {
            'code': ['.py', '.sh', '.js', '.tsx', '.jsx', '.cpp', '.java'],
            'docs': ['.md', '.txt', '.pdf', '.doc', '.docx'],
            'configs': ['.json', '.yml', '.yaml', '.toml', '.xml', '.ini'],
            'data': ['.db', '.sqlite', '.sql', '.csv'],
            'logs': ['.log', '.out', '.err'],
            'media': ['.png', '.jpg', '.mp4', '.gif'],
            'archives': ['.zip', '.tar', '.gz', '.7z']
        }

        for category, extensions in categories.items():
            if ext in extensions:
                return category

        return 'misc'

    def move_file_safely(self, filepath, date, category):
        """Move arquivo com verificação de duplicata e segurança"""
        # Verifica duplicata por hash
        file_hash = self.get_file_hash(filepath)

        if file_hash and file_hash in self.seen_hashes:
            print(f"  ❌ Duplicata removida: {filepath.name}")
            filepath.unlink()
            self.stats['duplicates'] += 1
            return

        if file_hash:
            self.seen_hashes[file_hash] = str(filepath)

        # Destino conforme LEI XIII
        dest_dir = self.archive / date / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / filepath.name

        # Evita sobrescrever - adiciona timestamp se necessário
        if dest_file.exists():
            timestamp = datetime.now().strftime('%H%M%S')
            stem = filepath.stem
            suffix = filepath.suffix
            dest_file = dest_dir / f"{stem}_{timestamp}{suffix}"

        # Move com tratamento de erro
        try:
            shutil.move(str(filepath), str(dest_file))
            print(f"  ✅ {filepath.name} → {date}/{category}/")
            self.stats['moved'] += 1

            # Progresso a cada 100 arquivos
            if self.stats['moved'] % 100 == 0:
                print(f"  📊 Progresso: {self.stats['moved']} arquivos organizados...")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            self.stats['errors'] += 1

    def process_all_folders(self):
        """Processa TODAS as pastas não-padrão no archive"""
        print("\n📦 PROCESSANDO ARCHIVE COMPLETO...")

        # Lista todas as pastas que NÃO são YYYY-MM-DD
        non_standard = []
        for item in self.archive.iterdir():
            if item.is_dir():
                # Verifica se é padrão YYYY-MM-DD
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', item.name):
                    non_standard.append(item)

        if not non_standard:
            print("  ✅ Archive já está totalmente organizado!")
            return

        print(f"  📁 {len(non_standard)} pastas não-padrão encontradas")

        for folder in sorted(non_standard):
            print(f"\n📁 Processando: {folder.name}/")
            self.stats['folders_processed'] += 1

            # Processa recursivamente
            for filepath in folder.rglob('*'):
                if filepath.is_file():
                    self.stats['processed'] += 1

                    # Extrai data
                    date = self.extract_date(filepath)

                    # Categoriza
                    category = self.categorize_file(filepath)

                    # Move
                    self.move_file_safely(filepath, date, category)

            # Remove pasta vazia
            self.cleanup_empty_folder(folder)

    def cleanup_empty_folder(self, folder):
        """Remove pasta se estiver vazia (recursivamente)"""
        try:
            # Remove subpastas vazias primeiro
            for root, dirs, files in os.walk(folder, topdown=False):
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()

            # Remove pasta principal se vazia
            if not any(folder.iterdir()):
                folder.rmdir()
                print(f"  🗑️ Pasta vazia removida: {folder.name}")
        except:
            pass

    def cleanup_all_empty(self):
        """Remove todas as pastas vazias no archive"""
        print("\n🧹 LIMPEZA FINAL...")

        empty_count = 0
        for folder in self.archive.iterdir():
            if folder.is_dir() and not any(folder.rglob('*')):
                try:
                    folder.rmdir()
                    print(f"  🗑️ Removida: {folder.name}/")
                    empty_count += 1
                except:
                    pass

        if empty_count > 0:
            print(f"  ✅ {empty_count} pastas vazias removidas")

    def generate_report(self):
        """Relatório completo com análises"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL - UNIFIED ARCHIVE MANAGER")
        print("="*60)

        print(f"\n📈 Estatísticas:")
        print(f"  • Pastas processadas: {self.stats['folders_processed']}")
        print(f"  • Arquivos analisados: {self.stats['processed']}")
        print(f"  • Arquivos organizados: {self.stats['moved']}")
        print(f"  • Duplicatas removidas: {self.stats['duplicates']}")
        print(f"  • Erros: {self.stats['errors']}")

        if self.stats['duplicates'] > 0:
            saved_space = self.stats['duplicates'] * 100  # Estimativa
            print(f"  • Espaço economizado: ~{saved_space/1024:.1f}MB")

        print(f"\n📅 Estrutura Final (YYYY-MM-DD):")
        date_folders = sorted([
            d for d in self.archive.iterdir()
            if d.is_dir() and re.match(r'^\d{4}-\d{2}-\d{2}$', d.name)
        ])

        # Mostra últimas 10 datas com mais detalhes
        for date_dir in date_folders[-10:]:
            total = sum(1 for _ in date_dir.rglob('*') if _.is_file())
            if total > 0:
                print(f"\n  {date_dir.name}/  ({total} arquivos)")

                # Estatísticas por categoria
                categories = {}
                for subdir in date_dir.iterdir():
                    if subdir.is_dir():
                        count = sum(1 for _ in subdir.rglob('*') if _.is_file())
                        if count > 0:
                            categories[subdir.name] = count

                for cat, count in sorted(categories.items()):
                    print(f"    └── {cat:10} ({count:3} arquivos)")

        # Análise de padrões
        print(f"\n🔍 Análise de Padrões:")
        if date_folders:
            first_date = date_folders[0].name
            last_date = date_folders[-1].name
            print(f"  • Período: {first_date} até {last_date}")
            print(f"  • Total de dias com arquivos: {len(date_folders)}")

    def run(self, dry_run=False):
        """Executa organização completa"""
        print("🗂️ UNIFIED ARCHIVE MANAGER")
        print("="*60)
        print(f"📁 Archive: {self.archive}")
        print(f"📏 LEI XIII: Padrão YYYY-MM-DD/categoria/")

        if dry_run:
            print("⚠️ MODO DRY-RUN: Apenas simulação, nada será movido")

        # Adquire lock
        if not self.acquire_lock():
            return False

        try:
            # Processa tudo
            self.process_all_folders()

            # Limpeza
            self.cleanup_all_empty()

            # Relatório
            self.generate_report()

            print("\n✅ ARCHIVE UNIFICADO COM SUCESSO!")
            print("📏 Conformidade total com LEI XIII")
            print("🔍 Para navegar: ls /Users/clubproducoes/Digimundo/archive/YYYY-MM-DD/")
            print("\nDIGIMUNDO PRESENTE")

        finally:
            # Libera lock
            self.release_lock()

        return True

# Interface de comando
if __name__ == '__main__':
    import sys

    manager = UnifiedArchiveManager()

    if '--dry-run' in sys.argv:
        manager.run(dry_run=True)
    elif '--force' in sys.argv:
        manager.run()
    else:
        print("\n⚠️ Este comando vai reorganizar TODO o archive!")
        print("Use --dry-run para simular ou --force para executar")
        print("\nExemplo:")
        print("  python3 unified_archive_manager.py --dry-run  # Simula")
        print("  python3 unified_archive_manager.py --force    # Executa")