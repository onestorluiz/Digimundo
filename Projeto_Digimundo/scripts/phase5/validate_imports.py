#!/usr/bin/env python3
"""
Validate all imports are correct after refactoring

This script:
1. Scans all .py files
2. Detects broken imports
3. Suggests fixes based on FILE_MANIFEST.yaml
4. Optionally fixes imports automatically

Usage:
    python scripts/phase5/validate_imports.py
    python scripts/phase5/validate_imports.py --fix  # Auto-fix broken imports
    python scripts/phase5/validate_imports.py --file app/services/scene_service.py
"""

import sys
import os
import ast
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import importlib.util


def detect_project_root() -> Path:
    """
    Auto-detect project root (cineprod-flask directory)

    Handles multiple scenarios:
    1. Running from Projeto_Digimundo/ (has cineprod-flask/ subdirectory)
    2. Running from cineprod-flask/ itself
    3. Running from inside cineprod-flask/ subdirectories

    Returns:
        Path to cineprod-flask/ directory
    """
    current = Path.cwd()

    # Scenario 1: Check if we're already in cineprod-flask/
    # (has both app/ and tests/ directories)
    if (current / 'app').exists() and (current / 'tests').exists():
        return current

    # Scenario 2: Check if cineprod-flask/ is a subdirectory
    if (current / 'cineprod-flask').exists():
        cineprod_path = current / 'cineprod-flask'
        if (cineprod_path / 'app').exists():
            return cineprod_path

    # Scenario 3: Check if we're inside cineprod-flask/ and need to navigate up
    if 'cineprod-flask' in str(current):
        temp = current
        while temp.name != 'cineprod-flask' and temp != temp.parent:
            temp = temp.parent
        if temp.name == 'cineprod-flask' and (temp / 'app').exists():
            return temp

    # Fallback: Try to find from script location
    script_parent = Path(__file__).parent.parent.parent
    if (script_parent / 'cineprod-flask').exists():
        return script_parent / 'cineprod-flask'

    # Last resort: assume we're in the right place
    print(f"⚠️  Warning: Could not auto-detect project root from {current}")
    print(f"   Assuming project root is: {current}")
    return current


# Detect project root with auto-detection
project_root = detect_project_root()
sys.path.insert(0, str(project_root))


def extract_imports_from_file(file_path: Path) -> List[Dict]:
    """
    Extract all import statements from a Python file

    Returns:
        List of dicts: [
            {
                'type': 'import' | 'from_import',
                'module': 'app.services.scene_service',
                'names': ['SceneService'],
                'line': 10
            },
            ...
        ]
    """
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read())
    except SyntaxError as e:
        print(f"⚠️  Syntax error in {file_path}: {e}")
        return []

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'type': 'import',
                    'module': alias.name,
                    'names': [alias.asname or alias.name],
                    'line': node.lineno
                })

        elif isinstance(node, ast.ImportFrom):
            if node.module:  # Skip relative imports like "from . import x"
                imports.append({
                    'type': 'from_import',
                    'module': node.module,
                    'names': [alias.name for alias in node.names],
                    'line': node.lineno
                })

    return imports


