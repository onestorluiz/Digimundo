#!/usr/bin/env python3
"""
V32 Precheck - Detect real paths for integration
"""
import json
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")

def find_file(patterns, description):
    """Find file matching patterns, ignoring backup dirs"""
    for pattern in patterns:
        matches = list(PROJECT_ROOT.rglob(pattern))
        matches = [m for m in matches if 'backup' not in str(m).lower()]
        if matches:
            return str(matches[0].relative_to(PROJECT_ROOT))
    return None

def main():
    paths = {
        "project_root": str(PROJECT_ROOT),
        "timestamp": datetime.now().isoformat(),
        "files": {}
    }
    
    # Core components
    paths["files"]["chat"] = find_file(
        ["apps/scripturemon/chat.py", "src/apps/scripturemon/chat.py"],
        "Chat module"
    )
    
    paths["files"]["memory_manager"] = find_file(
        ["apps/scripturemon/memory_manager.py", "src/memory/unified_manager.py"],
        "Memory Manager"
    )
    
    paths["files"]["rag_adapter"] = find_file(
        ["src/rag/adapter.py", "apps/scripturemon/rag_adapter.py"],
        "RAG Adapter"
    )
    
    paths["files"]["soulos_wrapper"] = find_file(
        ["src/utils/soulos_wrapper.py", "apps/scripturemon/soulos_wrapper.py"],
        "SoulOS Wrapper"
    )
    
    paths["files"]["sqlite_dao"] = find_file(
        ["src/memory/sqlite_dao.py", "apps/scripturemon/sqlite_dao.py"],
        "SQLite DAO"
    )
    
    paths["files"]["settings"] = find_file(
        ["config/settings.yaml", "src/config/settings.yaml"],
        "Settings YAML"
    )
    
    paths["files"]["runtime_settings"] = find_file(
        ["src/config/runtime_settings.py"],
        "Runtime Settings"
    )
    
    # Additional components for integration
    paths["files"]["memory_unification"] = find_file(
        ["apps/scripturemon/memory_unification.py"],
        "Memory Unification"
    )
    
    paths["files"]["rag_advanced"] = find_file(
        ["apps/scripturemon/rag_advanced.py"],
        "RAG Advanced"
    )
    
    # Summary
    paths["files_found"] = {k: v for k, v in paths["files"].items() if v}
    paths["files_missing"] = [k for k, v in paths["files"].items() if not v]
    
    # Save report
    output_dir = PROJECT_ROOT / "reports" / "integrate_align_v32"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "precheck.json", 'w') as f:
        json.dump(paths, f, indent=2)
    
    print(f"✅ Precheck complete: {len(paths['files_found'])} files found")
    return paths

if __name__ == "__main__":
    main()