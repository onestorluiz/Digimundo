#!/usr/bin/env python3
"""Test memory locator probe functionality"""

import sys
import os
import json
from pathlib import Path

# Disable heavy systems for testing
os.environ['DISABLE_OLLAMA'] = '1'
os.environ['DISABLE_BACKUP'] = '1'
os.environ['DISABLE_TELEPATHY'] = '1'

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from apps.scripturemon.canonical.memory_manager import MemoryLocator

print("Testing MemoryLocator probe...")
print("-" * 60)

locator = MemoryLocator()

# Clear cache
if locator.runtime_path.exists():
    locator.runtime_path.unlink()
    print("✓ Cache cleared")

# Test each candidate manually
for module_path, class_name, init_args in locator.CANDIDATES:
    canonical_name = f"{module_path}.{class_name}"
    print(f"\nTesting: {canonical_name}")
    
    success, instance, error = locator.probe_candidate(module_path, class_name, init_args)
    
    if success:
        print(f"  ✅ SUCCESS - {canonical_name}")
        print(f"     Instance: {instance.__class__.__name__}")
        if hasattr(instance, 'functional'):
            print(f"     Functional: {instance.functional}")
        break
    else:
        print(f"  ❌ FAILED - {error}")

print("\n" + "-" * 60)
print("Running full locate...")

# Now run full locate
instance, report = locator.locate()

print("\nReport:")
print(json.dumps(report, indent=2))

if report.get("selected") and report["selected"] != "NoOpMemoryManager":
    print(f"\n✅ SUCCESS: Found working memory manager: {report['selected']}")
else:
    print(f"\n❌ FAILED: No working memory manager found")

# Test the instance
if instance and hasattr(instance, 'save'):
    try:
        result = instance.save("Final test", memory_type="test")
        print(f"Save test: {'✅ PASS' if result else '❌ FAIL'}")
    except Exception as e:
        print(f"Save test: ❌ ERROR - {e}")