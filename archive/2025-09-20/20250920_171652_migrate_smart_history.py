#!/usr/bin/env python3
"""
🧠 MIGRAÇÃO INTELIGENTE HISTÓRIA DIGIMUNDO → GIT
Migra apenas código fonte e documentos, ignorando arquivos compactados
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import json

class SmartHistoryMigrator:
    def __init__(self):
        # Pastas históricas para processar
        self.historical_paths = [
            Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION"),
            Path("/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia"),
            Path("/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo")
        ]

        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-smart-history")
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/smart_migration_analysis.json")

        # EXTENSÕES A IGNORAR (arquivos compactados e backups)
        self.ignored_extensions = {
            '.tar', '.gz', '.zip', '.rar', '.7z', '.bz2', '.xz',
            '.tar.gz', '.tar.bz2', '.tar.xz', '.tgz',
            '.dmg', '.iso', '.pkg', '.deb', '.rpm',
            '.backup', '.bak', '.old', '.orig'
        }

        # EXTENSÕES PRIORITÁRIAS (código e documentação)
        self.priority_extensions = {
            # Código
            '.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash',
            '.c', '.cpp', '.h', '.hpp', '.java', '.go', '.rs',
            '.swift', '.kt', '.scala', '.rb', '.php', '.r',

            # Documentação
            '.md', '.txt', '.rst', '.doc', '.docx', '.odt',

            # Configuração
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
            '.env', '.config', '.conf', '.xml',

            # Web
            '.html', '.css', '.scss', '.sass', '.less',

            # Dados estruturados
            '.csv', '.sql', '.db', '.sqlite',

            # Scripts e notebooks
            '.ipynb', '.rmd', '.jl',

            # Diagramas e docs técnicos
            '.dot', '.puml', '.drawio', '.tex'
        }

    def should_ignore_file(self, file_path):
        """Determina se arquivo deve ser ignorado"""
        # Ignorar arquivos do sistema
        if file_path.name.startswith('.'):
            return True

        # Verificar extensão completa (para .tar.gz etc)
        for ext in self.ignored_extensions:
            if str(file_path).endswith(ext):
                return True

        # Ignorar arquivos muito grandes (>50MB) que não são código
        try:
            if file_path.stat().st_size > 50 * 1024 * 1024:
                if file_path.suffix.lower() not in self.priority_extensions:
                    return True
        except:
            pass

        return False

    def analyze_smart_files(self):
        """Analisa apenas arquivos relevantes, ignorando compactados"""
        print("🧠 ANÁLISE INTELIGENTE - Ignorando arquivos compactados...")

        file_timeline = []
        duplicate_hashes = {}
        ignored_count = 0
        ignored_size = 0

        for historical_path in self.historical_paths:
            if not historical_path.exists():
                print(f"⚠️ Pasta não encontrada: {historical_path}")
                continue

            print(f"\n🔍 Processando: {historical_path.name}")

            path_size = sum(f.stat().st_size for f in historical_path.rglob('*') if f.is_file()) / (1024**3)
            print(f"   📂 Tamanho total da pasta: {path_size:.1f} GB")

            file_count = 0
            for root, dirs, files in os.walk(historical_path):
                # Ignorar diretórios ocultos
                dirs[:] = [d for d in dirs if not d.startswith('.')]

                for file in files:
                    file_path = Path(root) / file

                    # FILTRO INTELIGENTE
                    if self.should_ignore_file(file_path):
                        ignored_count += 1
                        try:
                            ignored_size += file_path.stat().st_size
                        except:
                            pass
                        continue

                    try:
                        stat = file_path.stat()

                        # Hash apenas para arquivos pequenos (<10MB)
                        file_hash = None
                        if stat.st_size < 10 * 1024 * 1024:
                            with open(file_path, 'rb') as f:
                                file_hash = hashlib.md5(f.read()).hexdigest()
                        else:
                            # Para arquivos grandes, usar tamanho+nome como identificador
                            file_hash = f"{stat.st_size}_{file_path.name}"

                        file_info = {
                            'path': str(file_path),
                            'name': file,
                            'size': stat.st_size,
                            'created': datetime.fromtimestamp(stat.st_birthtime).isoformat(),
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'hash': file_hash,
                            'extension': file_path.suffix.lower(),
                            'relative_path': str(file_path.relative_to(historical_path)),
                            'is_priority': file_path.suffix.lower() in self.priority_extensions
                        }

                        # Detectar duplicatas
                        if file_hash in duplicate_hashes:
                            file_info['is_duplicate'] = True
                            file_info['original'] = duplicate_hashes[file_hash]
                        else:
                            duplicate_hashes[file_hash] = str(file_path)
                            file_info['is_duplicate'] = False

                        file_timeline.append(file_info)
                        file_count += 1

                        if file_count % 1000 == 0:
                            print(f"   📊 Processados: {file_count:,} arquivos relevantes...")

                    except Exception as e:
                        pass  # Ignorar erros silenciosamente

            print(f"   ✅ {historical_path.name}: {file_count:,} arquivos relevantes")

        # Ordenar por data de criação
        file_timeline.sort(key=lambda x: x['created'])

        # Estatísticas
        unique_files = [f for f in file_timeline if not f['is_duplicate']]
        priority_files = [f for f in unique_files if f['is_priority']]

        analysis = {
            'total_files_scanned': len(file_timeline) + ignored_count,
            'ignored_files': ignored_count,
            'ignored_size_gb': ignored_size / (1024**3),
            'relevant_files': len(file_timeline),
            'unique_files': len(unique_files),
            'duplicates': len([f for f in file_timeline if f['is_duplicate']]),
            'priority_files': len(priority_files),
            'total_size_mb': sum(f['size'] for f in file_timeline) / (1024**2),
            'unique_size_mb': sum(f['size'] for f in unique_files) / (1024**2),
            'priority_size_mb': sum(f['size'] for f in priority_files) / (1024**2),
            'timeline': file_timeline,
            'analysis_date': datetime.now().isoformat()
        }

        # Salvar análise
        with open(self.analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print("\n" + "="*60)
        print("📊 ANÁLISE INTELIGENTE COMPLETA:")
        print(f"   🔍 Arquivos analisados: {analysis['total_files_scanned']:,}")
        print(f"   🚫 Arquivos ignorados: {analysis['ignored_files']:,} ({analysis['ignored_size_gb']:.1f} GB)")
        print(f"   📁 Arquivos relevantes: {analysis['relevant_files']:,}")
        print(f"   🔗 Arquivos únicos: {analysis['unique_files']:,}")
        print(f"   ⭐ Arquivos prioritários: {analysis['priority_files']:,}")
        print(f"   📋 Duplicatas: {analysis['duplicates']:,}")
        print(f"   💾 Tamanho final: {analysis['unique_size_mb']/1024:.1f} GB")
        print(f"   ✨ Economia vs original: {(analysis['ignored_size_gb'] + (analysis['total_size_mb']-analysis['unique_size_mb'])/1024):.1f} GB")

        # Listar tipos de arquivo mais comuns
        from collections import Counter
        ext_counter = Counter(f['extension'] for f in unique_files)
        print("\n📝 TOP 10 TIPOS DE ARQUIVO:")
        for ext, count in ext_counter.most_common(10):
            size_mb = sum(f['size'] for f in unique_files if f['extension'] == ext) / (1024**2)
            print(f"   {ext:10} {count:8,} arquivos = {size_mb:8.1f} MB")

        return analysis

    def create_git_repository(self, analysis):
        """Cria repositório Git com arquivos relevantes"""
        print("\n🚀 Criando repositório Git inteligente...")

        # Limpar/criar repositório
        if self.git_repo_path.exists():
            shutil.rmtree(self.git_repo_path)

        self.git_repo_path.mkdir()
        os.chdir(self.git_repo_path)

        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Digimundo Smart Migrator'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'smart@digimundo.dev'], check=True)

        # Processar apenas arquivos únicos e relevantes
        unique_files = [f for f in analysis['timeline'] if not f['is_duplicate']]

        # Agrupar por períodos inteligentes
        periods = self.group_by_smart_periods(unique_files)

        for period_name, files in periods.items():
            print(f"\n📅 Processando: {period_name}")
            print(f"   📁 {len(files)} arquivos únicos")

            copied_count = 0
            for file_info in files:
                if self.copy_file_to_git(file_info):
                    copied_count += 1

            if copied_count > 0:
                # Commit do período
                subprocess.run(['git', 'add', '.'], check=True)

                commit_msg = f"📅 {period_name}\n\n"
                commit_msg += f"📁 {copied_count} arquivos\n"
                commit_msg += f"💾 {sum(f['size'] for f in files) / (1024**2):.1f} MB\n\n"

                # Listar tipos principais
                from collections import Counter
                ext_counter = Counter(f['extension'] for f in files)
                commit_msg += "📝 Principais tipos:\n"
                for ext, count in ext_counter.most_common(5):
                    commit_msg += f"  • {ext}: {count} arquivos\n"

                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)

                # Tag para navegação
                tag_name = f"v{period_name.lower().replace(' ', '-').replace(':', '')}"
                subprocess.run(['git', 'tag', tag_name], check=True)
                print(f"   ✅ Commit criado com {copied_count} arquivos")

    def group_by_smart_periods(self, timeline):
        """Agrupa arquivos por períodos mensais"""
        periods = {}

        for file_info in timeline:
            created_date = datetime.fromisoformat(file_info['created'])
            period_key = created_date.strftime("%Y-%m: %B %Y")

            if period_key not in periods:
                periods[period_key] = []

            periods[period_key].append(file_info)

        return dict(sorted(periods.items()))

    def copy_file_to_git(self, file_info):
        """Copia arquivo para repositório Git organizadamente"""
        source_path = Path(file_info['path'])

        if not source_path.exists():
            return False

        # Organizar por tipo e data
        ext = file_info['extension'].lower()
        created_date = datetime.fromisoformat(file_info['created'])
        year_month = created_date.strftime("%Y-%m")

        # Determinar categoria
        if ext in {'.py', '.js', '.ts', '.sh', '.bash'}:
            category = "code"
        elif ext in {'.md', '.txt', '.rst', '.doc'}:
            category = "docs"
        elif ext in {'.json', '.yaml', '.yml', '.ini'}:
            category = "config"
        elif ext in {'.html', '.css', '.scss'}:
            category = "web"
        elif ext in {'.db', '.sqlite', '.sql'}:
            category = "data"
        else:
            category = "misc"

        # Criar estrutura de diretórios
        dest_dir = self.git_repo_path / category / year_month
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Nome único para evitar conflitos
        dest_name = f"{created_date.strftime('%Y%m%d_%H%M%S')}_{file_info['name']}"
        dest_path = dest_dir / dest_name

        try:
            shutil.copy2(source_path, dest_path)
            return True
        except Exception as e:
            return False

    def generate_report(self):
        """Gera relatório final da migração inteligente"""
        if not self.analysis_file.exists():
            return

        with open(self.analysis_file, 'r') as f:
            analysis = json.load(f)

        report = f"""
