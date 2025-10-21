#!/usr/bin/env python3
"""
🔄 MIGRAÇÃO COMPLETA HISTÓRIA DIGIMUNDO → GIT UNIFICADO
Processa TODAS as pastas históricas por datas reais, não por estrutura de backup
"""

import os
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import json

class CompleteHistoryMigrator:
    def __init__(self):
        # TODAS as pastas históricas identificadas
        self.historical_paths = [
            Path("/Users/clubproducoes/Digimundo/SURGICAL_PRESERVATION"),
            Path("/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia"),
            Path("/Users/clubproducoes/Digimundo/Pre_Limpeza_Minimalista_Lixo")
        ]

        self.git_repo_path = Path("/Users/clubproducoes/Digimundo/digimundo-complete-history")
        self.analysis_file = Path("/Users/clubproducoes/Digimundo/complete_migration_analysis.json")

    def analyze_all_historical_folders(self):
        """Analisa TODAS as pastas históricas por datas reais"""
        print("🔍 Analisando TODA a história do Digimundo por datas reais...")
        print("📁 Pastas históricas:")
        for path in self.historical_paths:
            if path.exists():
                size = self.get_folder_size(path)
                print(f"   📂 {path.name}: {size:.1f} GB")
            else:
                print(f"   ❌ {path.name}: Não encontrada")

        file_timeline = []
        duplicate_hashes = {}
        total_files = 0
        total_size = 0

        for historical_path in self.historical_paths:
            if not historical_path.exists():
                print(f"⚠️ Pasta não encontrada: {historical_path}")
                continue

            print(f"\n🔍 Processando: {historical_path.name}")
            folder_files = 0
            folder_size = 0

            for root, dirs, files in os.walk(historical_path):
                for file in files:
                    if file.startswith('.') or file == '.DS_Store':
                        continue

                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        file_size = stat.st_size
                        folder_files += 1
                        folder_size += file_size
                        total_files += 1
                        total_size += file_size

                        # Hash para detectar duplicatas globais
                        file_hash = self.calculate_file_hash(file_path)

                        file_info = {
                            'path': str(file_path),
                            'name': file,
                            'size': file_size,
                            'created': datetime.fromtimestamp(stat.st_birthtime).isoformat(),
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                            'hash': file_hash,
                            'extension': file_path.suffix.lower(),
                            'source_folder': historical_path.name,
                            'relative_path': str(file_path.relative_to(historical_path))
                        }

                        # Detectar duplicatas entre TODAS as pastas
                        if file_hash in duplicate_hashes:
                            file_info['is_duplicate'] = True
                            file_info['original'] = duplicate_hashes[file_hash]
                        else:
                            duplicate_hashes[file_hash] = str(file_path)
                            file_info['is_duplicate'] = False

                        file_timeline.append(file_info)

                        # Progresso a cada 1000 arquivos
                        if total_files % 1000 == 0:
                            print(f"   📊 Processados: {total_files:,} arquivos...")

                    except Exception as e:
                        print(f"   ❌ Erro ao analisar {file_path}: {e}")

            print(f"   ✅ {historical_path.name}: {folder_files:,} arquivos, {folder_size/1024/1024:.1f} MB")

        # Ordenar TODA a timeline por data de criação
        print("\n🔄 Ordenando timeline global por datas de criação...")
        file_timeline.sort(key=lambda x: x['created'])

        # Estatísticas globais
        unique_files = [f for f in file_timeline if not f['is_duplicate']]
        duplicates = [f for f in file_timeline if f['is_duplicate']]

        analysis = {
            'scan_date': datetime.now().isoformat(),
            'historical_folders': [str(p) for p in self.historical_paths if p.exists()],
            'total_files': len(file_timeline),
            'unique_files': len(unique_files),
            'duplicates': len(duplicates),
            'total_size_gb': total_size / (1024**3),
            'unique_size_gb': sum(f['size'] for f in unique_files) / (1024**3),
            'earliest_file': file_timeline[0]['created'] if file_timeline else None,
            'latest_file': file_timeline[-1]['created'] if file_timeline else None,
            'timeline': file_timeline
        }

        # Salvar análise completa
        with open(self.analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\n📊 ANÁLISE COMPLETA DA HISTÓRIA DIGIMUNDO:")
        print(f"   📁 Total de arquivos: {analysis['total_files']:,}")
        print(f"   🔗 Arquivos únicos: {analysis['unique_files']:,}")
        print(f"   📋 Duplicatas: {analysis['duplicates']:,}")
        print(f"   💾 Tamanho total: {analysis['total_size_gb']:.1f} GB")
        print(f"   ✨ Tamanho único: {analysis['unique_size_gb']:.1f} GB")
        print(f"   🎯 Economia: {analysis['total_size_gb'] - analysis['unique_size_gb']:.1f} GB ({((analysis['total_size_gb'] - analysis['unique_size_gb']) / analysis['total_size_gb'] * 100):.1f}%)")
        print(f"   📅 Período: {analysis['earliest_file']} → {analysis['latest_file']}")

        return analysis

    def calculate_file_hash(self, file_path):
        """Calcula hash MD5 com tratamento de erro"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            # Para arquivos que não conseguimos ler, usar path como identificador
            return hashlib.md5(str(file_path).encode()).hexdigest()

    def get_folder_size(self, folder_path):
        """Calcula tamanho da pasta em GB"""
        total_size = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    try:
                        file_path = Path(root) / file
                        total_size += file_path.stat().st_size
                    except:
                        continue
        except:
            pass
        return total_size / (1024**3)

    def create_unified_git_history(self, analysis):
        """Cria repositório Git unificado com história cronológica completa"""
        print("\n🚀 Criando repositório Git unificado da história completa...")

        # Criar repositório limpo
        if self.git_repo_path.exists():
            shutil.rmtree(self.git_repo_path)

        self.git_repo_path.mkdir()
        os.chdir(self.git_repo_path)

        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'config', 'user.name', 'Digimundo Time Archaeologist'], check=True)
        subprocess.run(['git', 'config', 'user.email', 'history@digimundo.complete'], check=True)

        # Agrupar por períodos cronológicos inteligentes
        periods = self.group_by_intelligent_periods(analysis['timeline'])

        commit_count = 0
        for period_name, files in periods.items():
            print(f"📅 Processando período: {period_name}")

            # Processar apenas arquivos únicos
            unique_files = [f for f in files if not f['is_duplicate']]

            if not unique_files:
                print(f"   ⚠️ Nenhum arquivo único neste período")
                continue

            # Copiar arquivos para estrutura Git organizada
            files_copied = 0
            for file_info in unique_files:
                try:
                    self.copy_file_to_organized_structure(file_info)
                    files_copied += 1
                except Exception as e:
                    print(f"   ❌ Erro ao copiar {file_info['name']}: {e}")

            if files_copied > 0:
                # Commit do período
                subprocess.run(['git', 'add', '.'], check=True)

                commit_msg = self.generate_commit_message(period_name, unique_files)
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)

                # Tag para marcos importantes
                tag_name = self.generate_tag_name(period_name, commit_count)
                subprocess.run(['git', 'tag', tag_name], check=True)

                commit_count += 1
                print(f"   ✅ Commit criado: {files_copied} arquivos, tag: {tag_name}")

        print(f"\n🎉 Repositório Git criado com {commit_count} commits cronológicos!")

    def group_by_intelligent_periods(self, timeline):
        """Agrupa arquivos por períodos cronológicos inteligentes"""
        periods = {}

        for file_info in timeline:
            created_date = datetime.fromisoformat(file_info['created'])

            # Estratégia híbrida: períodos menores para desenvolvimento intenso
            if created_date.year == 2025 and created_date.month >= 8:
                # Período intenso: agrupar por semana
                week_start = created_date - datetime.timedelta(days=created_date.weekday())
                period_key = f"{created_date.year}-{created_date.month:02d}-W{week_start.day:02d}: Semana {created_date.strftime('%d %b')}"
            else:
                # Período inicial: agrupar por mês
                period_key = f"{created_date.year}-{created_date.month:02d}: {created_date.strftime('%B %Y')}"

            if period_key not in periods:
                periods[period_key] = []

            periods[period_key].append(file_info)

        # Ordenar períodos cronologicamente
        return dict(sorted(periods.items()))

    def copy_file_to_organized_structure(self, file_info):
        """Copia arquivo para estrutura Git organizada por tipo e origem"""
        source_path = Path(file_info['path'])

        # Estrutura: origem/tipo/arquivo
        origin = self.normalize_folder_name(file_info['source_folder'])

        if file_info['extension'] in ['.py', '.sh', '.js', '.ts', '.go', '.rs']:
            type_dir = "code"
        elif file_info['extension'] in ['.md', '.txt', '.doc', '.pdf']:
            type_dir = "docs"
        elif file_info['extension'] in ['.json', '.yaml', '.yml', '.xml', '.toml']:
            type_dir = "config"
        elif file_info['extension'] in ['.db', '.sqlite', '.sql']:
            type_dir = "data"
        elif file_info['extension'] in ['.jpg', '.png', '.gif', '.webp']:
            type_dir = "images"
        else:
            type_dir = "misc"

        dest_dir = self.git_repo_path / origin / type_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Nome com timestamp para evitar conflitos
        created_date = datetime.fromisoformat(file_info['created'])
        dest_name = f"{created_date.strftime('%Y%m%d_%H%M%S')}_{file_info['name']}"
        dest_path = dest_dir / dest_name

        shutil.copy2(source_path, dest_path)

    def normalize_folder_name(self, folder_name):
        """Normaliza nome da pasta para uso no Git"""
        return folder_name.replace(' ', '_').replace('/', '_').lower()

    def generate_commit_message(self, period_name, files):
        """Gera mensagem de commit informativa"""
        total_size = sum(f['size'] for f in files) / (1024*1024)

        # Estatísticas por origem
        origins = {}
        for f in files:
            origin = f['source_folder']
            if origin not in origins:
                origins[origin] = 0
            origins[origin] += 1

        msg = f"{period_name}\n\n"
        msg += f"📁 {len(files)} arquivos únicos ({total_size:.1f} MB)\n"
        msg += f"📅 Período: {files[0]['created']} → {files[-1]['created']}\n\n"

        msg += "📂 Origens:\n"
        for origin, count in origins.items():
            msg += f"   • {origin}: {count} arquivos\n"

        msg += "\n🔗 Principais arquivos:\n"
        for f in files[:5]:  # Top 5
            msg += f"   • {f['name']} ({f['size']/1024:.1f}KB)\n"

        if len(files) > 5:
            msg += f"   ... e mais {len(files) - 5} arquivos\n"

        return msg

    def generate_tag_name(self, period_name, commit_count):
        """Gera nome de tag para o período"""
        # Extrair informações do período
        parts = period_name.split(':')
        period_code = parts[0].replace('-', '').replace('W', 'w').lower()
        return f"v{commit_count:03d}_{period_code}"

    def generate_final_report(self, analysis):
        """Gera relatório final completo"""
        report = f"""
# 📊 RELATÓRIO COMPLETO MIGRAÇÃO HISTÓRIA DIGIMUNDO

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🌌 História Unificada Migrada

### 📂 Pastas Processadas
"""
        for folder in analysis['historical_folders']:
            folder_name = Path(folder).name
            folder_files = len([f for f in analysis['timeline'] if f['source_folder'] == folder_name])
            report += f"- **{folder_name}**: {folder_files:,} arquivos\n"

        report += f"""

### 📈 Estatísticas Globais

- **Total de arquivos analisados:** {analysis['total_files']:,}
- **Arquivos únicos preservados:** {analysis['unique_files']:,}
- **Duplicatas eliminadas:** {analysis['duplicates']:,}
- **Tamanho original:** {analysis['total_size_gb']:.1f} GB
- **Tamanho otimizado:** {analysis['unique_size_gb']:.1f} GB
- **Economia de espaço:** {analysis['total_size_gb'] - analysis['unique_size_gb']:.1f} GB ({((analysis['total_size_gb'] - analysis['unique_size_gb']) / analysis['total_size_gb'] * 100):.1f}%)

### ⏰ Período Histórico
- **Primeiro arquivo:** {analysis['earliest_file']}
- **Último arquivo:** {analysis['latest_file']}

## 🗂️ Estrutura Git Unificada

```
digimundo-complete-history/
├── surgical_preservation/
│   ├── code/        # Scripts e programas
│   ├── docs/        # Documentação
│   ├── config/      # Configurações
│   ├── data/        # Bancos de dados
│   └── misc/        # Outros arquivos
├── digimundo_verdadeira_historia/
│   └── [mesma estrutura]
└── pre_limpeza_minimalista_lixo/
    └── [mesma estrutura]
```

## 🏷️ Sistema de Tags Cronológicas

Cada período possui uma tag Git para navegação temporal:

```bash
# Listar todas as eras
git tag --list

# Voltar para um período específico
git checkout v001_202503

# Ver evolução entre períodos
git diff v001_202503 v050_202509

# Buscar por conteúdo específico
git log --grep="keyword"

# Ver arquivos de uma era
git ls-tree -r v010_202508
```

## 🔍 Comandos de Exploração

```bash
# Navegar para repositório histórico
cd {self.git_repo_path}

# Timeline visual completa
git log --oneline --graph --all --decorate

# Buscar por arquivo específico
git log --follow --patch -- "**/arquivo.py"

# Ver atividade por período
git shortlog --summary --numbered

# Estatísticas por autor/período
git log --pretty=format:"%ad %s" --date=short | head -20

# Encontrar quando arquivo foi criado
git log --diff-filter=A --name-only --pretty=format: | sort -u
```

## 🎯 Vantagens da Migração

1. **Busca Inteligente**: Encontrar qualquer arquivo ou mudança rapidamente
2. **Navegação Temporal**: Voltar para qualquer momento da história
3. **Economia Massiva**: {analysis['total_size_gb'] - analysis['unique_size_gb']:.1f} GB economizados
4. **Estrutura Organizada**: Arquivos categorizados por tipo e origem
5. **Histórico Preservado**: Zero perda de informação histórica
6. **Deduplicação**: Eliminação automática de arquivos repetidos

---

**🎉 DIGIMUNDO HISTORY PRESERVED IN GIT! 🎉**
"""

        with open(self.git_repo_path / "COMPLETE_HISTORY_REPORT.md", 'w') as f:
            f.write(report)

        print("📋 Relatório completo salvo em COMPLETE_HISTORY_REPORT.md")

def main():
    migrator = CompleteHistoryMigrator()

    print("🌌 MIGRAÇÃO COMPLETA DA HISTÓRIA DIGIMUNDO → GIT UNIFICADO")
    print("=" * 70)

    # Fase 1: Análise completa de todas as pastas históricas
    analysis = migrator.analyze_all_historical_folders()

    # Fase 2: Criação do Git histórico unificado
    migrator.create_unified_git_history(analysis)

    # Fase 3: Relatório final
    migrator.generate_final_report(analysis)

    print("=" * 70)
    print("✅ MIGRAÇÃO COMPLETA DA HISTÓRIA DIGIMUNDO!")
    print(f"📁 Repositório Git unificado: {migrator.git_repo_path}")
    print(f"📊 Análise detalhada: {migrator.analysis_file}")
    print(f"💾 Economia total: {analysis['total_size_gb'] - analysis['unique_size_gb']:.1f} GB")
    print("\n🎯 TODA A HISTÓRIA DO DIGIMUNDO AGORA EM GIT!")

if __name__ == "__main__":
    main()