#!/usr/bin/env python3
"""
Show implementation progress from FILE_MANIFEST.yaml

Usage:
    python scripts/phase5/show_progress.py
    python scripts/phase5/show_progress.py --phase 5.1
    python scripts/phase5/show_progress.py --state planned
    python scripts/phase5/show_progress.py --detailed
"""

import sys
import os
from pathlib import Path
import yaml
from typing import Dict, List
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

    # If not found, raise error
    raise FileNotFoundError(
        f"FILE_MANIFEST.yaml not found in any of these locations:\n" +
        "\n".join(f"  - {p}" for p in possible_paths)
    )


def extract_all_files(manifest: dict) -> List[Dict]:
    """Extract all file specs from manifest"""
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


def calculate_progress_bar(current: int, total: int, width: int = 40) -> str:
    """Generate progress bar string"""
    if total == 0:
        return "░" * width

    filled = int((current / total) * width)
    empty = width - filled

    return "▓" * filled + "░" * empty


def show_overall_progress(manifest: dict):
    """Show overall Fase 5 progress"""
    all_files = extract_all_files(manifest)

    # Count by state
    by_state = {'planned': 0, 'staged': 0, 'implemented': 0, 'validated': 0, 'finalized': 0, 'deprecated': 0}

    for file_spec in all_files:
        state = file_spec.get('state', 'planned')
        if state in by_state:
            by_state[state] += 1

    total = len(all_files)
    completed = by_state['finalized']
    in_progress = by_state['staged'] + by_state['implemented'] + by_state['validated']

    print("┌" + "─" * 68 + "┐")
    print("│ FASE 5 - PLATFORM EVOLUTION" + " " * 40 + "│")
    print("│ Overall Implementation Progress" + " " * 36 + "│")
    print("├" + "─" * 68 + "┤")

    progress_pct = int((completed / total) * 100) if total > 0 else 0
    bar = calculate_progress_bar(completed, total, width=50)

    print(f"│ Progress: {bar} {progress_pct}%  │")
    print("│" + " " * 68 + "│")
    print(f"│ ✅ Finalized:    {completed:3d} files{' ' * 48}│")
    print(f"│ 🟡 In Progress:  {in_progress:3d} files{' ' * 48}│")
    print(f"│ ⏳ Planned:      {by_state['planned']:3d} files{' ' * 48}│")
    print(f"│ ❌ Deprecated:   {by_state['deprecated']:3d} files{' ' * 48}│")
    print("│" + " " * 68 + "│")
    print(f"│ Total Files:     {total:3d}{' ' * 51}│")
    print("└" + "─" * 68 + "┘")


def show_phase_progress(manifest: dict, phase: str = None):
    """Show progress for specific phase or all phases"""
    all_files = extract_all_files(manifest)

    # Group by phase
    by_phase = {}
    for file_spec in all_files:
        file_phase = str(file_spec.get('phase', ''))

        if file_phase not in by_phase:
            by_phase[file_phase] = {
                'planned': 0,
                'staged': 0,
                'implemented': 0,
                'validated': 0,
                'finalized': 0,
                'total': 0
            }

        state = file_spec.get('state', 'planned')
        if state in by_phase[file_phase]:
            by_phase[file_phase][state] += 1
        by_phase[file_phase]['total'] += 1

    # Filter by phase if specified
    if phase:
        phases_to_show = {phase: by_phase.get(phase, {})}
    else:
        phases_to_show = by_phase

    # Display
    print("\n┌" + "─" * 68 + "┐")
    print("│ PROGRESS BY PHASE" + " " * 50 + "│")
    print("└" + "─" * 68 + "┘\n")

    for phase_num in sorted(phases_to_show.keys()):
        stats = phases_to_show[phase_num]

        if not stats or stats['total'] == 0:
            continue

        completed = stats['finalized']
        total = stats['total']
        pct = int((completed / total) * 100) if total > 0 else 0

        bar = calculate_progress_bar(completed, total, width=30)

        phase_name = {
            '5.1': 'Foundation',
            '5.2': 'Conflict Detection',
            '5.3': 'Schedule Optimizer',
            '5.4': 'Predictive Analytics'
        }.get(phase_num, f'Phase {phase_num}')

        print(f"Phase {phase_num}: {phase_name}")
        print(f"  Progress: {bar} {pct}%")
        print(f"  Files: {completed}/{total} finalized")
        print(f"  Status: ✅{stats['finalized']} 🟡{stats['implemented'] + stats['validated']} ⏳{stats['planned']}")
        print()


def show_detailed_progress(manifest: dict, phase: str = None, state: str = None):
    """Show detailed file-by-file progress"""
    all_files = extract_all_files(manifest)

    # Filter
    filtered_files = all_files

    if phase:
        filtered_files = [f for f in filtered_files if str(f.get('phase')) == phase]

    if state:
        filtered_files = [f for f in filtered_files if f.get('state') == state]

    # Group by phase
    by_phase = {}
    for file_spec in filtered_files:
        file_phase = str(file_spec.get('phase', 'unknown'))

        if file_phase not in by_phase:
            by_phase[file_phase] = []

        by_phase[file_phase].append(file_spec)

    # Display
    print("\n┌" + "─" * 78 + "┐")
    print("│ DETAILED FILE STATUS" + " " * 57 + "│")
    print("└" + "─" * 78 + "┘\n")

    for phase_num in sorted(by_phase.keys()):
        files = by_phase[phase_num]

        print(f"\n{'='*78}")
        print(f"Phase {phase_num}")
        print(f"{'='*78}\n")

        for file_spec in files:
            state = file_spec.get('state', 'planned')
            priority = file_spec.get('priority', 'medium')
            path = file_spec['path']
            desc = file_spec.get('description', 'No description')

            # State emoji
            state_emoji = {
                'planned': '⏳',
                'staged': '🟡',
                'implemented': '🟢',
                'validated': '✅',
                'finalized': '✅',
                'deprecated': '❌'
            }.get(state, '❓')

            # Priority emoji
            priority_emoji = {
                'critical': '🔴',
                'high': '🟡',
                'medium': '🟢',
                'low': '⚪'
            }.get(priority, '⚪')

            print(f"{state_emoji} {priority_emoji} {path}")
            print(f"   State: {state} | Priority: {priority}")
            if desc and len(desc) < 100:
                print(f"   {desc}")
            print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Show Fase 5 implementation progress')
    parser.add_argument('--phase', type=str, help='Filter by phase (e.g., 5.1)')
    parser.add_argument('--state', type=str, help='Filter by state (planned, implemented, etc)')
    parser.add_argument('--detailed', action='store_true', help='Show detailed file-by-file progress')
    args = parser.parse_args()

    # Load manifest
    manifest = load_manifest()

    # Show progress
    if args.detailed:
        show_detailed_progress(manifest, phase=args.phase, state=args.state)
    elif args.phase or args.state:
        if args.phase:
            show_phase_progress(manifest, phase=args.phase)

        if args.state:
            all_files = extract_all_files(manifest)
            filtered = [f for f in all_files if f.get('state') == args.state]
            print(f"\n{len(filtered)} files with state '{args.state}':")
            for f in filtered[:20]:  # Show first 20
                print(f"  - {f['path']}")
    else:
        # Default: overall progress + phase breakdown
        show_overall_progress(manifest)
        show_phase_progress(manifest)


if __name__ == '__main__':
    main()
