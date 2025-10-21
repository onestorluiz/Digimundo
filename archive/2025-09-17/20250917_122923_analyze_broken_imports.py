#!/usr/bin/env python3
"""
🔍 ANALYZE BROKEN IMPORTS
=========================
Analisa e categoriza os imports quebrados para criar mapeamento
"""

import ast
from pathlib import Path
from collections import defaultdict, Counter
import json

def analyze_broken_imports():
    """Analisa todos os imports quebrados no projeto"""
    print("\n" + "="*80)
    print("🔍 ANALYZING BROKEN IMPORTS")
    print("="*80)

    project_root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")

    # Collect all imports
    all_imports = []
    broken_imports = defaultdict(list)
    import_counts = Counter()

    # Standard library modules
    stdlib = {
        'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing',
        're', 'ast', 'collections', 'itertools', 'functools', 'asyncio',
        'threading', 'subprocess', 'logging', 'hashlib', 'uuid', 'random',
        'math', 'sqlite3', 'pickle', 'zlib', 'gzip', 'base64', 'urllib',
        'multiprocessing', 'concurrent', 'signal', 'warnings', 'copy',
        'dataclasses', 'enum', 'abc', 'weakref', 'inspect', 'traceback'
    }

    # Known third-party modules
    third_party = {
        'numpy', 'pandas', 'scipy', 'sklearn', 'matplotlib', 'seaborn',
        'requests', 'flask', 'django', 'fastapi', 'pytest', 'networkx',
        'nltk', 'spacy', 'transformers', 'torch', 'tensorflow', 'keras',
        'beautifulsoup4', 'selenium', 'pillow', 'opencv-cv', 'msgpack',
        'lz4', 'tiktoken', 'anthropic', 'openai', 'psutil', 'aiofiles'
    }

    # Scan all Python files
    for py_file in project_root.rglob("*.py"):
        if '.bak' in str(py_file) or '__pycache__' in str(py_file):
            continue

        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=str(py_file))

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_name = alias.name
                        all_imports.append(import_name)
                        import_counts[import_name] += 1

                        # Check if it's broken (not stdlib or third-party)
                        base_module = import_name.split('.')[0]
                        if base_module not in stdlib and base_module not in third_party:
                            # Check if it's an internal module that doesn't exist
                            if not (project_root / import_name.replace('.', '/')).exists():
                                if not (project_root / f"{import_name.replace('.', '/')}.py").exists():
                                    broken_imports[import_name].append(str(py_file.relative_to(project_root)))

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        import_name = node.module
                        all_imports.append(import_name)
                        import_counts[import_name] += 1

                        # Check if it's broken
                        base_module = import_name.split('.')[0]
                        if base_module not in stdlib and base_module not in third_party:
                            if not (project_root / import_name.replace('.', '/')).exists():
                                if not (project_root / f"{import_name.replace('.', '/')}.py").exists():
                                    broken_imports[import_name].append(str(py_file.relative_to(project_root)))

        except Exception as e:
            print(f"  ⚠️ Error analyzing {py_file.name}: {e}")

    # Sort broken imports by frequency
    broken_by_frequency = sorted(
        [(module, len(files), files[:3]) for module, files in broken_imports.items()],
        key=lambda x: x[1],
        reverse=True
    )

    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"  • Total unique imports: {len(set(all_imports))}")
    print(f"  • Total broken imports: {len(broken_imports)}")
    print(f"  • Total occurrences: {sum(len(files) for files in broken_imports.values())}")

    print(f"\n🔝 TOP 20 BROKEN IMPORTS:")
    for i, (module, count, example_files) in enumerate(broken_by_frequency[:20], 1):
        print(f"  {i:2}. {module:<50} ({count} occurrences)")
        for file in example_files[:2]:
            print(f"      └─ {file}")

    # Analyze patterns
    patterns = defaultdict(list)
    for module in broken_imports.keys():
        if 'memory' in module.lower():
            patterns['memory_related'].append(module)
        elif 'digilang' in module.lower():
            patterns['digilang_related'].append(module)
        elif 'soul' in module.lower():
            patterns['soul_related'].append(module)
        elif 'quantum' in module.lower():
            patterns['quantum_related'].append(module)
        elif 'crystal' in module.lower():
            patterns['crystal_related'].append(module)
        elif 'telepathic' in module.lower():
            patterns['telepathic_related'].append(module)

    print(f"\n🔍 IMPORT PATTERNS:")
    for pattern, modules in patterns.items():
        print(f"  • {pattern}: {len(modules)} modules")

    # Generate mapping suggestions
    print(f"\n🗺️ SUGGESTED MAPPINGS:")

    # Find existing modules that might be the correct targets
    existing_modules = set()
    for py_file in project_root.rglob("*.py"):
        if '.bak' not in str(py_file) and '__pycache__' not in str(py_file):
            rel_path = py_file.relative_to(project_root)
            module_name = str(rel_path).replace('/', '.').replace('.py', '')
            if module_name.endswith('.__init__'):
                module_name = module_name[:-9]
            existing_modules.add(module_name)

    mappings = {}
    for broken_module in list(broken_imports.keys())[:30]:  # Top 30 broken imports
        # Try to find a similar existing module
        broken_parts = broken_module.split('.')
        candidates = []

        for existing in existing_modules:
            existing_parts = existing.split('.')
            # Check for similar names
            if broken_parts[-1].lower() in existing.lower():
                candidates.append(existing)
            elif len(broken_parts) > 1 and broken_parts[-2:] == existing_parts[-2:]:
                candidates.append(existing)

        if candidates:
            # Pick the most likely candidate
            best = min(candidates, key=lambda x: abs(len(x) - len(broken_module)))
            mappings[broken_module] = best
            print(f"  {broken_module} -> {best}")

    # Save analysis results
    results = {
        'total_broken': len(broken_imports),
        'top_broken': broken_by_frequency[:50],
        'patterns': {k: len(v) for k, v in patterns.items()},
        'suggested_mappings': mappings
    }

    with open(project_root / 'broken_imports_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Analysis saved to broken_imports_analysis.json")
    print("="*80)

    return results

if __name__ == "__main__":
    analyze_broken_imports()