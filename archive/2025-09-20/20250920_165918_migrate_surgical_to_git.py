#!/usr/bin/env python3
"""
🔄 MIGRAÇÃO SURGICAL_PRESERVATION → GIT HISTÓRICO INTELIGENTE
Organiza arquivos por datas REAIS de criação/modificação, não por pastas de backup
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import hashlib
import json

class SurgicalToGitMigrator:
    def __init__(self):
        self.surgical_path = Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION")
        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-history")
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/migration_analysis.json")

    def analyze_all_files(self):
        """Analisa TODOS os arquivos por datas reais, ignorando estrutura de pastas"""
        print("🔍 Analisando todos os arquivos por datas reais...")

        file_timeline = []
        duplicate_hashes = {}

        for root, dirs, files in os.walk(self.surgical_path):
            for file in files:
                if file.startswith('.'):
                    continue

                file_path = Path(root) / file
                try:
                    stat = file_path.stat()

                    # Hash para detectar duplicatas
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()

                    file_info = {
                        'path': str(file_path),
                        'name': file,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_birthtime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                        'hash': file_hash,
                        'extension': file_path.suffix.lower(),
                        'relative_path': str(file_path.relative_to(self.surgical_path))
                    }

                    # Detectar duplicatas
                    if file_hash in duplicate_hashes:
                        file_info['is_duplicate'] = True
                        file_info['original'] = duplicate_hashes[file_hash]
                    else:
                        duplicate_hashes[file_hash] = str(file_path)
                        file_info['is_duplicate'] = False

                    file_timeline.append(file_info)

                except Exception as e:
                    print(f"❌ Erro ao analisar {file_path}: {e}")

        # Ordenar por data de criação
        file_timeline.sort(key=lambda x: x['created'])

        # Salvar análise
        analysis = {
            'total_files': len(file_timeline),
            'unique_files': len([f for f in file_timeline if not f['is_duplicate']]),
            'duplicates': len([f for f in file_timeline if f['is_duplicate']]),
            'total_size_mb': sum(f['size'] for f in file_timeline) / (1024*1024),
            'unique_size_mb': sum(f['size'] for f in file_timeline if not f['is_duplicate']) / (1024*1024),
            'timeline': file_timeline,
            'analysis_date': datetime.now().isoformat()
        }

        with open(self.analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"✅ Análise completa:")
        print(f"   📁 Total de arquivos: {analysis['total_files']}")
        print(f"   🔗 Arquivos únicos: {analysis['unique_files']}")
        print(f"   📋 Duplicatas: {analysis['duplicates']}")
        print(f"   💾 Tamanho total: {analysis['total_size_mb']:.1f} MB")
        print(f"   ✨ Tamanho único: {analysis['unique_size_mb']:.1f} MB")
        print(f"   📊 Economia potencial: {analysis['total_size_mb'] - analysis['unique_size_mb']:.1f} MB")

        return analysis

    def create_git_history(self, analysis):
        """Cria repositório Git com histórico cronológico real"""
        print("🚀 Criando repositório Git histórico...")

        # Criar repositório
        if self.git_repo_path.exists():
            shutil.rmtree(self.git_repo_path)

        self.git_repo_path.mkdir()
        os.chdir(self.git_repo_path)

        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Digimundo Archaeologist'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'history@digimundo.dev'], check=True)

        # Organizar arquivos por períodos
        periods = self.group_by_periods(analysis['timeline'])

        for period_name, files in periods.items():
            print(f"📅 Processando período: {period_name}")

            # Copiar arquivos únicos deste período
            unique_files = [f for f in files if not f['is_duplicate']]

            for file_info in unique_files:
                self.copy_file_to_git(file_info)

            if unique_files:
                # Commit do período
                subprocess.run(['git', 'add', '.'], check=True)

                commit_msg = f"{period_name}\n\n"
                commit_msg += f"📁 {len(unique_files)} arquivos únicos\n"
                commit_msg += f"📊 Tamanho: {sum(f['size'] for f in unique_files) / (1024*1024):.1f} MB\n"
                commit_msg += f"📅 Período: {files[0]['created']} → {files[-1]['created']}\n\n"
                commit_msg += "🔗 Arquivos:\n"
                for f in unique_files[:10]:  # Limitar lista
                    commit_msg += f"- {f['name']}\n"
                if len(unique_files) > 10:
                    commit_msg += f"... e mais {len(unique_files) - 10} arquivos\n"

                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)

                # Tag para marco importante
                tag_name = f"v{period_name.lower().replace(' ', '-').replace(':', '')}"
                subprocess.run(['git', 'tag', tag_name], check=True)
                print(f"   🏷️ Tag criada: {tag_name}")

    def group_by_periods(self, timeline):
        """Agrupa arquivos por períodos cronológicos inteligentes"""
        periods = {}

        for file_info in timeline:
            created_date = datetime.fromisoformat(file_info['created'])

            # Agrupar por mês/ano para maior granularidade
            period_key = created_date.strftime("%Y-%m: %B %Y")

            if period_key not in periods:
                periods[period_key] = []

            periods[period_key].append(file_info)

        # Ordenar períodos cronologicamente
        sorted_periods = {}
        for key in sorted(periods.keys()):
            sorted_periods[key] = periods[key]

        return sorted_periods

    def copy_file_to_git(self, file_info):
        """Copia arquivo para estrutura Git organizada"""
        source_path = Path(file_info['path'])

        # Criar estrutura por tipo/extensão
        if file_info['extension'] in ['.py', '.sh', '.js', '.ts']:
            dest_dir = self.git_repo_path / "code"
        elif file_info['extension'] in ['.md', '.txt', '.doc']:
            dest_dir = self.git_repo_path / "docs"
        elif file_info['extension'] in ['.json', '.yaml', '.yml', '.xml']:
            dest_dir = self.git_repo_path / "config"
        elif file_info['extension'] in ['.db', '.sqlite']:
            dest_dir = self.git_repo_path / "data"
        else:
            dest_dir = self.git_repo_path / "misc"

        dest_dir.mkdir(exist_ok=True)

        # Nome único para evitar conflitos
        created_date = datetime.fromisoformat(file_info['created'])
        dest_name = f"{created_date.strftime('%Y%m%d_%H%M%S')}_{file_info['name']}"
        dest_path = dest_dir / dest_name

        try:
            shutil.copy2(source_path, dest_path)
        except Exception as e:
            print(f"⚠️ Erro ao copiar {source_path}: {e}")

    def generate_report(self):
        """Gera relatório final da migração"""
        if not self.analysis_file.exists():
            return

        with open(self.analysis_file, 'r') as f:
            analysis = json.load(f)

        report = f"""