def validate_import(import_spec: Dict, project_root: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate if an import statement is correct

    Returns:
        (is_valid, error_message)
    """
    module_path = import_spec['module'].replace('.', '/')

    # Check if it's a project import (starts with 'app.')
    if not import_spec['module'].startswith('app.'):
        # External library - assume valid
        return True, None

    # Convert module path to file path
    possible_paths = [
        project_root / f"{module_path}.py",
        project_root / module_path / "__init__.py",
    ]

    # Check if file exists
    for path in possible_paths:
        if path.exists():
            return True, None

    # File doesn't exist
    return False, f"Module not found: {import_spec['module']}"


def scan_all_files(root_dir: Path = None) -> Dict:
    """
    Scan all Python files and validate imports

    Returns:
        {
            'valid': [...],
            'broken': [
                {
                    'file': 'app/services/scene_service.py',
                    'import': {...},
                    'error': 'Module not found: ...'
                },
                ...
            ]
        }
    """
    if root_dir is None:
        root_dir = project_root

    results = {
        'valid': [],
        'broken': []
    }

    # Scan directories
    scan_dirs = [
        'app',
        'tests',
        'celery_tasks',
        'scripts'
    ]

    for scan_dir in scan_dirs:
        scan_path = root_dir / scan_dir

        if not scan_path.exists():
            continue

        for py_file in scan_path.rglob('*.py'):
            # Skip __pycache__, _archived, venv
            rel_path = py_file.relative_to(root_dir)
            rel_path_str = str(rel_path)

            if any(skip in rel_path_str for skip in ['__pycache__', '_archived', '_backup', 'venv', '.venv']):
                continue

            # Extract imports
            imports = extract_imports_from_file(py_file)

            for import_spec in imports:
                is_valid, error = validate_import(import_spec, root_dir)

                if is_valid:
                    results['valid'].append({
                        'file': rel_path_str,
                        'import': import_spec
                    })
                else:
                    results['broken'].append({
                        'file': rel_path_str,
                        'import': import_spec,
                        'error': error
                    })

    return results


def suggest_fix(broken_import: Dict) -> Optional[str]:
    """
    Suggest a fix for a broken import

    Returns:
        Suggested import statement or None
    """
    module = broken_import['import']['module']

    # Common migration patterns
    migrations = {
        'app.services.old_scene_service': 'app.services.scene_service',
        'app.models.old_event': 'app.models.event',
    }

    if module in migrations:
        new_module = migrations[module]
        return f"from {new_module} import {', '.join(broken_import['import']['names'])}"

    # Try to find similar modules
    # (Would need FILE_MANIFEST.yaml integration for better suggestions)

    return None


def format_results(results: Dict) -> str:
    """Format validation results for terminal output"""
    output = []

    output.append("=" * 70)
    output.append("IMPORT VALIDATION RESULTS")
    output.append("=" * 70)

    # Summary
    total_imports = len(results['valid']) + len(results['broken'])
    output.append(f"\nTotal imports checked: {total_imports}")
    output.append(f"✅ Valid:  {len(results['valid'])}")
    output.append(f"❌ Broken: {len(results['broken'])}")

    # Broken imports details
    if results['broken']:
        output.append("\n" + "=" * 70)
        output.append("BROKEN IMPORTS")
        output.append("=" * 70)

        # Group by file
        by_file = {}
        for item in results['broken']:
            file = item['file']
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(item)

        for file, items in sorted(by_file.items()):
            output.append(f"\n📄 {file}:")

            for item in items:
                imp = item['import']
                line = imp['line']
                module = imp['module']
                names = ', '.join(imp['names'])

                output.append(f"  Line {line}: from {module} import {names}")
                output.append(f"          Error: {item['error']}")

                # Suggest fix
                suggestion = suggest_fix(item)
                if suggestion:
                    output.append(f"          💡 Suggested fix: {suggestion}")

    else:
        output.append("\n✅ All imports are valid!")

    output.append("\n" + "=" * 70)

    return "\n".join(output)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate Python imports')
    parser.add_argument('--fix', action='store_true', help='Auto-fix broken imports')
    parser.add_argument('--file', type=str, help='Check specific file only')
    args = parser.parse_args()

    print("🔍 Validating imports...")
    print()

    # Scan files
    if args.file:
        file_path = project_root / args.file
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)

        imports = extract_imports_from_file(file_path)
        results = {'valid': [], 'broken': []}

        for import_spec in imports:
            is_valid, error = validate_import(import_spec, project_root)

            if is_valid:
                results['valid'].append({'file': args.file, 'import': import_spec})
            else:
                results['broken'].append({
                    'file': args.file,
                    'import': import_spec,
                    'error': error
                })
    else:
        results = scan_all_files()

    # Print results
    print(format_results(results))

    # Fix if requested
    if args.fix and results['broken']:
        print("\n🔧 Auto-fix mode enabled (NOT IMPLEMENTED YET)")
        print("   Manual fixes required for now")

    # Exit code
    if results['broken']:
        sys.exit(1)  # Broken imports found
    else:
        sys.exit(0)  # All imports valid


if __name__ == '__main__':
    main()
