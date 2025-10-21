#!/usr/bin/env python3
"""Test MemoryLocator with exact candidate list"""

import sys
import os
import json
from pathlib import Path

# Disable heavy systems for quick testing
os.environ['DISABLE_OLLAMA'] = '1'
os.environ['DISABLE_SOUL'] = '1'
os.environ['DISABLE_TELEPATHY'] = '1'

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from apps.scripturemon.canonical.memory_manager import MemoryLocator

print("Testing MemoryLocator with EXACT candidate list...")
print("-" * 60)

locator = MemoryLocator()

# Clear cache
if locator.runtime_path.exists():
    locator.runtime_path.unlink()
    print("✓ Cache cleared")

print("\nExpected candidates (in order):")
print("1. apps.scripturemon.memory_manager:UnifiedMemoryManager")
print("2. apps.scripturemon.memory_unification_restored:UnifiedMemory")
print("3. apps.scripturemon.crystal_memory_restored:CrystalMemory")
print("4. apps.scripturemon.membridge_restored:MemoryBridge")

print("\n" + "-" * 60)
print("Testing each candidate individually...")

for i, (module_path, class_name, init_args) in enumerate(locator.CANDIDATES, 1):
    canonical_name = f"{module_path}:{class_name}"
    print(f"\n{i}. Testing: {canonical_name}")
    
    success, instance, error = locator.probe_candidate(module_path, class_name, init_args)
    
    if success:
        print(f"   ✅ SUCCESS")
        if hasattr(instance, 'functional'):
            print(f"   Functional: {instance.functional}")
        print(f"   Instance type: {instance.__class__.__name__}")
        break
    else:
        print(f"   ❌ FAILED: {error}")

print("\n" + "-" * 60)
print("Running full locate...")

# Now run full locate
instance, report = locator.locate()

print("\nReport:")
print(json.dumps(report, indent=2))

# Validate results
if report.get("selected"):
    if report["selected"] != "NoOpMemoryManager":
        print(f"\n✅ SUCCESS: Found working memory manager")
        print(f"   Selected: {report['selected']}")
        canonical_not_noop = True
    else:
        print(f"\n❌ FAILED: Only NoOp available")
        canonical_not_noop = False
else:
    print(f"\n❌ FAILED: No memory manager found")
    canonical_not_noop = False

# Test probe functionality
memory_probe_pass = False
if instance:
    try:
        # Test save
        save_result = instance.save("MemoryLocator probe test", memory_type="probe")
        # Test get
        get_result = instance.get_context("probe")
        
        if save_result and get_result is not None:
            memory_probe_pass = True
            print(f"Probe test: ✅ PASS")
        else:
            print(f"Probe test: ❌ FAIL (save={save_result}, get={get_result is not None})")
    except Exception as e:
        print(f"Probe test: ❌ ERROR - {e}")

# Generate acceptance
acceptance = {
    "memory_probe_pass": memory_probe_pass,
    "canonical_not_noop": canonical_not_noop,
    "status": "PASS" if (memory_probe_pass and canonical_not_noop) else "FAIL",
    "notes": f"Selected: {report.get('selected', 'None')}"
}

print("\n" + "-" * 60)
print("Acceptance:")
print(json.dumps(acceptance, indent=2))