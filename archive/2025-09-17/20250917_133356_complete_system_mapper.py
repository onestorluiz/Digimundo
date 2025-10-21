#!/usr/bin/env python3
"""
🗺️ COMPLETE SYSTEM MAPPER
==========================
Mapeia TODO o sistema para criar memória completa para Claude
"""

import os
import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
import hashlib

class CompleteSystemMapper:
    """Mapeia completamente o sistema ScriptureMonChampion"""

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.system_map = {
            'modules': {},
            'generators': [],
            'test_files': [],
            'config_files': [],
            'data_directories': [],
            'important_patterns': {},
            'entry_points': [],
            'dependencies': defaultdict(list)
        }

    def analyze_python_file(self, file_path: Path) -> Dict:
        """Analisa um arquivo Python completamente"""
        info = {
            'path': str(file_path.relative_to(self.root)),
            'size': file_path.stat().st_size,
            'purpose': None,
            'imports': [],
            'classes': [],
            'functions': [],
            'generates_files': False,
            'entry_point': False,
            'test_file': False,
            'dependencies': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extrair docstring do módulo
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            if docstring:
                info['purpose'] = docstring.split('\n')[0]

            # Analisar AST
            for node in ast.walk(tree):
                # Imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        info['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        info['imports'].append(node.module)

                # Classes
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'methods': []
                    }
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append(item.name)
                    info['classes'].append(class_info)

                # Functions
                elif isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'docstring': ast.get_docstring(node)
                    }
                    info['functions'].append(func_info)

            # Detectar se é gerador de arquivos
            generators_patterns = [
                'open.*w',
                'write',
                'dump',
                'save',
                'create_file',
                'generate'
            ]

            for pattern in generators_patterns:
                if pattern in content:
                    info['generates_files'] = True
                    break

            # Detectar entry points
            if 'if __name__ == "__main__"' in content or 'def main(' in content:
                info['entry_point'] = True

            # Detectar test files
            if 'test_' in file_path.name or '/tests/' in str(file_path):
                info['test_file'] = True

        except Exception as e:
            info['error'] = str(e)

        return info

    def map_directory_structure(self) -> Dict:
        """Mapeia estrutura completa de diretórios"""
        structure = {}

        for item in self.root.rglob("*"):
            if '.git' in str(item) or '__pycache__' in str(item):
                continue

            rel_path = item.relative_to(self.root)
            parts = rel_path.parts

            current = structure
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            if item.is_file():
                current[parts[-1]] = "file"
            else:
                if parts[-1] not in current:
                    current[parts[-1]] = {}

        return structure

    def find_important_files(self) -> Dict:
        """Identifica arquivos importantes do sistema"""
        important = {
            'main_systems': [],
            'memory_systems': [],
            'digilang_versions': [],
            'cli_interfaces': [],
            'api_endpoints': [],
            'config_files': [],
            'documentation': []
        }

        for py_file in self.root.rglob("*.py"):
            name = py_file.name.lower()
            path_str = str(py_file)

            # Sistemas principais
            if 'unified' in name or 'manager' in name or 'orchestrator' in name:
                important['main_systems'].append(str(py_file.relative_to(self.root)))

            # Sistemas de memória
            if 'memory' in name or 'crystal' in name:
                important['memory_systems'].append(str(py_file.relative_to(self.root)))

            # Versões do DigiLang
            if 'digilang' in name:
                important['digilang_versions'].append(str(py_file.relative_to(self.root)))

            # CLIs
            if 'cli' in name or 'champion' in name:
                important['cli_interfaces'].append(str(py_file.relative_to(self.root)))

            # APIs
            if 'api' in name or 'endpoint' in name:
                important['api_endpoints'].append(str(py_file.relative_to(self.root)))

        # Config files
        for config_file in self.root.rglob("*.json"):
            important['config_files'].append(str(config_file.relative_to(self.root)))

        # Documentation
        for doc_file in self.root.rglob("*.md"):
            important['documentation'].append(str(doc_file.relative_to(self.root)))

        return important

    def analyze_dependencies(self) -> Dict:
        """Analisa dependências entre módulos"""
        dependencies = defaultdict(list)

        for py_file in self.root.rglob("*.py"):
            if '.bak' in str(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Procurar imports internos
                import_patterns = [
                    'from apps.scripturemon',
                    'from deployments',
                    'import apps',
                    'from scripts'
                ]

                for pattern in import_patterns:
                    if pattern in content:
                        dependencies[str(py_file.relative_to(self.root))].append(pattern)

            except:
                pass

        return dict(dependencies)

    def generate_complete_map(self) -> Dict:
        """Gera mapeamento completo do sistema"""
        print("🗺️ MAPEANDO SISTEMA COMPLETO...")
        print("="*60)

        # 1. Estrutura de diretórios
        print("\n📂 Mapeando estrutura de diretórios...")
        structure = self.map_directory_structure()

        # 2. Arquivos importantes
        print("📍 Identificando arquivos importantes...")
        important = self.find_important_files()

        # 3. Análise detalhada de cada Python file
        print("🔍 Analisando arquivos Python...")
        modules = {}
        generators = []
        entry_points = []

        py_files = list(self.root.rglob("*.py"))
        for i, py_file in enumerate(py_files):
            if '.bak' in str(py_file):
                continue

            if i % 50 == 0:
                print(f"  Processando {i}/{len(py_files)}...")

            info = self.analyze_python_file(py_file)
            rel_path = str(py_file.relative_to(self.root))

            modules[rel_path] = info

            if info['generates_files']:
                generators.append(rel_path)

            if info['entry_point']:
                entry_points.append(rel_path)

        # 4. Dependências
        print("🔗 Analisando dependências...")
        dependencies = self.analyze_dependencies()

        # 5. Diretórios de dados
        print("💾 Identificando diretórios de dados...")
        data_dirs = []
        for item in self.root.iterdir():
            if item.is_dir() and item.name in ['data', 'output', 'outputs', 'results', 'backups', 'logs']:
                data_dirs.append(item.name)

        # Compilar tudo
        complete_map = {
            'root': str(self.root),
            'structure_summary': {
                'total_files': len(modules),
                'total_directories': len([d for d in structure if isinstance(structure[d], dict)]),
                'python_files': len([m for m in modules if m.endswith('.py')]),
                'test_files': len([m for m in modules if modules[m]['test_file']]),
                'entry_points': len(entry_points),
                'generators': len(generators)
            },
            'important_files': important,
            'modules': modules,
            'generators': generators,
            'entry_points': entry_points,
            'data_directories': data_dirs,
            'dependencies': dependencies
        }

        return complete_map

    def save_map(self, output_path: Path):
        """Salva o mapa completo"""
        complete_map = self.generate_complete_map()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(complete_map, f, indent=2, default=str)

        print(f"\n✅ Mapa salvo em: {output_path}")
        return complete_map


def main():
    mapper = CompleteSystemMapper()

    # Salvar mapa JSON
    json_path = Path("/Users/clubproducoes/Digimundo/scripturemon-champion/COMPLETE_SYSTEM_MAP.json")
    complete_map = mapper.save_map(json_path)

    # Estatísticas
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO SISTEMA")
    print("="*60)

    stats = complete_map['structure_summary']
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n🎯 ARQUIVOS MAIS IMPORTANTES:")

    print("\n  Sistemas Principais:")
    for sys in complete_map['important_files']['main_systems'][:5]:
        print(f"    - {sys}")

    print("\n  Geradores de Arquivos:")
    for gen in complete_map['generators'][:5]:
        print(f"    - {gen}")

    print("\n  Entry Points:")
    for ep in complete_map['entry_points'][:5]:
        print(f"    - {ep}")

    print("\n✅ Mapeamento completo salvo em COMPLETE_SYSTEM_MAP.json")


if __name__ == "__main__":
    main()