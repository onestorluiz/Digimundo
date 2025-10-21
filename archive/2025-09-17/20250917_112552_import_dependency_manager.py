#!/usr/bin/env python3
"""
📦 IMPORT DEPENDENCY MANAGER
============================
Gerencia e atualiza imports automaticamente
Detecta dependências circulares e imports quebrados
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import networkx as nx
import json
import time


@dataclass
class ImportInfo:
    """Informação sobre um import"""
    module: str
    names: List[str]
    alias: Optional[str] = None
    level: int = 0  # For relative imports
    line: int = 0
    is_from: bool = False
    

@dataclass
class ModuleInfo:
    """Informação sobre um módulo"""
    path: Path
    name: str
    imports: List[ImportInfo] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    

class ImportDependencyManager:
    """Gerenciador de dependências de imports"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.module_map: Dict[str, ModuleInfo] = {}
        self.import_graph = nx.DiGraph()
        self.circular_dependencies: List[List[str]] = []
        self.broken_imports: Dict[str, List[str]] = defaultdict(list)
        self.stats = {
            'modules_analyzed': 0,
            'total_imports': 0,
            'circular_deps_found': 0,
            'broken_imports_found': 0,
            'auto_fixes_applied': 0
        }
        
    def analyze_project(self) -> Dict[str, Any]:
        """Analisa todo o projeto"""
        print("\n📦 ANALYZING IMPORT DEPENDENCIES")
        print("="*60)
        
        # Scan all Python files
        for py_file in self.project_root.rglob("*.py"):
            if '.bak' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            self._analyze_module(py_file)
            
        # Build dependency graph
        self._build_dependency_graph()
        
        # Find circular dependencies
        self._find_circular_dependencies()
        
        # Find broken imports
        self._find_broken_imports()
        
        return self.get_report()
    
    def _analyze_module(self, file_path: Path) -> Optional[ModuleInfo]:
        """Analisa um módulo Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content, filename=str(file_path))
            
            # Get module name from path
            module_name = self._path_to_module_name(file_path)
            
            module_info = ModuleInfo(
                path=file_path,
                name=module_name
            )
            
            # Analyze imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_info = ImportInfo(
                            module=alias.name,
                            names=[alias.name],
                            alias=alias.asname,
                            line=node.lineno,
                            is_from=False
                        )
                        module_info.imports.append(import_info)
                        module_info.dependencies.add(alias.name)
                        
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        names = [n.name for n in node.names]
                        import_info = ImportInfo(
                            module=node.module,
                            names=names,
                            level=node.level or 0,
                            line=node.lineno,
                            is_from=True
                        )
                        module_info.imports.append(import_info)
                        module_info.dependencies.add(node.module)
                        
                # Find exports (classes and functions)
                elif isinstance(node, ast.ClassDef):
                    module_info.exports.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    module_info.exports.append(node.name)
            
            self.module_map[module_name] = module_info
            self.stats['modules_analyzed'] += 1
            self.stats['total_imports'] += len(module_info.imports)
            
            return module_info
            
        except Exception as e:
            print(f"  ⚠️ Error analyzing {file_path}: {e}")
            return None
    
    def _path_to_module_name(self, file_path: Path) -> str:
        """Converte path para nome de módulo"""
        try:
            rel_path = file_path.relative_to(self.project_root)
            parts = list(rel_path.parts)
            
            # Remove .py extension
            if parts[-1].endswith('.py'):
                parts[-1] = parts[-1][:-3]
            
            # Handle __init__.py
            if parts[-1] == '__init__':
                parts = parts[:-1]
            
            return '.'.join(parts)
        except:
            return str(file_path.stem)
    
    def _build_dependency_graph(self):
        """Constrói grafo de dependências"""
        for module_name, module_info in self.module_map.items():
            self.import_graph.add_node(module_name)
            
            for dep in module_info.dependencies:
                # Try to resolve internal dependencies
                resolved = self._resolve_import(module_name, dep)
                if resolved in self.module_map:
                    self.import_graph.add_edge(module_name, resolved)
    
    def _resolve_import(self, from_module: str, import_name: str) -> str:
        """Resolve nome de import para módulo real"""
        # Try direct match
        if import_name in self.module_map:
            return import_name
        
        # Try relative to current module
        parts = from_module.split('.')
        if len(parts) > 1:
            parent = '.'.join(parts[:-1])
            relative = f"{parent}.{import_name}"
            if relative in self.module_map:
                return relative
        
        # Try common patterns
        if 'apps.scripturemon' not in import_name:
            full_name = f"apps.scripturemon.{import_name}"
            if full_name in self.module_map:
                return full_name
        
        return import_name
    
    def _find_circular_dependencies(self):
        """Encontra dependências circulares"""
        try:
            cycles = list(nx.simple_cycles(self.import_graph))
            self.circular_dependencies = cycles
            self.stats['circular_deps_found'] = len(cycles)
            
            if cycles:
                print(f"\n🔄 Found {len(cycles)} circular dependencies:")
                for i, cycle in enumerate(cycles[:5], 1):  # Show first 5
                    print(f"  {i}. {' -> '.join(cycle)} -> {cycle[0]}")
        except:
            pass
    
    def _find_broken_imports(self):
        """Encontra imports quebrados"""
        for module_name, module_info in self.module_map.items():
            for import_info in module_info.imports:
                # Check if import can be resolved
                resolved = self._resolve_import(module_name, import_info.module)
                
                # Check against known modules
                if resolved not in self.module_map:
                    # Check if it's a standard library or third-party
                    if not self._is_standard_or_third_party(import_info.module):
                        self.broken_imports[module_name].append(import_info.module)
                        self.stats['broken_imports_found'] += 1
    
    def _is_standard_or_third_party(self, module: str) -> bool:
        """Verifica se é biblioteca padrão ou third-party"""
        standard_libs = {
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing',
            're', 'ast', 'collections', 'itertools', 'functools', 'asyncio',
            'threading', 'subprocess', 'logging', 'hashlib', 'uuid', 'random',
            'math', 'sqlite3', 'pickle', 'zlib', 'gzip', 'base64', 'urllib'
        }
        
        third_party = {
            'numpy', 'pandas', 'scipy', 'sklearn', 'matplotlib', 'seaborn',
            'requests', 'flask', 'django', 'fastapi', 'pytest', 'networkx',
            'nltk', 'spacy', 'transformers', 'torch', 'tensorflow', 'keras',
            'beautifulsoup4', 'selenium', 'pillow', 'opencv-cv', 'msgpack',
            'lz4', 'tiktoken', 'anthropic', 'openai'
        }
        
        base_module = module.split('.')[0]
        return base_module in standard_libs or base_module in third_party
    
    def auto_fix_imports(self, dry_run: bool = True) -> int:
        """Tenta corrigir imports automaticamente"""
        fixes_applied = 0
        
        print("\n🔧 AUTO-FIXING BROKEN IMPORTS")
        print("="*60)
        
        # Known fixes
        import_fixes = {
            'DigionProducermonOrchestrator': 'DigionProducerMonOrchestrator',
            'persistent_memory_system_system_system': 'persistent_memory_system_system_system_system',
            'memory_simple': 'memory_systems.memory_simple',
            'memory_brain': 'memory_systems.memory_brain'
        }
        
        for module_name, broken_imports in self.broken_imports.items():
            if module_name not in self.module_map:
                continue
                
            module_info = self.module_map[module_name]
            file_path = module_info.path
            
            fixes_for_file = []
            for broken in broken_imports:
                if broken in import_fixes:
                    fixes_for_file.append((broken, import_fixes[broken]))
            
            if fixes_for_file and not dry_run:
                if self._apply_import_fixes(file_path, fixes_for_file):
                    fixes_applied += len(fixes_for_file)
                    print(f"  ✅ Fixed {len(fixes_for_file)} imports in {file_path.name}")
        
        self.stats['auto_fixes_applied'] = fixes_applied
        return fixes_applied
    
    def _apply_import_fixes(self, file_path: Path, fixes: List[Tuple[str, str]]) -> bool:
        """Aplica correções de import em um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply fixes
            for old, new in fixes:
                content = content.replace(f"from {old}", f"from {new}")
                content = content.replace(f"import {old}", f"import {new}")
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        except Exception as e:
            print(f"  ❌ Error fixing {file_path}: {e}")
            return False
    
    def get_report(self) -> Dict[str, Any]:
        """Gera relatório completo"""
        return {
            'stats': self.stats,
            'circular_dependencies': self.circular_dependencies,
            'broken_imports': dict(self.broken_imports),
            'module_count': len(self.module_map),
            'total_dependencies': self.import_graph.number_of_edges()
        }
    
    def visualize_dependencies(self, output_file: str = "import_graph.png"):
        """Visualiza grafo de dependências (requer matplotlib)"""
        try:
            import matplotlib.pyplot as plt
            
            # Create subgraph with only internal modules
            internal_nodes = [n for n in self.import_graph.nodes() if 'apps.scripturemon' in n]
            subgraph = self.import_graph.subgraph(internal_nodes)
            
            # Draw
            pos = nx.spring_layout(subgraph)
            nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', 
                   edge_color='gray', node_size=100, font_size=8)
            
            plt.title("Import Dependency Graph")
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"\n📊 Dependency graph saved to {output_file}")
        except ImportError:
            print("  ⚠️ matplotlib not available for visualization")


def test_import_manager():
    """Testa o Import Dependency Manager"""
    print("\n🧪 TESTING IMPORT DEPENDENCY MANAGER")
    print("="*80)
    
    manager = ImportDependencyManager(
        Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
    )
    
    # Analyze project
    report = manager.analyze_project()
    
    # Print report
    print("\n📊 ANALYSIS REPORT:")
    print(f"  • Modules analyzed: {report['stats']['modules_analyzed']}")
    print(f"  • Total imports: {report['stats']['total_imports']}")
    print(f"  • Circular dependencies: {report['stats']['circular_deps_found']}")
    print(f"  • Broken imports: {report['stats']['broken_imports_found']}")
    
    # Try auto-fix (dry run)
    print("\n🔧 Testing auto-fix (dry run)...")
    fixes = manager.auto_fix_imports(dry_run=True)
    print(f"  Would fix {fixes} imports")
    
    return report


if __name__ == "__main__":
    test_import_manager()