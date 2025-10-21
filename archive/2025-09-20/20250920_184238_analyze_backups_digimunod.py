#!/usr/bin/env python3
"""
🔍 ANALISADOR DE BACKUPS DIGIMUNOD - EXTRAI APENAS ARQUIVOS ÚNICOS
Analisa pasta Backups Digimunod e adiciona apenas conteúdo único ao Git
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib
import json
import zipfile
import tempfile

class BackupsDigimunodAnalyzer:
    def __init__(self):
        self.backup_path = Path("/Users/clubproducoes/Backups Digimunod")

        # Repositório Git existente
        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-history")

        # Arquivo de análise
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/backups_digimunod_analysis.json")

        # Extensões desejadas
        self.wanted_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash',
            '.md', '.txt', '.rst', '.json', '.yaml', '.yml',
            '.html', '.css', '.scss', '.sql', '.xml', '.ini'
        }

        # Hashes globais de arquivos já existentes
        self.existing_hashes = {}
        self.new_unique_files = []
        self.duplicates_found = []

    def phase1_scan_existing_repo(self):
        """FASE 1: Escaneia repositório Git existente para criar base de hashes"""
        print("📂 FASE 1: Analisando repositório Git existente...")

        if not self.git_repo_path.exists():
            print("   ⚠️ Repositório Git não encontrado!")
            return

        file_count = 0
        for root, dirs, files in os.walk(self.git_repo_path):
            # Ignorar .git
            dirs[:] = [d for d in dirs if d != '.git']

            for file in files:
                if file.startswith('.'):
                    continue

                file_path = Path(root) / file

                try:
                    # Hash do conteúdo
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()

                    self.existing_hashes[file_hash] = str(file_path)
                    file_count += 1

                    if file_count % 1000 == 0:
                        print(f"   📊 {file_count:,} arquivos indexados...")

                except Exception:
                    pass

        print(f"✅ FASE 1 completa: {len(self.existing_hashes):,} hashes únicos catalogados")

    def phase2_analyze_archives(self):
        """FASE 2: Analisa o arquivo ARCHIVES.zip"""
        print("\n📦 FASE 2: Analisando ARCHIVES.zip (11GB)...")

        archive_path = self.backup_path / "ARCHIVES.zip"
        if not archive_path.exists():
            print(f"   ⚠️ Arquivo não encontrado: {archive_path}")
            return

        size_gb = archive_path.stat().st_size / (1024**3)
        print(f"   📁 Tamanho: {size_gb:.1f} GB")

        unique_count = 0
        duplicate_count = 0
        processed = 0

        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                members = zip_file.namelist()
                total = len(members)
                print(f"   📦 {total:,} arquivos no ZIP")

                for member_name in members:
                    processed += 1
                    if processed % 500 == 0:
                        percent = (processed / total) * 100
                        print(f"      Processando {processed}/{total} ({percent:.1f}%)...")

                    try:
                        info = zip_file.getinfo(member_name)
                        if info.is_dir():
                            continue

                        file_path = Path(member_name)

                        # Filtrar extensões
                        if file_path.suffix.lower() not in self.wanted_extensions:
                            continue

                        # Ignorar arquivos do sistema
                        if file_path.name.startswith('.'):
                            continue

                        # Ler conteúdo
                        content = zip_file.read(member_name)
                        file_hash = hashlib.md5(content).hexdigest()

                        # Verificar se é único
                        if file_hash in self.existing_hashes:
                            duplicate_count += 1
                            self.duplicates_found.append({
                                'name': file_path.name,
                                'path': member_name,
                                'existing': self.existing_hashes[file_hash]
                            })
                        else:
                            # Arquivo único! Salvar temporariamente
                            with tempfile.NamedTemporaryFile(delete=False, suffix=file_path.suffix) as tmp:
                                tmp.write(content)
                                tmp.flush()

                                # Registrar arquivo único
                                file_info = {
                                    'temp_path': tmp.name,
                                    'original_name': file_path.name,
                                    'original_path': member_name,
                                    'size': info.file_size,
                                    'created': datetime(*info.date_time).isoformat(),
                                    'extension': file_path.suffix.lower(),
                                    'source': 'ARCHIVES.zip',
                                    'hash': file_hash
                                }

                                self.new_unique_files.append(file_info)
                                self.existing_hashes[file_hash] = member_name
                                unique_count += 1

                    except Exception as e:
                        pass

        except Exception as e:
            print(f"   ❌ Erro ao processar ZIP: {e}")

        print(f"   ✅ ARCHIVES.zip: {unique_count} únicos, {duplicate_count} duplicatas")

    def phase3_scan_folders(self):
        """FASE 3: Escaneia pastas bin e data"""
        print("\n📂 FASE 3: Analisando pastas bin e data...")

        for folder_name in ['bin', 'data']:
            folder_path = self.backup_path / folder_name
            if not folder_path.exists():
                continue

            print(f"   🔍 Processando: {folder_name}/")
            folder_unique = 0

            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file

                    # Filtrar extensões
                    if file_path.suffix.lower() not in self.wanted_extensions:
                        continue

                    # Ignorar arquivos do sistema
                    if file.startswith('.'):
                        continue

                    try:
                        # Hash do conteúdo
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            file_hash = hashlib.md5(content).hexdigest()

                        # Verificar se é único
                        if file_hash not in self.existing_hashes:
                            # Salvar temporariamente
                            with tempfile.NamedTemporaryFile(delete=False, suffix=file_path.suffix) as tmp:
                                tmp.write(content)
                                tmp.flush()

                                stat = file_path.stat()
                                file_info = {
                                    'temp_path': tmp.name,
                                    'original_name': file,
                                    'original_path': str(file_path),
                                    'size': stat.st_size,
                                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                    'extension': file_path.suffix.lower(),
                                    'source': f'{folder_name}/',
                                    'hash': file_hash
                                }

                                self.new_unique_files.append(file_info)
                                self.existing_hashes[file_hash] = str(file_path)
                                folder_unique += 1

                    except Exception:
                        pass

            print(f"      ✅ {folder_name}/: {folder_unique} arquivos únicos")

    def phase4_add_to_git(self):
        """FASE 4: Adiciona arquivos únicos ao repositório Git"""
        if not self.new_unique_files:
            print("\n⚠️ Nenhum arquivo único encontrado!")
            return

        print(f"\n🚀 FASE 4: Adicionando {len(self.new_unique_files)} arquivos únicos ao Git...")

        os.chdir(self.git_repo_path)

        # Agrupar por tipo
        by_category = {}
        for file_info in self.new_unique_files:
            ext = file_info['extension']

            if ext in {'.py', '.js', '.ts', '.sh'}:
                category = "code"
            elif ext in {'.md', '.txt', '.rst'}:
                category = "docs"
            elif ext in {'.json', '.yaml', '.yml'}:
                category = "config"
            else:
                category = "misc"

            if category not in by_category:
                by_category[category] = []
            by_category[category].append(file_info)

        # Copiar arquivos
        copied = 0
        for category, files in by_category.items():
            print(f"   📁 {category}: {len(files)} arquivos")

            for file_info in files:
                created = datetime.fromisoformat(file_info['created'])
                dest_dir = self.git_repo_path / category / created.strftime("%Y-%m") / "backups_digimunod"
                dest_dir.mkdir(parents=True, exist_ok=True)

                # Nome único
                dest_name = f"{created.strftime('%Y%m%d_%H%M%S')}_{file_info['original_name']}"
                dest_path = dest_dir / dest_name

                try:
                    shutil.copy2(file_info['temp_path'], dest_path)
                    os.unlink(file_info['temp_path'])  # Limpar temporário
                    copied += 1
                except Exception:
                    pass

        if copied > 0:
            # Commit
            subprocess.run(['git', 'add', '.'], check=True)

            msg = f"🆕 Backups Digimunod Analisados - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            msg += f"📦 ARCHIVES.zip processado (11GB)\n"
            msg += f"✨ Arquivos únicos adicionados: {copied}\n"
            msg += f"🔗 Duplicatas ignoradas: {len(self.duplicates_found)}\n\n"
            msg += "📊 Por categoria:\n"
            for cat, files in by_category.items():
                msg += f"  • {cat}: {len(files)} arquivos\n"

            subprocess.run(['git', 'commit', '-m', msg], check=True)

            # Tag
            tag = f"backups-digimunod-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            subprocess.run(['git', 'tag', tag], check=True)

            print(f"   ✅ Git commit criado com {copied} arquivos")
            print(f"   🏷️ Tag: {tag}")

    def generate_report(self):
        """Gera relatório da análise"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'backup_path': str(self.backup_path),
            'archives_size_gb': 11.1,
            'existing_files_in_git': len(self.existing_hashes) - len(self.new_unique_files),
            'new_unique_files': len(self.new_unique_files),
            'duplicates_found': len(self.duplicates_found),
            'total_new_size_mb': sum(f['size'] for f in self.new_unique_files) / (1024**2) if self.new_unique_files else 0,
            'unique_files': self.new_unique_files[:100],  # Limitar para não ficar muito grande
            'duplicates_sample': self.duplicates_found[:50]
        }

        with open(self.analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print("\n" + "="*60)
        print("✅ ANÁLISE DE BACKUPS DIGIMUNOD COMPLETA!")
        print(f"📂 Pasta analisada: {self.backup_path}")
        print(f"📦 ARCHIVES.zip: 11.1 GB")
        print(f"📁 Arquivos já no Git: {analysis['existing_files_in_git']:,}")
        print(f"✨ Novos arquivos únicos: {analysis['new_unique_files']:,}")
        print(f"🔗 Duplicatas ignoradas: {analysis['duplicates_found']:,}")
        print(f"💾 Tamanho novo adicionado: {analysis['total_new_size_mb']:.1f} MB")
        print(f"📊 Análise salva em: {self.analysis_file}")
        print(f"📁 Repositório Git: {self.git_repo_path}")
        print("\n🗑️ Após verificar, você pode deletar:")
        print(f"   rm -rf '/Users/clubproducoes/Backups Digimunod'")

def main():
    analyzer = BackupsDigimunodAnalyzer()

    print("🔍 ANALISADOR DE BACKUPS DIGIMUNOD")
    print("="*60)

    # Fase 1: Indexar repositório existente
    analyzer.phase1_scan_existing_repo()

    # Fase 2: Analisar ARCHIVES.zip
    analyzer.phase2_analyze_archives()

    # Fase 3: Analisar pastas bin e data
    analyzer.phase3_scan_folders()

    # Fase 4: Adicionar ao Git
    analyzer.phase4_add_to_git()

    # Relatório
    analyzer.generate_report()

if __name__ == "__main__":
    main()