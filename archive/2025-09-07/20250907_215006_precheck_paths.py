#!/usr/bin/env python3
"""
Detect real paths for critical files in scripturemon-validation
"""
import json
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")

def find_file(patterns, description):
    """Find file matching patterns"""
    for pattern in patterns:
        matches = list(PROJECT_ROOT.rglob(pattern))
        # Filter out backup directories
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
    
    # Chat
    chat_patterns = [
        "apps/scripturemon/chat.py",
        "src/apps/scripturemon/chat.py",
        "**/chat.py"
    ]
    paths["files"]["chat"] = find_file(chat_patterns, "Chat module")
    
    # Memory Manager
    memory_patterns = [
        "apps/scripturemon/memory_manager.py",
        "src/memory/unified_manager.py",
        "src/memory/memory_manager.py",
        "**/memory_manager.py"
    ]
    paths["files"]["memory_manager"] = find_file(memory_patterns, "Memory Manager")
    
    # RAG Adapter
    rag_patterns = [
        "src/rag/adapter.py",
        "apps/scripturemon/rag_advanced.py",
        "**/rag_adapter.py",
        "**/rag_advanced.py"
    ]
    paths["files"]["rag_adapter"] = find_file(rag_patterns, "RAG Adapter")
    
    # SoulOS Wrapper
    soulos_patterns = [
        "src/utils/soulos_wrapper.py",
        "apps/scripturemon/soulos_wrapper.py",
        "**/soulos_wrapper.py"
    ]
    paths["files"]["soulos_wrapper"] = find_file(soulos_patterns, "SoulOS Wrapper")
    
    # Settings
    settings_patterns = [
        "config/settings.yaml",
        "src/config/settings.yaml",
        "**/settings.yaml"
    ]
    paths["files"]["settings"] = find_file(settings_patterns, "Settings YAML")
    
    # Runtime settings (if exists)
    runtime_patterns = [
        "src/config/runtime_settings.py",
        "**/runtime_settings.py"
    ]
    paths["files"]["runtime_settings"] = find_file(runtime_patterns, "Runtime Settings")
    
    # Check what actually exists
    paths["files_found"] = {k: v for k, v in paths["files"].items() if v}
    paths["files_missing"] = {k: v for k, v in paths["files"].items() if not v}
    
    # Save report
    output_dir = PROJECT_ROOT / "reports" / "fix_current"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "precheck.json"
    with open(output_file, 'w') as f:
        json.dump(paths, f, indent=2)
    
    print(f"✅ Precheck saved to: {output_file}")
    print(f"\n📁 Files found:")
    for key, path in paths["files_found"].items():
        print(f"  {key}: {path}")
    
    if paths["files_missing"]:
        print(f"\n⚠️ Files not found:")
        for key in paths["files_missing"]:
            print(f"  {key}: Not found")
    
    return paths

if __name__ == "__main__":
    main()