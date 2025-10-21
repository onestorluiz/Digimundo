#!/usr/bin/env python3
"""
Git Session Summary - Reconecta contexto após sessão

Usage:
    python scripts/git_session_summary.py --last 5
    python scripts/git_session_summary.py --since FASE1_COMPLETE
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.git_memory_bridge import GitMemoryBridge

def main():
    parser = argparse.ArgumentParser(description="Generate session summary from Git history")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--last", type=int, help="Last N commits")
    group.add_argument("--since", type=str, help="Since commit/tag")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    # Initialize bridge
    repo_path = Path(__file__).parent.parent
    memory_dir = repo_path / "memory"

    bridge = GitMemoryBridge(
        repo_path=str(repo_path),
        memory_dir=str(memory_dir)
    )

    # Generate summary
    if args.last:
        summary = bridge.generate_session_summary(last_n=args.last)
    elif args.since:
        summary = bridge.generate_session_summary(since_commit=args.since)
    else:
        # Default: últimos 5 commits
        summary = bridge.generate_session_summary(last_n=5)

    # Output
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        _print_summary(summary)

def _print_summary(summary: dict):
    """Formata summary para output humano"""
    print("=" * 70)
    print("📊 GIT SESSION SUMMARY")
    print("=" * 70)
    print()

    print(f"📍 Session Range: {summary['session_start']} → {summary['session_end']}")
    print(f"📝 Commits: {summary['commits_count']}")
    print()

    if summary['commits']:
        print("Commits:")
        for commit in summary['commits'][:10]:  # Max 10
            print(f"  - {commit}")
        if len(summary['commits']) > 10:
            print(f"  ... and {len(summary['commits']) - 10} more")
        print()

    print(f"📊 Changes:")
    print(f"  Files changed: {summary['total_files_changed']}")
    print(f"  Lines added: {summary['total_lines_added']}")
    print(f"  Lines removed: {summary['total_lines_removed']}")
    print()

    if summary['specialists_modified']:
        print(f"🔬 Specialists Modified ({len(summary['specialists_modified'])}):")
        for spec in summary['specialists_modified'][:5]:
            print(f"  - {spec}")
        if len(summary['specialists_modified']) > 5:
            print(f"  ... and {len(summary['specialists_modified']) - 5} more")
        print()

    if summary['tests_added']:
        print(f"🧪 Tests Added ({len(summary['tests_added'])}):")
        for test in summary['tests_added'][:5]:
            print(f"  - {test}")
        if len(summary['tests_added']) > 5:
            print(f"  ... and {len(summary['tests_added']) - 5} more")
        print()

    if summary['todos_accumulated']:
        print(f"📝 TODOs Extracted ({len(summary['todos_accumulated'])}):")
        for todo in summary['todos_accumulated'][:5]:
            print(f"  - [{todo['type']}] {todo['text'][:60]}...")
        if len(summary['todos_accumulated']) > 5:
            print(f"  ... and {len(summary['todos_accumulated']) - 5} more")
        print()

    if summary['patterns']:
        print(f"🔍 Patterns Detected:")
        for pattern in summary['patterns']:
            print(f"  - {pattern}")
        print()

    if summary['phases']:
        print(f"🎯 Phases:")
        for phase, count in summary['phases'].items():
            print(f"  - {phase}: {count} commits")
        print()

    print("=" * 70)
    print("✅ Context recovered - Ready to continue")
    print("=" * 70)

if __name__ == "__main__":
    main()
