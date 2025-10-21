#!/usr/bin/env python3
"""
Detect import cycles in scripturemon-validation
"""
import ast
import os
from pathlib import Path
from typing import Dict, Set, List
import json

PROJECT_ROOT = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")

def extract_imports(file_path: Path) -> Set[str]:
    """Extract all imports from a Python file"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
    except Exception:
        pass
    
    return imports

def build_graph() -> Dict[str, Set[str]]:
    """Build import dependency graph"""
    graph = {}
    
    for py_file in PROJECT_ROOT.rglob("*.py"):
        # Skip backup directories
        if 'backup' in str(py_file).lower():
            continue
        if any(part.startswith('.') or part == '__pycache__' for part in py_file.parts):
            continue
            
        rel_path = py_file.relative_to(PROJECT_ROOT)
        module = str(rel_path.with_suffix('')).replace('/', '.')
        
        imports = extract_imports(py_file)
        internal_imports = set()
        
        for imp in imports:
            # Check if it's an internal import
            if imp.startswith(('apps.', 'src.', 'scripts.', 'tools.')):
                internal_imports.add(imp)
        
        if internal_imports:
            graph[module] = internal_imports
    
    return graph

def find_cycles(graph: Dict[str, Set[str]]) -> List[List[str]]:
    """Find cycles using DFS"""
    cycles = []
    visited = set()
    rec_stack = []
    
    def dfs(node: str):
        if node in rec_stack:
            # Found cycle
            idx = rec_stack.index(node)
            cycle = rec_stack[idx:] + [node]
            cycles.append(cycle)
            return
        
        if node in visited:
            return
        
        visited.add(node)
        rec_stack.append(node)
        
        if node in graph:
            for neighbor in graph[node]:
                dfs(neighbor)
        
        rec_stack.pop()
    
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return cycles

def main():
    print("🔍 Detecting import cycles...")
    
    graph = build_graph()
    cycles = find_cycles(graph)
    
    # Save markdown report
    output_dir = PROJECT_ROOT / "reports" / "fix_current"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "import_cycles.md", 'w') as f:
        f.write("# Import Cycles Report\n\n")
        f.write(f"Total modules analyzed: {len(graph)}\n\n")
        
        if cycles:
            f.write(f"## ⚠️ Found {len(cycles)} cycle(s):\n\n")
            for i, cycle in enumerate(cycles, 1):
                f.write(f"### Cycle {i}\n")
                f.write(" → ".join(cycle) + "\n\n")
        else:
            f.write("## ✅ No import cycles detected!\n\n")
        
        f.write("## Module Graph\n\n")
        f.write(f"Total internal dependencies: {sum(len(deps) for deps in graph.values())}\n")
    
    print(f"📝 Report saved to: reports/fix_current/import_cycles.md")
    
    if cycles:
        print(f"⚠️ Found {len(cycles)} cycle(s)")
    else:
        print("✅ No import cycles detected")
    
    return len(cycles) == 0

if __name__ == "__main__":
    main()