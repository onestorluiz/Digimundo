#!/usr/bin/env python3
"""
🔍 ANALISADOR DE NOVOS BACKUPS - EXTRAI APENAS ARQUIVOS ÚNICOS
Analisa novos backups e adiciona apenas conteúdo único ao Git
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

class NewBackupAnalyzer:
    def __init__(self):
        self.backup_files = [
            Path("/Users/clubproducoes/Digimundo/scripturemon-champion 2.zip"),
            Path("/Users/clubproducoes/Digimundo/Novos_backps/scripturemon-champion.zip")
        ]

        # Repositório Git existente
        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-ultimate-history")

        # Arquivo de análise
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/new_backups_analysis.json")

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

    def phase2_analyze_backups(self):
        """FASE 2: Analisa os novos backups ZIP"""
        print("\n📦 FASE 2: Analisando novos backups...")

        for backup_path in self.backup_files:
            if not backup_path.exists():
                print(f"   ⚠️ Não encontrado: {backup_path}")
                continue

            size_mb = backup_path.stat().st_size / (1024**2)
            print(f"\n🔍 Processando: {backup_path.name} ({size_mb:.1f} MB)")

            unique_count = 0
            duplicate_count = 0

            try:
                with zipfile.ZipFile(backup_path, 'r') as zip_file:
                    members = zip_file.namelist()
                    print(f"   📁 {len(members):,} arquivos no ZIP")

                    for i, member_name in enumerate(members, 1):
                        if i % 500 == 0:
                            print(f"      Processando {i}/{len(members)}...")

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

                        try:
                            # Ler conteúdo
                            content = zip_file.read(member_name)
                            file_hash = hashlib.md5(content).hexdigest()

                            # Verificar se é único
                            if file_hash in self.existing_hashes:
                                duplicate_count += 1
                                self.duplicates_found.append({
                                    'name': file_path.name,
                                    'source': backup_path.name,
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
                                        'source_backup': backup_path.name,
                                        'hash': file_hash
                                    }

                                    self.new_unique_files.append(file_info)
                                    self.existing_hashes[file_hash] = member_name
                                    unique_count += 1

                        except Exception as e:
                            pass

            except Exception as e:
                print(f"   ❌ Erro ao processar ZIP: {e}")

            print(f"   ✅ {backup_path.name}: {unique_count} únicos, {duplicate_count} duplicatas")

    def phase3_add_to_git(self):
        """FASE 3: Adiciona arquivos únicos ao repositório Git"""
        if not self.new_unique_files:
            print("\n⚠️ Nenhum arquivo único encontrado!")
            return

        print(f"\n🚀 FASE 3: Adicionando {len(self.new_unique_files)} arquivos únicos ao Git...")

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
                dest_dir = self.git_repo_path / category / created.strftime("%Y-%m")
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

            msg = f"🆕 Novos Backups Analisados - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            msg += f"📦 Backups processados: 2\n"
            msg += f"✨ Arquivos únicos adicionados: {copied}\n"
            msg += f"🔗 Duplicatas ignoradas: {len(self.duplicates_found)}\n\n"
            msg += "📊 Por categoria:\n"
            for cat, files in by_category.items():
                msg += f"  • {cat}: {len(files)} arquivos\n"

            subprocess.run(['git', 'commit', '-m', msg], check=True)

            # Tag
            tag = f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            subprocess.run(['git', 'tag', tag], check=True)

            print(f"   ✅ Git commit criado com {copied} arquivos")
            print(f"   🏷️ Tag: {tag}")

    def generate_report(self):
        """Gera relatório da análise"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'backups_analyzed': [str(b) for b in self.backup_files],
            'existing_files_in_git': len(self.existing_hashes),
            'new_unique_files': len(self.new_unique_files),
            'duplicates_found': len(self.duplicates_found),
            'total_new_size_mb': sum(f['size'] for f in self.new_unique_files) / (1024**2),
            'unique_files': self.new_unique_files,
            'duplicates': self.duplicates_found[:100]  # Limitar lista
        }

        with open(self.analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print("\n" + "="*60)
        print("✅ ANÁLISE DE NOVOS BACKUPS COMPLETA!")
        print(f"📂 Arquivos já no Git: {analysis['existing_files_in_git']:,}")
        print(f"✨ Novos arquivos únicos: {analysis['new_unique_files']:,}")
        print(f"🔗 Duplicatas ignoradas: {analysis['duplicates_found']:,}")
        print(f"💾 Tamanho novo adicionado: {analysis['total_new_size_mb']:.1f} MB")
        print(f"📊 Análise salva em: {self.analysis_file}")
        print(f"📁 Repositório Git: {self.git_repo_path}")

def main():
    analyzer = NewBackupAnalyzer()

    print("🔍 ANALISADOR DE NOVOS BACKUPS")
    print("="*60)

    # Fase 1: Indexar repositório existente
    analyzer.phase1_scan_existing_repo()

    # Fase 2: Analisar novos backups
    analyzer.phase2_analyze_backups()

    # Fase 3: Adicionar ao Git
    analyzer.phase3_add_to_git()

    # Relatório
    analyzer.generate_report()

if __name__ == "__main__":
    main()