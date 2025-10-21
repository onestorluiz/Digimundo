#!/usr/bin/env python3
"""
Pre-commit Minimalista - Validações essenciais antes do commit
"""

import subprocess
import sys
from pathlib import Path

def check_syntax(files):
    """Verifica sintaxe Python"""
    errors = []
    for file in files:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            errors.append(f"{file}: {result.stderr}")
    return errors

def check_imports(files):
    """Verifica imports básicos"""
    errors = []
    for file in files:
        try:
            with open(file) as f:
                content = f.read()
            compile(content, file, 'exec')
        except ImportError as e:
            errors.append(f"{file}: {e}")
    return errors

def run_tests():
    """Roda testes se existirem"""
    test_dir = Path("tests")
    if test_dir.exists():
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout
    return True, "No tests found"

def main():
    """Hook principal"""
    print("🎯 Pre-commit validation...")

    # Pegar arquivos modificados
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True,
        text=True
    )

    files = [f for f in result.stdout.strip().split('\n') if f.endswith('.py')]

    if not files:
        print("✅ No Python files to check")
        return 0

    # Validações
    all_errors = []

    # 1. Sintaxe
    errors = check_syntax(files)
    if errors:
        print("❌ Syntax errors:")
        for e in errors:
            print(f"  {e}")
        all_errors.extend(errors)

    # 2. Imports
    errors = check_imports(files)
    if errors:
        print("❌ Import errors:")
        for e in errors:
            print(f"  {e}")
        all_errors.extend(errors)

    # 3. Testes (opcional)
    success, output = run_tests()
    if not success:
        print("❌ Tests failed:")
        print(output)
        all_errors.append("Tests failed")

    if all_errors:
        print(f"\n❌ Commit blocked: {len(all_errors)} errors found")
        return 1

    print("✅ All checks passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())