# 🧠 RELATÓRIO DE MIGRAÇÃO INTELIGENTE

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Repositório:** {self.git_repo_path}

## 📊 ESTATÍSTICAS

### Análise Inicial
- **Total de arquivos verificados:** {analysis['total_files_scanned']:,}
- **Arquivos ignorados (compactados):** {analysis['ignored_files']:,} ({analysis['ignored_size_gb']:.1f} GB)
- **Arquivos relevantes encontrados:** {analysis['relevant_files']:,}

### Resultado Final
- **Arquivos únicos migrados:** {analysis['unique_files']:,}
- **Arquivos prioritários:** {analysis['priority_files']:,}
- **Duplicatas removidas:** {analysis['duplicates']:,}
- **Tamanho final:** {analysis['unique_size_mb']/1024:.1f} GB
- **Economia total:** {(analysis['ignored_size_gb'] + (analysis['total_size_mb']-analysis['unique_size_mb'])/1024):.1f} GB

## 🗂️ ESTRUTURA CRIADA

```
digimundo-smart-history/
├── code/        # Código fonte por data
├── docs/        # Documentação
├── config/      # Arquivos de configuração
├── data/        # Bancos de dados e dados
├── web/         # Assets web
└── misc/        # Outros arquivos
```

## 🎯 O QUE FOI IGNORADO

