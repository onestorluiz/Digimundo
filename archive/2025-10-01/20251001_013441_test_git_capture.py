#!/usr/bin/env python3
"""
Teste de captura de commit com GitMemoryBridge

Testa se o sistema consegue capturar commits existentes.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.git_memory_bridge import GitMemoryBridge

def test_capture():
    """Testa captura de commits existentes"""
    print("🔥 Testing GitMemoryBridge...")
    print()

    # Initialize bridge
    repo_path = Path(__file__).parent.parent
    memory_dir = repo_path / "memory"

    bridge = GitMemoryBridge(
        repo_path=str(repo_path),
        memory_dir=str(memory_dir)
    )

    print(f"✅ Bridge initialized")
    print(f"   Repo: {repo_path}")
    print(f"   Memory: {memory_dir}")
    print()

    # Test 1: Capture latest commit (HEAD)
    print("📸 Test 1: Capturing HEAD...")
    try:
        snapshot = bridge.capture_commit("HEAD")
        print(f"✅ HEAD captured successfully")
        print(f"   Commit: {snapshot['commit_hash_short']}")
        print(f"   Phase: {snapshot['phase']}")
        print(f"   Files: {snapshot['files_changed']}")
        print(f"   TODOs: {len(snapshot['todos_extracted'])}")
        print()
    except Exception as e:
        print(f"❌ Failed to capture HEAD: {e}")
        return False

    # Test 2: Capture specific commit (FASE 1 complete)
    print("📸 Test 2: Capturing a9febcf (FASE 1 complete)...")
    try:
        snapshot = bridge.capture_commit("a9febcf")
        print(f"✅ a9febcf captured successfully")
        print(f"   Message: {snapshot['message'].split(chr(10))[0]}")
        print(f"   Phase: {snapshot['phase']}")
        print(f"   Files: {snapshot['files_changed']}")
        print(f"   Specialists: {snapshot['specialists_modified']}")
        print(f"   Tests: {snapshot['tests_added']}")
        print(f"   TODOs: {len(snapshot['todos_extracted'])}")
        print()
    except Exception as e:
        print(f"❌ Failed to capture a9febcf: {e}")
        return False

    # Test 3: Generate session summary
    print("📊 Test 3: Generating session summary (last 3 commits)...")
    try:
        summary = bridge.generate_session_summary(last_n=3)
        print(f"✅ Session summary generated")
        print(f"   Commits: {summary['commits_count']}")
        print(f"   Files changed: {summary['total_files_changed']}")
        print(f"   Lines added: {summary['total_lines_added']}")
        print(f"   TODOs found: {len(summary['todos_accumulated'])}")
        print(f"   Specialists: {summary['specialists_modified']}")
        print(f"   Patterns: {summary['patterns']}")
        print()
    except Exception as e:
        print(f"❌ Failed to generate summary: {e}")
        return False

    # Test 4: Verify files created
    print("📁 Test 4: Verifying memory files...")
    commits_dir = memory_dir / "commits"
    files_created = list(commits_dir.glob("*.json"))
    print(f"✅ Files created: {len(files_created)}")
    for file in sorted(files_created)[-3:]:  # Show last 3
        print(f"   - {file.name}")
    print()

    print("=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_capture()
    sys.exit(0 if success else 1)
