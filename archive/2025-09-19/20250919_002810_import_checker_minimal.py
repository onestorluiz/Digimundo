#!/usr/bin/env python3
"""
Import Checker Minimalista - Detecta imports quebrados e circulares
"""

import ast
from pathlib import Path
from typing import Dict, Set, List

def check_imports(root: str = ".") -> Dict:
    """Analisa imports do projeto"""
    root_path = Path(root)
    imports = {}  # arquivo -> lista de imports
    modules = set()  # módulos que existem

    # Coletar todos os imports e módulos existentes
    for py_file in root_path.rglob("*.py"):
        if '__pycache__' in str(py_file):
            continue

        modules.add(str(py_file.relative_to(root_path))[:-3].replace('/', '.'))

        try:
            with open(py_file) as f:
                tree = ast.parse(f.read())

            file_imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        file_imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    file_imports.append(node.module)

            if file_imports:
                imports[str(py_file.relative_to(root_path))] = file_imports
        except:
            pass

    # Detectar problemas
    problems = {
        'broken': [],
        'circular': [],
        'stats': {'total_files': len(imports), 'total_imports': sum(len(i) for i in imports.values())}
    }

    # Imports quebrados (não são stdlib nem existem no projeto)
    stdlib = {'os', 'sys', 'json', 'time', 'pathlib', 'typing', 're', 'ast',
              'collections', 'itertools', 'functools', 'asyncio', 'threading',
              'subprocess', 'logging', 'math', 'random', 'datetime'}

    for file, file_imports in imports.items():
        for imp in file_imports:
            base = imp.split('.')[0]
            if base not in stdlib and not any(m.startswith(imp) for m in modules):
                problems['broken'].append(f"{file}: {imp}")

    # Detectar circulares simples (A->B->A)
    for file_a, imports_a in imports.items():
        module_a = file_a[:-3].replace('/', '.')
        for imp in imports_a:
            if imp in modules:
                file_b = imp.replace('.', '/') + '.py'
                if file_b in imports:
                    if module_a in imports[file_b]:
                        cycle = sorted([module_a, imp])
                        if cycle not in problems['circular']:
                            problems['circular'].append(cycle)

    return problems

def main():
    """Executa análise e mostra resultado"""
    print("🔍 Analisando imports...")
    result = check_imports("/Users/clubproducoes/Digimundo/scripturemon-champion")

    print(f"\n📊 Estatísticas:")
    print(f"  • Arquivos: {result['stats']['total_files']}")
    print(f"  • Imports: {result['stats']['total_imports']}")

    if result['broken']:
        print(f"\n❌ Imports quebrados ({len(result['broken'])}):")
        for imp in result['broken'][:10]:  # Mostrar apenas 10
            print(f"  • {imp}")

    if result['circular']:
        print(f"\n🔄 Dependências circulares ({len(result['circular'])}):")
        for cycle in result['circular'][:5]:  # Mostrar apenas 5
            print(f"  • {' <-> '.join(cycle)}")

if __name__ == "__main__":
    main()