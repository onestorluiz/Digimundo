#!/usr/bin/env python3
"""Test MemoryLocator with harmony integration"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from apps.scripturemon.canonical.memory_manager import MemoryLocator

print("🎭 Testing MemoryLocator with Harmony...")
print("-" * 60)

# Clear cache
locator = MemoryLocator()
if locator.runtime_path.exists():
    locator.runtime_path.unlink()

# Test location
instance, report = locator.locate()

print("\nReport:")
print(json.dumps(report, indent=2))

print("\n" + "-" * 60)

if report.get("selected"):
    print(f"✅ Selected: {report['selected']}")
    
    # Test the instance
    if instance:
        # Test save
        try:
            result = instance.save("Harmony test memory", memory_type="harmony_test")
            print(f"Save test: {'✅ PASS' if result else '❌ FAIL'}")
        except Exception as e:
            print(f"Save test: ❌ ERROR - {e}")
        
        # Test get_context
        try:
            results = instance.get_context("harmony")
            print(f"Get test: ✅ PASS - {len(results) if results else 0} results")
        except Exception as e:
            print(f"Get test: ❌ ERROR - {e}")
        
        # Test stats
        try:
            stats = instance.get_stats()
            if 'active_systems' in stats:
                print(f"Stats: ✅ Harmony with {stats['active_systems']} systems")
            else:
                print(f"Stats: ✅ {stats.get('type', 'Unknown')}")
        except Exception as e:
            print(f"Stats test: ❌ ERROR - {e}")
else:
    print("❌ No memory manager found")