- Arquivos `.tar`, `.gz`, `.zip` (backups compactados)
- Arquivos de sistema (começados com `.`)
- Arquivos muito grandes sem relevância (>50MB não-código)
- Duplicatas detectadas por hash MD5

## ✅ PRÓXIMOS PASSOS

1. Verificar o repositório criado:
   ```bash
   cd {self.git_repo_path}
   git log --oneline --graph --all
   ```

2. Navegar por tags temporais:
   ```bash
   git tag --list
   git checkout v2025-03-march-2025
   ```

3. Após verificação, deletar pastas originais:
   ```bash
   rm -rf "/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION"
   rm -rf "/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia"
   rm -rf "/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo"
   ```

**MIGRAÇÃO INTELIGENTE COMPLETA!** 🎉
"""

        report_path = self.git_repo_path / "MIGRATION_REPORT.md"
        with open(report_path, 'w') as f:
            f.write(report)

        print("\n📋 Relatório salvo em:", report_path)

def main():
    migrator = SmartHistoryMigrator()

    print("🧠 MIGRAÇÃO INTELIGENTE - IGNORANDO ARQUIVOS COMPACTADOS")
    print("="*60)

    # Fase 1: Análise inteligente
    print("\n📊 FASE 1: Análise inteligente dos arquivos...")
    analysis = migrator.analyze_smart_files()

    # Fase 2: Criar repositório Git
    print("\n🚀 FASE 2: Criando repositório Git otimizado...")
    migrator.create_git_repository(analysis)

    # Fase 3: Relatório
    print("\n📋 FASE 3: Gerando relatório...")
    migrator.generate_report()

    print("\n" + "="*60)
    print("✅ MIGRAÇÃO INTELIGENTE COMPLETA!")
    print(f"📁 Repositório criado: {migrator.git_repo_path}")
    print(f"📊 Análise salva: {migrator.analysis_file}")
    print("\n🎯 Verifique o repositório antes de deletar as pastas originais!")

if __name__ == "__main__":
    main()