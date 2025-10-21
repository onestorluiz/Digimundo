# Script de Limpeza Final
import ast
from pathlib import Path

def find_dead_code(base_path: Path):
    dead_functions = []
    for py_file in base_path.glob("**/*.py")[:10]:
        try:
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name.startswith('_unused_'):
                        dead_functions.append(node.name)
        except:
            pass
    return dead_functions

if __name__ == "__main__":
    base = Path(".")
    dead = find_dead_code(base)
    print(f"Found {len(dead)} dead functions")
