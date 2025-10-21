#!/usr/bin/env python3
"""
🔧 FIX IMPORTS AUTOMATICALLY
=============================
Corrige imports quebrados automaticamente baseado em mapeamento inteligente
"""

import ast
import os
from pathlib import Path
from typing import Dict, Set, Tuple
import json
import shutil

class ImportFixer:
    """Sistema inteligente de correção de imports"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

        # Mapeamento de correções conhecidas
        self.import_mapping = {
            # Bibliotecas Python que precisam ser instaladas
            'pdfplumber': '__INSTALL__',
            'PyPDF2': '__INSTALL__',
            'aiohttp': '__INSTALL__',
            'qiskit': '__INSTALL__',

            # Bibliotecas padrão do Python que não foram importadas corretamente
            'gc': '__STDLIB__',
            'struct': '__STDLIB__',
            'shutil': '__STDLIB__',
            'mmap': '__STDLIB__',
            'lzma': '__STDLIB__',
            'contextlib': '__STDLIB__',
            'queue': '__STDLIB__',
            'importlib': '__STDLIB__',
            'difflib': '__STDLIB__',
            'heapq': '__STDLIB__',
            'resource': '__STDLIB__',
            '__future__': '__FUTURE__',

            # Imports internos que precisam ser ajustados
            'config_silicon_valley': 'apps.scripturemon.config_silicon_valley',
            'vocab_schema': 'apps.scripturemon.digilang_advanced.vocab_schema',
            'tokenizer_utils': 'apps.scripturemon.digilang.tokenizer_utils',
            'memory_federation': 'apps.scripturemon.memory_systems.memory_federation',
            'ollama': '__COMMENT__',  # Comentar pois é ferramenta externa

            # Imports de módulos depreciados - redirecionar para versões atuais
            'apps.scripturemon.crystal_memory': 'apps.scripturemon.screenplay_crystal_memory',
            'apps.scripturemon.digilang_v7_ultimate': 'apps.scripturemon.deprecated_versions.digilang_v7_ultimate',
            'apps.scripturemon.digilang_v8_1_supreme': 'apps.scripturemon.deprecated_versions.digilang_v8_1_supreme',
            'apps.scripturemon.digilang_v9_academic': 'apps.scripturemon.deprecated_versions.digilang_v9_academic',
            'apps.scripturemon.digilang_v10_supreme': 'apps.scripturemon.deprecated_versions.digilang_v10_supreme',
            'apps.scripturemon.digilang_v19_personalized': 'apps.scripturemon.deprecated_versions.digilang_v19_personalized',
            'apps.scripturemon.digilang_v20_extreme': 'apps.scripturemon.deprecated_versions.digilang_v20_extreme',
            'apps.scripturemon.digilang_v21_ultimate': 'apps.scripturemon.deprecated_versions.digilang_v21_ultimate',
            'apps.scripturemon.digilang_batman_ultimate': 'apps.scripturemon.deprecated_versions.digilang_batman_ultimate',
            'apps.scripturemon.digilang_val_integration': 'apps.scripturemon.deprecated_versions.digilang_val_integration',
            'apps.scripturemon.digilang_hybrid': 'apps.scripturemon.deprecated_versions.digilang_hybrid',

            # Mapeamentos do sistema integrado
            'integrated_validation_system': 'apps.scripturemon.integrated_validation_system',
            'ast_based_refactoring': 'ast_based_refactoring',
            'import_dependency_manager': 'import_dependency_manager',
            'async_await_validator': 'async_await_validator',
            'precommit_validation_hooks': 'precommit_validation_hooks',
        }

        # Criar diretório de versões depreciadas se não existir
        self.deprecated_dir = self.project_root / 'apps' / 'scripturemon' / 'deprecated_versions'
        self.deprecated_dir.mkdir(parents=True, exist_ok=True)

        self.stats = {
            'files_processed': 0,
            'imports_fixed': 0,
            'imports_commented': 0,
            'libraries_to_install': set(),
            'errors': []
        }

    def fix_all_imports(self, dry_run: bool = True) -> Dict:
        """Corrige todos os imports quebrados"""
        print("\n" + "="*80)
        print("🔧 FIXING IMPORTS AUTOMATICALLY")
        print("="*80)
        print(f"  Mode: {'DRY RUN' if dry_run else 'APPLYING FIXES'}")

        # Processar todos os arquivos Python
        for py_file in self.project_root.rglob("*.py"):
            if '.bak' in str(py_file) or '__pycache__' in str(py_file):
                continue

            self._fix_file_imports(py_file, dry_run)

        # Relatório final
        self._print_report()

        return self.stats

    def _fix_file_imports(self, file_path: Path, dry_run: bool) -> bool:
        """Corrige imports em um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Parse AST
            tree = ast.parse(original_content, filename=str(file_path))

            # Transform imports
            transformer = ImportTransformer(self.import_mapping, self.stats)
            new_tree = transformer.visit(tree)

            # Generate new code
            try:
                new_content = ast.unparse(new_tree)
            except:
                # Fallback para Python < 3.9
                new_content = self._manual_fix_imports(original_content, transformer.fixes)

            # Check if changes were made
            if new_content != original_content and transformer.fixes:
                if not dry_run:
                    # Backup
                    backup_path = file_path.with_suffix('.py.import_bak')
                    shutil.copy2(file_path, backup_path)

                    # Write fixed content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"  ✅ Fixed {len(transformer.fixes)} imports in {file_path.name}")
                else:
                    print(f"  Would fix {len(transformer.fixes)} imports in {file_path.name}")

                self.stats['files_processed'] += 1
                self.stats['imports_fixed'] += len(transformer.fixes)
                return True

        except Exception as e:
            self.stats['errors'].append(f"{file_path.name}: {e}")
            return False

        return False

    def _manual_fix_imports(self, content: str, fixes: list) -> str:
        """Correção manual de imports para Python < 3.9"""
        lines = content.split('\n')

        for fix in fixes:
            for i, line in enumerate(lines):
                if fix['old'] in line:
                    if fix['type'] == 'replace':
                        lines[i] = line.replace(fix['old'], fix['new'])
                    elif fix['type'] == 'comment':
                        if not line.strip().startswith('#'):
                            lines[i] = f"# {line}  # Commented: external dependency"

        return '\n'.join(lines)

    def _print_report(self):
        """Imprime relatório de correções"""
        print("\n" + "="*60)
        print("📊 IMPORT FIX REPORT:")
        print("="*60)
        print(f"  • Files processed: {self.stats['files_processed']}")
        print(f"  • Imports fixed: {self.stats['imports_fixed']}")
        print(f"  • Imports commented: {self.stats['imports_commented']}")

        if self.stats['libraries_to_install']:
            print(f"\n📦 LIBRARIES TO INSTALL:")
            for lib in sorted(self.stats['libraries_to_install']):
                print(f"  pip install {lib}")

        if self.stats['errors']:
            print(f"\n⚠️ ERRORS ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"  • {error}")

        print("="*60)


class ImportTransformer(ast.NodeTransformer):
    """Transforma imports usando mapeamento"""

    def __init__(self, mapping: Dict[str, str], stats: Dict):
        self.mapping = mapping
        self.stats = stats
        self.fixes = []

    def visit_Import(self, node: ast.Import):
        """Visita import statements"""
        self.generic_visit(node)

        new_names = []
        for alias in node.names:
            mapped = self.mapping.get(alias.name)

            if mapped == '__INSTALL__':
                # Biblioteca precisa ser instalada
                self.stats['libraries_to_install'].add(alias.name)
                new_names.append(alias)
            elif mapped == '__STDLIB__':
                # Biblioteca padrão, manter
                new_names.append(alias)
            elif mapped == '__COMMENT__':
                # Comentar import
                self.stats['imports_commented'] += 1
                self.fixes.append({
                    'type': 'comment',
                    'old': f"import {alias.name}",
                    'new': f"# import {alias.name}"
                })
            elif mapped:
                # Substituir import
                new_alias = ast.alias(name=mapped, asname=alias.asname)
                new_names.append(new_alias)
                self.fixes.append({
                    'type': 'replace',
                    'old': f"import {alias.name}",
                    'new': f"import {mapped}"
                })
            else:
                new_names.append(alias)

        node.names = new_names
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Visita from...import statements"""
        self.generic_visit(node)

        if node.module:
            mapped = self.mapping.get(node.module)

            if mapped == '__INSTALL__':
                self.stats['libraries_to_install'].add(node.module)
            elif mapped == '__STDLIB__':
                pass  # Manter como está
            elif mapped == '__COMMENT__':
                self.stats['imports_commented'] += 1
                self.fixes.append({
                    'type': 'comment',
                    'old': f"from {node.module}",
                    'new': f"# from {node.module}"
                })
            elif mapped == '__FUTURE__':
                # Manter imports from __future__
                pass
            elif mapped:
                old_module = node.module
                node.module = mapped
                self.fixes.append({
                    'type': 'replace',
                    'old': f"from {old_module}",
                    'new': f"from {mapped}"
                })

        return node


def main():
    """Função principal"""
    project_root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Criar instância do fixer
    fixer = ImportFixer(project_root)

    # Primeiro fazer dry run
    print("\n🔍 PHASE 1: DRY RUN")
    stats_dry = fixer.fix_all_imports(dry_run=True)

    # Perguntar se quer aplicar
    print("\n" + "="*60)
    print(f"Ready to fix {stats_dry['imports_fixed']} imports in {stats_dry['files_processed']} files.")
    response = input("Apply fixes? (y/n): ")

    if response.lower() == 'y':
        # Reset stats
        fixer.stats = {
            'files_processed': 0,
            'imports_fixed': 0,
            'imports_commented': 0,
            'libraries_to_install': set(),
            'errors': []
        }

        # Aplicar correções
        print("\n✅ PHASE 2: APPLYING FIXES")
        stats_real = fixer.fix_all_imports(dry_run=False)

        print("\n✅ IMPORT FIXES APPLIED SUCCESSFULLY!")

        # Salvar relatório
        with open(project_root / 'import_fixes_report.json', 'w') as f:
            json.dump({
                'files_processed': stats_real['files_processed'],
                'imports_fixed': stats_real['imports_fixed'],
                'imports_commented': stats_real['imports_commented'],
                'libraries_to_install': list(stats_real['libraries_to_install']),
                'errors': stats_real['errors']
            }, f, indent=2)

        print(f"💾 Report saved to import_fixes_report.json")
    else:
        print("\n❌ Fixes not applied.")


if __name__ == "__main__":
    main()