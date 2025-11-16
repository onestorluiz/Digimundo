#!/usr/bin/env python3
"""
Sync FILE_MANIFEST.yaml with actual filesystem state

This script:
1. Checks all planned files - updates state if they exist
2. Checks all implemented files - marks as missing if they don't exist
3. Finds untracked files on disk
4. Updates FILE_MANIFEST.yaml automatically

Usage:
    python scripts/phase5/sync_manifest.py
    python scripts/phase5/sync_manifest.py --dry-run  # Preview changes only
"""

import sys
import os
from pathlib import Path
import yaml
from typing import Dict, List, Tuple
from datetime import datetime


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


def load_manifest() -> Tuple[dict, Path]:
    """Load FILE_MANIFEST.yaml and return content + path"""
    # Try multiple locations for FILE_MANIFEST.yaml
    possible_paths = [
        project_root / "docs/fase_5/FILE_MANIFEST.yaml",           # If in cineprod-flask/
        project_root.parent / "docs/fase_5/FILE_MANIFEST.yaml",    # If parent is Projeto_Digimundo/
        Path(__file__).parent.parent.parent / "docs/fase_5/FILE_MANIFEST.yaml"  # From script location
    ]

    for manifest_path in possible_paths:
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = yaml.safe_load(f)
            return manifest, manifest_path

    # If not found, raise error
    raise FileNotFoundError(
        f"FILE_MANIFEST.yaml not found in any of these locations:\n" +
        "\n".join(f"  - {p}" for p in possible_paths)
    )


def save_manifest(manifest: dict, path: Path):
    """Save updated manifest with proper formatting"""
    with open(path, 'w') as f:
        yaml.dump(manifest, f, sort_keys=False, default_flow_style=False, allow_unicode=True)


def sync_file_states(manifest: dict, dry_run: bool = False) -> List[str]:
    """
    Sync file states in manifest with filesystem reality

    Returns:
        List of change descriptions
    """
    changes = []

    for section_key, section_data in manifest.items():
        if section_key in ['metadata', 'totals', 'dependency_graph']:
            continue

        if not isinstance(section_data, dict):
            continue

        for category_key, items in section_data.items():
            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict) or 'path' not in item:
                    continue

                file_path = project_root / item['path']
                current_state = item.get('state')
                file_type = item.get('type', 'new_file')

                # Skip migrations and configs
                if file_type in ['migration', 'config']:
                    continue

                # Check if file exists
                exists = file_path.exists()

                # State transitions
                if exists and current_state == 'planned':
                    # File was planned but now exists → staged
                    if not dry_run:
                        item['state'] = 'staged'
                    changes.append(f"✓ {item['path']}: planned → staged")

                elif not exists and current_state in ['staged', 'implemented', 'validated']:
                    # File was implemented but now missing
                    if not dry_run:
                        item['state'] = 'missing'
                    changes.append(f"⚠  {item['path']}: {current_state} → missing")

                elif exists and current_state == 'deprecated':
                    # Deprecated file still exists (should be archived)
                    changes.append(f"⚠  {item['path']}: deprecated but still exists (archive needed)")

    return changes


def find_untracked_files(manifest: dict) -> List[str]:
    """
    Find files on disk that are not tracked in manifest

    Returns:
        List of untracked file paths
    """
    # Extract all tracked paths
    tracked_paths = set()

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
                    tracked_paths.add(item['path'])

    # Scan filesystem for .py files in key directories
    untracked = []
    search_dirs = [
        'app/services',
        'app/routes',
        'app/models',
        'app/ml',
        'tests/unit',
        'tests/integration',
        'celery_tasks'
    ]

    for search_dir in search_dirs:
        search_path = project_root / search_dir

        if not search_path.exists():
            continue

        for py_file in search_path.rglob('*.py'):
            # Get relative path from project root
            rel_path = py_file.relative_to(project_root)
            rel_path_str = str(rel_path)

            # Skip __pycache__, __init__.py, _archived
            if '__pycache__' in rel_path_str or '__init__.py' in rel_path_str:
                continue
            if '_archived' in rel_path_str or '_backup' in rel_path_str:
                continue

            # Check if tracked
            if rel_path_str not in tracked_paths:
                untracked.append(rel_path_str)

    return sorted(untracked)


def update_totals(manifest: dict) -> Dict:
    """Recalculate totals section based on actual file counts"""
    totals = {
        'fase_5_1': {'new_files': 0, 'modified_files': 0, 'deprecated_files': 0},
        'fase_5_2': {'new_files': 0, 'modified_files': 0, 'deprecated_files': 0},
        'fase_5_3': {'new_files': 0, 'modified_files': 0, 'deprecated_files': 0},
        'fase_5_4': {'new_files': 0, 'modified_files': 0, 'deprecated_files': 0},
    }

    for section_key, section_data in manifest.items():
        if not isinstance(section_data, dict):
            continue

        for category_key, items in section_data.items():
            if not isinstance(items, list):
                continue

            for item in items:
                if not isinstance(item, dict):
                    continue

                phase = item.get('phase')
                file_type = item.get('type')

                if not phase or not file_type:
                    continue

                phase_key = f'fase_{phase}'.replace('.', '_')

                if phase_key not in totals:
                    continue

                if file_type == 'new_file':
                    totals[phase_key]['new_files'] += 1
                elif file_type == 'modification':
                    totals[phase_key]['modified_files'] += 1
                elif file_type == 'deprecated':
                    totals[phase_key]['deprecated_files'] += 1

    return totals


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sync FILE_MANIFEST.yaml with filesystem')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
    args = parser.parse_args()

    print("🔄 Syncing FILE_MANIFEST.yaml with filesystem...")
    print()

    # Load manifest
    manifest, manifest_path = load_manifest()

    # Sync file states
    print("📊 Checking file states...")
    changes = sync_file_states(manifest, dry_run=args.dry_run)

    if changes:
        print(f"\n✓ Found {len(changes)} state changes:")
        for change in changes:
            print(f"  {change}")
    else:
        print("  ✓ All file states up to date")

    # Find untracked files
    print("\n📂 Scanning for untracked files...")
    untracked = find_untracked_files(manifest)

    if untracked:
        print(f"\n⚠️  Found {len(untracked)} untracked files:")
        for file_path in untracked[:10]:  # Show first 10
            print(f"  - {file_path}")

        if len(untracked) > 10:
            print(f"  ... and {len(untracked) - 10} more")

        print("\n💡 TIP: Add these files to FILE_MANIFEST.yaml or move to _archived/")
    else:
        print("  ✓ No untracked files found")

    # Update totals
    if not args.dry_run and changes:
        print("\n📊 Updating totals...")
        new_totals = update_totals(manifest)
        manifest['totals'] = new_totals

    # Save manifest
    if not args.dry_run:
        if changes:
            save_manifest(manifest, manifest_path)
            print(f"\n✅ Manifest synced: {len(changes)} changes saved")
        else:
            print("\n✅ Manifest already up to date")
    else:
        print("\n🔍 DRY RUN: No changes saved")

    # Summary
    print("\n" + "="*60)
    print(f"Summary:")
    print(f"  State changes: {len(changes)}")
    print(f"  Untracked files: {len(untracked)}")
    print(f"  Manifest path: {manifest_path}")
    print("="*60)


if __name__ == '__main__':
    main()
