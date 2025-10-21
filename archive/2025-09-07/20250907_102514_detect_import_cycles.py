#!/usr/bin/env python3
"""
Detect import cycles in the codebase.
"""

import ast
import os
from pathlib import Path
from typing import Dict, Set, List, Tuple
import json


def extract_imports(file_path: Path) -> Set[str]:
    """Extract all imports from a Python file."""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return imports


def build_dependency_graph(root_dir: Path) -> Dict[str, Set[str]]:
    """Build dependency graph for all Python files."""
    graph = {}
    
    # Map module names to file paths
    module_map = {}
    
    for py_file in root_dir.rglob("*.py"):
        if any(part.startswith('.') or part == '__pycache__' for part in py_file.parts):
            continue
        if 'backup' in str(py_file).lower():
            continue
            
        rel_path = py_file.relative_to(root_dir)
        module_name = str(rel_path.with_suffix('')).replace('/', '.')
        
        # Store both apps.x and src.x variants
        if module_name.startswith('apps.'):
            module_map[module_name] = py_file
            # Also store without apps prefix for relative imports
            short_name = module_name.replace('apps.', '')
            module_map[short_name] = py_file
        elif module_name.startswith('src.'):
            module_map[module_name] = py_file
            # Also store without src prefix
            short_name = module_name.replace('src.', '')
            module_map[short_name] = py_file
        
    # Build dependency graph
    for module_name, py_file in module_map.items():
        imports = extract_imports(py_file)
        deps = set()
        
        for imp in imports:
            # Check if it's an internal import
            if imp in ['apps', 'src']:
                # These are package roots, need more specific imports
                continue
            if imp in module_map:
                deps.add(imp)
        
        if deps:
            graph[module_name] = deps
    
    return graph


def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find all cycles in the dependency graph using DFS."""
    cycles = []
    visited = set()
    rec_stack = []
    
    def dfs(node: str, path: List[str]):
        if node in rec_stack:
            # Found a cycle
            cycle_start = rec_stack.index(node)
            cycle = rec_stack[cycle_start:] + [node]
            cycles.append(cycle)
            return
        
        if node in visited:
            return
        
        visited.add(node)
        rec_stack.append(node)
        
        if node in graph:
            for neighbor in graph[node]:
                dfs(neighbor, path + [neighbor])
        
        rec_stack.pop()
    
    for node in graph:
        if node not in visited:
            dfs(node, [node])
    
    # Remove duplicate cycles
    unique_cycles = []
    seen = set()
    
    for cycle in cycles:
        # Normalize cycle (start from smallest element)
        min_idx = cycle.index(min(cycle))
        normalized = tuple(cycle[min_idx:] + cycle[:min_idx])
        
        if normalized not in seen:
            seen.add(normalized)
            unique_cycles.append(list(normalized)[:-1])  # Remove duplicate last element
    
    return unique_cycles


def main():
    """Main function to detect import cycles."""
    root_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    
    print("🔍 Building dependency graph...")
    graph = build_dependency_graph(root_dir)
    
    print(f"📊 Found {len(graph)} modules with dependencies")
    
    print("\n🔄 Detecting import cycles...")
    cycles = find_cycles(graph)
    
    result = {
        "total_modules": len(graph),
        "cycles_found": len(cycles),
        "cycles": []
    }
    
    if cycles:
        print(f"\n⚠️  Found {len(cycles)} import cycle(s):\n")
        for i, cycle in enumerate(cycles, 1):
            print(f"Cycle {i}: {' -> '.join(cycle)}")
            result["cycles"].append(cycle)
    else:
        print("\n✅ No import cycles detected!")
    
    # Write results
    output_file = root_dir / "reports" / "fix_current" / "import_cycles.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📝 Results saved to: {output_file}")
    
    return len(cycles) == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)