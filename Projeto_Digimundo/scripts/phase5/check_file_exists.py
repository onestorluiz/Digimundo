#!/usr/bin/env python3
"""
Check if file exists before creating (prevent duplicates)

Usage:
    python scripts/phase5/check_file_exists.py app/services/new_service.py

Exit Codes:
    0: File doesn't exist (safe to create)
    1: File exists (do NOT create)
"""

import sys
import os
from pathlib import Path
import yaml
from difflib import get_close_matches
from typing import Dict, List, Optional


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


def load_manifest() -> dict:
    """Load FILE_MANIFEST.yaml"""
    # Try multiple locations for FILE_MANIFEST.yaml
    possible_paths = [
        project_root / "docs/fase_5/FILE_MANIFEST.yaml",           # If in cineprod-flask/
        project_root.parent / "docs/fase_5/FILE_MANIFEST.yaml",    # If parent is Projeto_Digimundo/
        Path(__file__).parent.parent.parent / "docs/fase_5/FILE_MANIFEST.yaml"  # From script location
    ]

    for manifest_path in possible_paths:
        if manifest_path.exists():
            with open(manifest_path) as f:
                return yaml.safe_load(f)

    # If not found anywhere, show warning
    print(f"⚠️  Warning: FILE_MANIFEST.yaml not found in any of these locations:")
    for path in possible_paths:
        print(f"   - {path}")
    return {}


def extract_all_file_paths(manifest: dict) -> List[Dict]:
    """
    Extract all file paths from manifest

    Returns:
        List of dicts: [{'path': 'app/...', 'state': 'planned', ...}, ...]
    """
    all_files = []

    for section_key, section_data in manifest.items():
        if section_key in ['metadata', 'totals', 'dependency_graph']:
            continue

        if not isinstance(section_data, dict):
            continue

        for category_key, items in section_data.items():
            if not isinstance(items, list):
                continue

            for item in items:
                if isinstance(item, dict) and 'path' in item:
                    all_files.append(item)

    return all_files


def check_file_exists(file_path: str) -> Dict:
    """
    Check if file exists on filesystem and in manifest

    Returns:
        {
            'exists': bool,
            'path': str,
            'similar_files': list,
            'state_in_manifest': str | None,
            'phase': str | None,
            'deprecated': bool
        }
    """
    # Check filesystem (relative to project_root)
    path = project_root / file_path
    exists_on_disk = path.exists()

    # Check manifest
    manifest = load_manifest()
    all_files = extract_all_file_paths(manifest)

    state_in_manifest = None
    phase = None
    deprecated = False

    for file_spec in all_files:
        if file_spec['path'] == file_path:
            state_in_manifest = file_spec.get('state')
            phase = file_spec.get('phase')
            deprecated = (state_in_manifest == 'deprecated')
            break

    # Find similar files (fuzzy match)
    all_paths = [f['path'] for f in all_files]
    similar = get_close_matches(file_path, all_paths, n=5, cutoff=0.6)

    return {
        'exists': exists_on_disk,
        'path': file_path,
        'similar_files': similar,
        'state_in_manifest': state_in_manifest,
        'phase': phase,
        'deprecated': deprecated
    }


def format_output(result: Dict) -> str:
    """Format check result for terminal output"""
    output = []

    if result['exists']:
        output.append(f"❌ File EXISTS: {result['path']}")
        output.append(f"   Status: File already exists on disk")

        if result['state_in_manifest']:
            output.append(f"   Manifest State: {result['state_in_manifest']}")
            output.append(f"   Phase: {result['phase']}")

            if result['deprecated']:
                output.append(f"   ⚠️  WARNING: File is marked as DEPRECATED in manifest")
                output.append(f"   → Consider archiving before creating new version")
        else:
            output.append(f"   ⚠️  WARNING: File exists but NOT tracked in FILE_MANIFEST.yaml")
            output.append(f"   → Consider adding to manifest or removing duplicate")
    else:
        output.append(f"✅ File does NOT exist: {result['path']}")

        if result['state_in_manifest']:
            output.append(f"   Manifest State: {result['state_in_manifest']}")
            output.append(f"   Phase: {result['phase']}")
            output.append(f"   ✓ Safe to create (tracked in manifest)")
        else:
            output.append(f"   ⚠️  WARNING: File NOT in FILE_MANIFEST.yaml")
            output.append(f"   → Consider adding to manifest before creating")

        if result['similar_files']:
            output.append(f"\n   📋 Similar files found:")
            for similar in result['similar_files']:
                output.append(f"      - {similar}")
            output.append(f"\n   💡 TIP: Check if one of these is what you need before creating new file")

    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_file_exists.py <file_path>")
        print("\nExample:")
        print("  python scripts/phase5/check_file_exists.py app/services/new_service.py")
        sys.exit(1)

    file_path = sys.argv[1]
    result = check_file_exists(file_path)

    print(format_output(result))

    # Exit code
    if result['exists']:
        sys.exit(1)  # File exists - do NOT create
    else:
        sys.exit(0)  # File doesn't exist - safe to create


if __name__ == '__main__':
    main()
