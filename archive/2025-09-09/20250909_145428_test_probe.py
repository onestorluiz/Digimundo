#!/usr/bin/env python3
"""Test memory probe status"""

from apps.scripturemon.canonical.memory_manager import get_memory_manager

mm = get_memory_manager()

print(f"Manager type: {type(mm).__name__}")
print(f"Has functional: {hasattr(mm, 'functional')}")
if hasattr(mm, 'functional'):
    print(f"Functional value: {mm.functional}")

# Test save
save_result = False
if hasattr(mm, 'save'):
    save_result = bool(mm.save("Bootstrap probe test", memory_type="probe"))
    print(f"Save result: {save_result}")

# Test get
get_result = False
if hasattr(mm, 'get_context'):
    results = mm.get_context("probe")
    get_result = results is not None
    print(f"Get result: {get_result}")
    print(f"Results: {results[:1] if results else []}")  # Show first result

probe_status = "pass" if (save_result and get_result) else "fail"
print(f"\nProbe status: {probe_status}")
