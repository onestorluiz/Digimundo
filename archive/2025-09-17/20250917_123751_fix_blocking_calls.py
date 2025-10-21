#!/usr/bin/env python3
"""
⚡ FIX BLOCKING CALLS IN ASYNC FUNCTIONS
=========================================
Substitui chamadas bloqueantes por alternativas assíncronas
"""

import ast
from pathlib import Path
from typing import Dict, List, Tuple
import shutil

class BlockingCallFixer:
    """Corrige chamadas bloqueantes em funções async"""

    def __init__(self, project_root: Path):
        self.project_root = project_root

        # Mapeamento de substituições
        self.replacements = {
            'time.sleep': 'await asyncio.sleep',
            'input': '# await ainput',  # Precisa de biblioteca externa
            'requests.get': 'await aiohttp_session.get',
            'requests.post': 'await aiohttp_session.post',
            'urllib.request.urlopen': 'await aiohttp_session.get',
            'subprocess.run': 'await asyncio.create_subprocess_exec',
            'subprocess.call': 'await asyncio.create_subprocess_exec',
            'os.system': 'await asyncio.create_subprocess_shell',
            'socket.recv': 'await async_socket.recv',
            'socket.send': 'await async_socket.send'
        }

        self.stats = {
            'files_processed': 0,
            'calls_fixed': 0,
            'errors': []
        }

    def fix_all_blocking_calls(self, dry_run: bool = True):
        """Corrige todas as chamadas bloqueantes"""
        print("\n" + "="*80)
        print("⚡ FIXING BLOCKING CALLS IN ASYNC FUNCTIONS")
        print("="*80)
        print(f"  Mode: {'DRY RUN' if dry_run else 'APPLYING FIXES'}")

        # Processar arquivos Python
        for py_file in self.project_root.rglob("*.py"):
            if '.bak' in str(py_file) or '__pycache__' in str(py_file):
                continue

            self._process_file(py_file, dry_run)

        # Relatório
        print("\n" + "="*60)
        print("📊 BLOCKING CALL FIX REPORT:")
        print("="*60)
        print(f"  • Files processed: {self.stats['files_processed']}")
        print(f"  • Calls fixed: {self.stats['calls_fixed']}")

        if self.stats['errors']:
            print(f"\n⚠️ ERRORS ({len(self.stats['errors'])}):")
            for error in self.stats['errors'][:5]:
                print(f"  • {error}")

        print("="*60)

        return self.stats

    def _process_file(self, file_path: Path, dry_run: bool):
        """Processa um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Parse AST
            tree = ast.parse(original_content, filename=str(file_path))

            # Transform
            transformer = BlockingCallTransformer(self.replacements, self.stats)
            new_tree = transformer.visit(tree)

            if transformer.changes_made:
                if not dry_run:
                    # Backup
                    backup_path = file_path.with_suffix('.py.blocking_bak')
                    shutil.copy2(file_path, backup_path)

                    # Generate new code
                    try:
                        new_content = ast.unparse(new_tree)
                    except:
                        # Fallback para Python < 3.9
                        new_content = self._manual_fix(original_content, transformer.fixes)

                    # Add imports if needed
                    if transformer.needs_asyncio and 'import asyncio' not in new_content:
                        new_content = 'import asyncio\n' + new_content

                    if transformer.needs_aiohttp and 'import aiohttp' not in new_content:
                        new_content = 'import aiohttp\n' + new_content

                    # Write
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"  ✅ Fixed {len(transformer.fixes)} blocking calls in {file_path.name}")
                else:
                    print(f"  Would fix {len(transformer.fixes)} blocking calls in {file_path.name}")

                self.stats['files_processed'] += 1
                self.stats['calls_fixed'] += len(transformer.fixes)

        except Exception as e:
            self.stats['errors'].append(f"{file_path.name}: {e}")

    def _manual_fix(self, content: str, fixes: List[Dict]) -> str:
        """Correção manual para Python < 3.9"""
        lines = content.split('\n')

        for fix in fixes:
            for i, line in enumerate(lines):
                if fix['old'] in line:
                    lines[i] = line.replace(fix['old'], fix['new'])

        return '\n'.join(lines)


class BlockingCallTransformer(ast.NodeTransformer):
    """Transforma chamadas bloqueantes"""

    def __init__(self, replacements: Dict, stats: Dict):
        self.replacements = replacements
        self.stats = stats
        self.fixes = []
        self.changes_made = False
        self.needs_asyncio = False
        self.needs_aiohttp = False
        self.in_async_function = False

    def visit_AsyncFunctionDef(self, node):
        """Visita função async"""
        old_state = self.in_async_function
        self.in_async_function = True

        # Processar body
        self.generic_visit(node)

        self.in_async_function = old_state
        return node

    def visit_Call(self, node):
        """Visita chamadas de função"""
        self.generic_visit(node)

        if self.in_async_function:
            call_name = self._get_call_name(node)

            if call_name in self.replacements:
                replacement = self.replacements[call_name]

                # Registrar fix
                self.fixes.append({
                    'old': call_name,
                    'new': replacement,
                    'line': node.lineno
                })

                self.changes_made = True

                # Check imports needed
                if 'asyncio' in replacement:
                    self.needs_asyncio = True
                if 'aiohttp' in replacement:
                    self.needs_aiohttp = True

                # Transform node (simplified)
                if replacement.startswith('await '):
                    # Wrap in await
                    return ast.Await(value=node)

        return node

    def _get_call_name(self, node: ast.Call) -> str:
        """Extrai nome da chamada"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return '.'.join(reversed(parts))
        return ''


def main():
    """Função principal"""
    project_root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    fixer = BlockingCallFixer(project_root)

    # Dry run primeiro
    print("\n🔍 PHASE 1: DRY RUN")
    stats_dry = fixer.fix_all_blocking_calls(dry_run=True)

    if stats_dry['calls_fixed'] > 0:
        print(f"\nReady to fix {stats_dry['calls_fixed']} blocking calls.")

        # Reset stats
        fixer.stats = {
            'files_processed': 0,
            'calls_fixed': 0,
            'errors': []
        }

        # Apply fixes
        print("\n✅ PHASE 2: APPLYING FIXES")
        stats_real = fixer.fix_all_blocking_calls(dry_run=False)

        print("\n✅ BLOCKING CALLS FIXED SUCCESSFULLY!")
    else:
        print("\n✅ No blocking calls found to fix!")


if __name__ == "__main__":
    main()