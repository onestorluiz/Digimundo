#!/usr/bin/env python3
"""
🧹 ANÁLISE E LIMPEZA COMPLETA DA RAIZ DO PROJETO
================================================
Identifica todos os arquivos e pastas não utilizados
e organiza movendo para estrutura de backup apropriada
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json
import shutil

class RootCleanupAnalyzer:
    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.analysis_results = {
            'essential': [],
            'backup_files': [],
            'test_files': [],
            'temp_files': [],
            'old_versions': [],
            'unused_directories': [],
            'config_files': [],
            'documentation': []
        }

    def analyze_root_files(self):
        """Analisa todos os arquivos na raiz"""
        print("📊 ANALISANDO ARQUIVOS NA RAIZ")
        print("=" * 60)

        # Arquivos na raiz (não em subdiretórios)
        root_files = [f for f in self.root.iterdir() if f.is_file()]

        for file_path in root_files:
            file_name = file_path.name
            file_size = file_path.stat().st_size / 1024  # KB

            # Classificar arquivo
            category = self.classify_file(file_name)

            file_info = {
                'name': file_name,
                'size_kb': round(file_size, 1),
                'path': str(file_path),
                'category': category
            }

            self.analysis_results[category].append(file_info)

            # Mostrar análise
            emoji = self.get_category_emoji(category)
            print(f"{emoji} {file_name:40} ({file_size:.1f} KB) -> {category}")

    def analyze_directories(self):
        """Analisa diretórios na raiz"""
        print("\n📁 ANALISANDO DIRETÓRIOS NA RAIZ")
        print("=" * 60)

        # Diretórios essenciais do sistema
        essential_dirs = {
            'src', 'tests', 'scripts', 'docs', 'data',
            'bin', 'digilibrary', 'config'
        }

        # Diretórios temporários ou de backup
        temp_backup_dirs = {
            'backups', 'cache', '__pycache__', '.validation_cache',
            'forensic_results', 'legacy', 'benchmark_results',
            '.ast_backups', 'output', 'logs'
        }

        root_dirs = [d for d in self.root.iterdir() if d.is_dir()]

        for dir_path in root_dirs:
            dir_name = dir_path.name

            # Diretórios ocultos (começam com .)
            if dir_name.startswith('.'):
                if dir_name in ['.git', '.claude']:
                    category = 'essential'
                else:
                    category = 'temp_files'
            elif dir_name in essential_dirs:
                category = 'essential'
            elif dir_name in temp_backup_dirs:
                category = 'temp_files'
            elif 'backup' in dir_name.lower() or 'old' in dir_name.lower():
                category = 'backup_files'
            elif 'test' in dir_name.lower():
                category = 'test_files'
            elif dir_name == 'deployments':
                category = 'unused_directories'  # Já identificado como problemático
            elif dir_name == 'apps':
                category = 'unused_directories'  # É um symlink para deployments
            else:
                # Verificar se tem conteúdo relevante
                if self.is_directory_used(dir_path):
                    category = 'essential'
                else:
                    category = 'unused_directories'

            dir_info = {
                'name': dir_name,
                'path': str(dir_path),
                'is_symlink': dir_path.is_symlink(),
                'file_count': len(list(dir_path.rglob('*'))) if not dir_path.is_symlink() else 0
            }

            emoji = self.get_category_emoji(category)
            print(f"{emoji} {dir_name:30} ({'symlink' if dir_info['is_symlink'] else f"{dir_info['file_count']} files"}) -> {category}")

            if category != 'essential':
                self.analysis_results[category].append(dir_info)

    def classify_file(self, filename):
        """Classifica arquivo por tipo"""

        # Arquivos essenciais
        essential_files = {
            'CLAUDE.md', 'README.md', 'requirements.txt',
            'script_doctor.py'
        }

        # Padrões de classificação
        if filename in essential_files:
            return 'essential'
        elif filename.endswith('.backup') or filename.endswith('.bak'):
            return 'backup_files'
        elif filename.endswith('_backup.tar.gz') or 'backup_' in filename:
            return 'backup_files'
        elif filename.startswith('test') or filename.endswith('_test.py'):
            return 'test_files'
        elif filename.startswith('.'):
            return 'config_files'
        elif filename.endswith('.log') or filename.endswith('.txt'):
            return 'temp_files'
        elif filename.endswith('.md'):
            return 'documentation'
        elif '_old' in filename or '_v1' in filename or '_v2' in filename:
            return 'old_versions'
        else:
            return 'essential'  # Por segurança

    def get_category_emoji(self, category):
        """Retorna emoji para categoria"""
        emojis = {
            'essential': '✅',
            'backup_files': '📦',
            'test_files': '🧪',
            'temp_files': '🗑️',
            'old_versions': '📜',
            'unused_directories': '❌',
            'config_files': '⚙️',
            'documentation': '📝'
        }
        return emojis.get(category, '❓')

    def is_directory_used(self, dir_path):
        """Verifica se diretório é usado pelo sistema"""
        # Verificar se tem imports em arquivos Python
        py_files = list(Path(self.root / 'src').rglob('*.py'))
        py_files.extend(list(Path(self.root / 'scripts').rglob('*.py')))

        dir_name = dir_path.name

        for py_file in py_files[:20]:  # Verificar amostra
            try:
                content = py_file.read_text()
                if f'from {dir_name}' in content or f'import {dir_name}' in content:
                    return True
            except:
                pass

        return False

    def generate_cleanup_plan(self):
        """Gera plano de limpeza"""
        print("\n" + "=" * 60)
        print("📋 PLANO DE LIMPEZA PROPOSTO")
        print("=" * 60)

        total_to_move = 0

        # Estrutura de backup proposta
        backup_base = self.root / "Pre_Limpeza_Minimalista"

        cleanup_structure = {
            'backup_files': backup_base / "backups_antigos",
            'test_files': backup_base / "arquivos_teste",
            'temp_files': backup_base / "temporarios",
            'old_versions': backup_base / "versoes_antigas",
            'unused_directories': backup_base / "diretorios_nao_usados",
            'config_files': backup_base / "configs_obsoletos"
        }

        print("\n📦 ARQUIVOS/PASTAS PARA MOVER:\n")

        for category, items in self.analysis_results.items():
            if category == 'essential' or category == 'documentation':
                continue

            if items:
                print(f"\n{self.get_category_emoji(category)} {category.upper().replace('_', ' ')} ({len(items)} items):")

                for item in items[:5]:  # Mostrar primeiros 5
                    if isinstance(item, dict):
                        name = item.get('name', item.get('path'))
                        print(f"  - {name}")

                if len(items) > 5:
                    print(f"  ... e mais {len(items) - 5} items")

                total_to_move += len(items)

        print(f"\n📊 TOTAL PARA MOVER: {total_to_move} items")

        # Salvar plano
        plan = {
            'timestamp': datetime.now().isoformat(),
            'analysis': self.analysis_results,
            'cleanup_structure': {k: str(v) for k, v in cleanup_structure.items()},
            'total_items': total_to_move
        }

        plan_file = self.root / "docs" / "CLEANUP_PLAN_ROOT.json"
        plan_file.write_text(json.dumps(plan, indent=2))
        print(f"\n📄 Plano salvo em: {plan_file}")

        return cleanup_structure

    def create_cleanup_script(self, cleanup_structure):
        """Cria script executável para limpeza"""

        script_content = '''#!/usr/bin/env python3
"""
🧹 SCRIPT DE LIMPEZA EXECUTÁVEL
Gerado automaticamente - Execute para limpar
"""

from pathlib import Path
import shutil

def execute_cleanup():
    root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Criar estrutura de backup
    backup_base = root / "Pre_Limpeza_Minimalista"

    directories = {
        'backup_files': backup_base / "backups_antigos",
        'test_files': backup_base / "arquivos_teste",
        'temp_files': backup_base / "temporarios",
        'old_versions': backup_base / "versoes_antigas",
        'unused_directories': backup_base / "diretorios_nao_usados",
        'config_files': backup_base / "configs_obsoletos"
    }

    # Criar diretórios
    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # Items para mover (gerado automaticamente)
    moves = {
'''

        # Adicionar items para mover
        for category, items in self.analysis_results.items():
            if category in ['essential', 'documentation']:
                continue

            if items and category in cleanup_structure:
                script_content += f"        '{category}': [\n"
                for item in items:
                    if isinstance(item, dict):
                        path = item.get('path', item.get('name'))
                        script_content += f"            '{path}',\n"
                script_content += "        ],\n"

        script_content += '''    }

    # Executar movimentos
    moved = 0
    errors = 0

    for category, paths in moves.items():
        dest_dir = directories.get(category)
        if not dest_dir:
            continue

        for path_str in paths:
            path = Path(path_str)
            if path.exists():
                try:
                    dest = dest_dir / path.name
                    if path.is_dir():
                        shutil.move(str(path), str(dest))
                    else:
                        shutil.move(str(path), str(dest))
                    print(f"✅ Movido: {path.name} -> {dest_dir.name}")
                    moved += 1
                except Exception as e:
                    print(f"❌ Erro ao mover {path.name}: {e}")
                    errors += 1

    print(f"\\n📊 RESULTADO: {moved} movidos, {errors} erros")

if __name__ == "__main__":
    print("🧹 INICIANDO LIMPEZA DA RAIZ")
    print("=" * 60)
    execute_cleanup()
'''

        script_file = self.root / "scripts" / "execute_root_cleanup.py"
        script_file.write_text(script_content)
        script_file.chmod(0o755)

        print(f"\n✅ Script de limpeza criado: {script_file}")
        print("\nPara executar a limpeza:")
        print(f"  python3 {script_file}")

    def run_analysis(self):
        """Executa análise completa"""
        print("\n🔍 ANÁLISE COMPLETA DA RAIZ DO PROJETO")
        print("=" * 60)

        # Analisar arquivos
        self.analyze_root_files()

        # Analisar diretórios
        self.analyze_directories()

        # Gerar plano
        cleanup_structure = self.generate_cleanup_plan()

        # Criar script
        self.create_cleanup_script(cleanup_structure)

        # Resumo final
        print("\n" + "=" * 60)
        print("📊 RESUMO DA ANÁLISE")
        print("=" * 60)

        essential_count = len(self.analysis_results['essential'])
        to_clean = sum(len(items) for cat, items in self.analysis_results.items()
                      if cat not in ['essential', 'documentation'])

        print(f"\n✅ Arquivos/Pastas essenciais: {essential_count}")
        print(f"📝 Documentação: {len(self.analysis_results['documentation'])}")
        print(f"🗑️ Para limpar: {to_clean}")

        # Espaço que será liberado (estimativa)
        total_size_kb = 0
        for category, items in self.analysis_results.items():
            if category in ['essential', 'documentation']:
                continue
            for item in items:
                if isinstance(item, dict) and 'size_kb' in item:
                    total_size_kb += item['size_kb']

        print(f"💾 Espaço a liberar: ~{total_size_kb / 1024:.1f} MB")

        print("\n🎯 PRÓXIMOS PASSOS:")
        print("1. Revisar o plano em docs/CLEANUP_PLAN_ROOT.json")
        print("2. Executar: python3 scripts/execute_root_cleanup.py")
        print("3. Verificar que sistema continua funcionando")
        print("4. Deletar backup se tudo OK após alguns dias")

def main():
    analyzer = RootCleanupAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()