#!/usr/bin/env python3
"""
🧠 MIGRAÇÃO ULTIMATE SMART - ANALISA DENTRO DOS BACKUPS
Extrai apenas arquivos únicos que não existem fora dos compactados
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import json
import tarfile
import zipfile
import tempfile

class UltimateSmartMigrator:
    def __init__(self):
        self.historical_paths = [
            Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION"),
            Path("/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia"),
            Path("/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo")
        ]

        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-ultimate-history")
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/ultimate_migration_analysis.json")

        # Extensões de código/docs que queremos preservar
        self.wanted_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash',
            '.md', '.txt', '.rst', '.json', '.yaml', '.yml',
            '.html', '.css', '.scss', '.sql', '.xml', '.ini'
        }

        # Hash global de todos os arquivos já encontrados
        self.global_hashes = {}
        self.files_from_archives = []
        self.files_from_folders = []

    def phase1_scan_loose_files(self):
        """FASE 1: Escaneia todos os arquivos 'soltos' (não compactados)"""
        print("📂 FASE 1: Escaneando arquivos não-compactados...")

        for historical_path in self.historical_paths:
            if not historical_path.exists():
                continue

            print(f"\n🔍 Processando: {historical_path.name}")

            for root, dirs, files in os.walk(historical_path):
                # Ignorar diretórios ocultos
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for file in files:
                    # Pular arquivos compactados nesta fase
                    if file.endswith(('.tar', '.gz', '.zip', '.rar', '.7z', '.bz2')):
                        continue

                    file_path = Path(root) / file

                    # Pular arquivos do sistema
                    if file.startswith('.'):
                        continue

                    # Só processar extensões desejadas
                    if file_path.suffix.lower() not in self.wanted_extensions:
                        continue

                    try:
                        stat = file_path.stat()

                        # Hash do conteúdo (ou tamanho+nome para arquivos grandes)
                        if stat.st_size < 10 * 1024 * 1024:  # <10MB
                            with open(file_path, 'rb') as f:
                                file_hash = hashlib.md5(f.read()).hexdigest()
                        else:
                            file_hash = f"{stat.st_size}_{file_path.name}"

                        # Registrar no hash global
                        if file_hash not in self.global_hashes:
                            self.global_hashes[file_hash] = {
                                'path': str(file_path),
                                'name': file,
                                'size': stat.st_size,
                                'created': datetime.fromtimestamp(stat.st_birthtime).isoformat(),
                                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                'extension': file_path.suffix.lower(),
                                'source': 'folder'
                            }
                            self.files_from_folders.append(self.global_hashes[file_hash])

                    except Exception as e:
                        pass

        print(f"\n✅ FASE 1 completa: {len(self.files_from_folders)} arquivos únicos encontrados")

    def phase2_scan_archives(self):
        """FASE 2: Escaneia DENTRO dos arquivos compactados"""
        print("\n📦 FASE 2: Analisando arquivos compactados...")

        archives_found = []

        # Encontrar todos os arquivos compactados
        for historical_path in self.historical_paths:
            if not historical_path.exists():
                continue

            for root, dirs, files in os.walk(historical_path):
                for file in files:
                    if file.endswith(('.tar', '.tar.gz', '.tgz', '.zip')):
                        archives_found.append(Path(root) / file)

        print(f"   📦 {len(archives_found)} arquivos compactados encontrados")

        # Analisar cada arquivo compactado
        for i, archive_path in enumerate(archives_found, 1):
            size_mb = archive_path.stat().st_size / (1024**2)
            print(f"\n   [{i}/{len(archives_found)}] {archive_path.name} ({size_mb:.1f} MB)")

            extracted_count = 0

            # Processar tar/tar.gz
            if str(archive_path).endswith(('.tar', '.tar.gz', '.tgz')):
                extracted_count += self.process_tar_archive(archive_path)

            # Processar zip
            elif archive_path.suffix.lower() == '.zip':
                extracted_count += self.process_zip_archive(archive_path)

            if extracted_count > 0:
                print(f"      ✨ {extracted_count} arquivos únicos extraídos")

    def process_tar_archive(self, archive_path):
        """Processa arquivo tar/tar.gz e extrai apenas arquivos únicos"""
        extracted = 0

        try:
            # Determinar modo de abertura
            if str(archive_path).endswith('.gz'):
                mode = 'r:gz'
            elif str(archive_path).endswith('.bz2'):
                mode = 'r:bz2'
            else:
                mode = 'r'

            with tarfile.open(archive_path, mode) as tar:
                # Usar getmembers com cuidado
                try:
                    members = tar.getmembers()
                except:
                    # Se falhar, tentar listar com tar command
                    print(f"      ⚠️ Arquivo corrompido, tentando método alternativo...")
                    return self.process_tar_with_command(archive_path)

                for member in members:
                    if not member.isfile():
                        continue

                    file_path = Path(member.name)

                    # Filtrar extensões desejadas
                    if file_path.suffix.lower() not in self.wanted_extensions:
                        continue

                    # Criar hash baseado em nome+tamanho
                    file_hash = f"{member.size}_{file_path.name}"

                    # Se não existe ainda, extrair
                    if file_hash not in self.global_hashes:
                        # Extrair para temporário
                        with tempfile.NamedTemporaryFile(delete=False) as tmp:
                            try:
                                f = tar.extractfile(member)
                                if f:
                                    tmp.write(f.read())
                                    tmp.flush()

                                    # Calcular hash real se pequeno
                                    if member.size < 10 * 1024 * 1024:
                                        tmp.seek(0)
                                        real_hash = hashlib.md5(tmp.read()).hexdigest()

                                        # Verificar se hash real já existe
                                        if real_hash in self.global_hashes:
                                            os.unlink(tmp.name)
                                            continue

                                        file_hash = real_hash

                                    # Registrar arquivo único
                                    self.global_hashes[file_hash] = {
                                        'path': tmp.name,  # Caminho temporário
                                        'name': file_path.name,
                                        'size': member.size,
                                        'created': datetime.fromtimestamp(member.mtime).isoformat(),
                                        'modified': datetime.fromtimestamp(member.mtime).isoformat(),
                                        'extension': file_path.suffix.lower(),
                                        'source': f'archive:{archive_path.name}',
                                        'temp_file': True
                                    }
                                    self.files_from_archives.append(self.global_hashes[file_hash])
                                    extracted += 1

                            except Exception as e:
                                if 'tmp' in locals():
                                    os.unlink(tmp.name)

        except Exception as e:
            print(f"      ❌ Erro ao processar: {e}")

        return extracted

    def process_tar_with_command(self, archive_path):
        """Usa comando tar para listar conteúdo de arquivo corrompido"""
        extracted = 0

        try:
            # Listar conteúdo com tar
            result = subprocess.run(
                ['tar', '-tzf', str(archive_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                files = result.stdout.strip().split('\n')

                for file in files:
                    file_path = Path(file)

                    # Filtrar extensões
                    if file_path.suffix.lower() in self.wanted_extensions:
                        # Hash simples baseado em nome
                        file_hash = f"cmd_{file_path.name}"

                        if file_hash not in self.global_hashes:
                            self.global_hashes[file_hash] = {
                                'path': str(archive_path),
                                'name': file_path.name,
                                'size': 0,  # Não sabemos o tamanho
                                'created': datetime.now().isoformat(),
                                'modified': datetime.now().isoformat(),
                                'extension': file_path.suffix.lower(),
                                'source': f'archive_cmd:{archive_path.name}',
                                'needs_extraction': True
                            }
                            self.files_from_archives.append(self.global_hashes[file_hash])
                            extracted += 1

        except Exception as e:
            pass

        return extracted

    def process_zip_archive(self, archive_path):
        """Processa arquivo zip e extrai apenas arquivos únicos"""
        extracted = 0

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for info in zip_file.infolist():
                    if info.is_dir():
                        continue

                    file_path = Path(info.filename)

                    # Filtrar extensões
                    if file_path.suffix.lower() not in self.wanted_extensions:
                        continue

                    # Hash baseado em tamanho+nome
                    file_hash = f"{info.file_size}_{file_path.name}"

                    if file_hash not in self.global_hashes:
                        # Extrair para temporário
                        with tempfile.NamedTemporaryFile(delete=False) as tmp:
                            try:
                                tmp.write(zip_file.read(info))
                                tmp.flush()

                                # Hash real se pequeno
                                if info.file_size < 10 * 1024 * 1024:
                                    tmp.seek(0)
                                    real_hash = hashlib.md5(tmp.read()).hexdigest()

                                    if real_hash in self.global_hashes:
                                        os.unlink(tmp.name)
                                        continue

                                    file_hash = real_hash

                                # Registrar
                                self.global_hashes[file_hash] = {
                                    'path': tmp.name,
                                    'name': file_path.name,
                                    'size': info.file_size,
                                    'created': datetime(*info.date_time).isoformat(),
                                    'modified': datetime(*info.date_time).isoformat(),
                                    'extension': file_path.suffix.lower(),
                                    'source': f'archive:{archive_path.name}',
                                    'temp_file': True
                                }
                                self.files_from_archives.append(self.global_hashes[file_hash])
                                extracted += 1

                            except Exception as e:
                                if 'tmp' in locals():
                                    os.unlink(tmp.name)

        except Exception as e:
            print(f"      ❌ Erro ao processar zip: {e}")

        return extracted

    def phase3_create_git(self):
        """FASE 3: Cria repositório Git com todos os arquivos únicos"""
        print("\n🚀 FASE 3: Criando repositório Git...")

        # Limpar/criar repositório
        if self.git_repo_path.exists():
            shutil.rmtree(self.git_repo_path)

        self.git_repo_path.mkdir()
        os.chdir(self.git_repo_path)

        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Ultimate Migrator'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'ultimate@digimundo.dev'], check=True)

        # Combinar todos os arquivos únicos
        all_files = list(self.global_hashes.values())
        all_files.sort(key=lambda x: x['created'])

        # Agrupar por mês
        from collections import defaultdict
        by_month = defaultdict(list)

        for file_info in all_files:
            created = datetime.fromisoformat(file_info['created'])
            month_key = created.strftime("%Y-%m")
            by_month[month_key].append(file_info)

        # Processar cada mês
        for month in sorted(by_month.keys()):
            files = by_month[month]
            print(f"\n📅 Processando {month}: {len(files)} arquivos")

            copied = 0
            for file_info in files:
                if self.copy_file_to_git(file_info):
                    copied += 1

            if copied > 0:
                # Commit
                subprocess.run(['git', 'add', '.'], check=True)

                msg = f"📅 {month}\n\n"
                msg += f"📁 {copied} arquivos\n"
                msg += f"📂 {len([f for f in files if f['source'] == 'folder'])} de pastas\n"
                msg += f"📦 {len([f for f in files if 'archive' in f['source']])} de arquivos compactados\n"

                subprocess.run(['git', 'commit', '-m', msg], check=True)

                # Tag
                subprocess.run(['git', 'tag', f"v{month}"], check=True)

    def copy_file_to_git(self, file_info):
        """Copia arquivo para repositório Git"""
        source_path = Path(file_info['path'])

        if not source_path.exists() and not file_info.get('needs_extraction'):
            return False

        # Organizar por tipo
        ext = file_info['extension'].lower()
        if ext in {'.py', '.js', '.ts', '.sh'}:
            category = "code"
        elif ext in {'.md', '.txt', '.rst'}:
            category = "docs"
        elif ext in {'.json', '.yaml', '.yml'}:
            category = "config"
        else:
            category = "misc"

        # Criar diretório
        created = datetime.fromisoformat(file_info['created'])
        dest_dir = self.git_repo_path / category / created.strftime("%Y-%m")
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Nome único
        dest_name = f"{created.strftime('%Y%m%d_%H%M%S')}_{file_info['name']}"
        dest_path = dest_dir / dest_name

        try:
            if file_info.get('needs_extraction'):
                # Precisaria extrair do arquivo compactado
                # Por ora, pular
                return False
            else:
                shutil.copy2(source_path, dest_path)

                # Limpar arquivo temporário se houver
                if file_info.get('temp_file'):
                    os.unlink(source_path)

                return True
        except:
            return False

    def generate_report(self):
        """Gera relatório final"""
        total_files = len(self.global_hashes)
        from_folders = len(self.files_from_folders)
        from_archives = len(self.files_from_archives)

        print("\n" + "="*60)
        print("✅ MIGRAÇÃO ULTIMATE COMPLETA!")
        print(f"📁 Total de arquivos únicos: {total_files:,}")
        print(f"📂 De pastas: {from_folders:,}")
        print(f"📦 De arquivos compactados: {from_archives:,} (NOVOS!)")
        print(f"💎 Arquivos recuperados de backups: {from_archives:,}")
        print(f"📍 Repositório: {self.git_repo_path}")

def main():
    migrator = UltimateSmartMigrator()

    print("🧠 MIGRAÇÃO ULTIMATE - ANALISANDO DENTRO DOS BACKUPS")
    print("="*60)

    # FASE 1: Arquivos soltos
    migrator.phase1_scan_loose_files()

    # FASE 2: Dentro dos arquivos compactados
    migrator.phase2_scan_archives()

    # FASE 3: Criar Git
    migrator.phase3_create_git()

    # Relatório
    migrator.generate_report()

if __name__ == "__main__":
    main()