# 📊 RELATÓRIO DE MIGRAÇÃO SURGICAL_PRESERVATION → GIT

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📈 Estatísticas

- **Total de arquivos analisados:** {analysis['total_files']:,}
- **Arquivos únicos:** {analysis['unique_files']:,}
- **Duplicatas removidas:** {analysis['duplicates']:,}
- **Tamanho original:** {analysis['total_size_mb']:.1f} MB
- **Tamanho otimizado:** {analysis['unique_size_mb']:.1f} MB
- **Economia:** {analysis['total_size_mb'] - analysis['unique_size_mb']:.1f} MB ({((analysis['total_size_mb'] - analysis['unique_size_mb']) / analysis['total_size_mb'] * 100):.1f}%)

## 🗂️ Estrutura Git Criada

```
digimundo-history/
├── code/        # Scripts Python, Bash, JS, TS
├── docs/        # Documentação MD, TXT
├── config/      # Arquivos JSON, YAML
├── data/        # Bancos de dados
└── misc/        # Outros arquivos
```

## 🏷️ Tags Cronológicas

Cada período histórico tem uma tag Git para fácil navegação:
- `git tag --list` - Lista todas as tags
- `git checkout v2025-03-prehistory` - Volta para período específico
- `git log --oneline --graph` - Visualiza histórico

## 🔍 Comandos Úteis

```bash
# Navegar para repositório histórico
cd /Users/clubproducoes/Digimundo/digimundo-history

# Ver evolução temporal
git log --oneline --graph --all

# Buscar por conteúdo específico
git log --grep="keyword"

# Comparar períodos
git diff v2025-03-prehistory v2025-09-champion

# Ver arquivos de um período
git ls-tree -r v2025-04-awakening
```
"""

        with open(self.git_repo_path / "MIGRATION_REPORT.md", 'w') as f:
            f.write(report)

        print("📋 Relatório de migração salvo em MIGRATION_REPORT.md")

def main():
    migrator = SurgicalToGitMigrator()

    print("🚀 INICIANDO MIGRAÇÃO SURGICAL_PRESERVATION → GIT HISTÓRICO")
    print("=" * 60)

    # Fase 1: Análise completa
    analysis = migrator.analyze_all_files()

    # Fase 2: Criação do Git histórico
    migrator.create_git_history(analysis)

    # Fase 3: Relatório final
    migrator.generate_report()

    print("=" * 60)
    print("✅ MIGRAÇÃO COMPLETA!")
    print(f"📁 Repositório Git: {migrator.git_repo_path}")
    print(f"📊 Análise detalhada: {migrator.analysis_file}")
    print("\n🎯 Próximo passo: Verificar o repositório histórico criado")

if __name__ == "__main__":
    main()