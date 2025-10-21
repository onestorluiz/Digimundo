#!/usr/bin/env python3
import os
from pathlib import Path

required_modules = [
    "apps/scripturemon/bootstrap.py",
    "apps/scripturemon/cli.py",
    "apps/scripturemon/chat.py",
    "apps/scripturemon/canonical/memory_manager.py",
    "apps/scripturemon/compat/aliases.py",
    "apps/scripturemon/monitoring_system.py",
    "bin/scripturemon"
]

results = []
for module in required_modules:
    path = Path(module)
    exists = path.exists()
    results.append(f"{'✅' if exists else '❌'} {module}")
    
scan_content = f"""# Phase 0 - Module Validation Scan

## Required Modules Check
{chr(10).join(results)}

## Extra Files Found
"""

# Check for extra files in bin/
bin_dir = Path("bin")
if bin_dir.exists():
    extras = []
    for f in bin_dir.iterdir():
        if f.name != "scripturemon" and not f.name.startswith("."):
            extras.append(f"- {f.name} ({'executable' if os.access(f, os.X_OK) else 'non-executable'})")
    
    if extras:
        scan_content += chr(10).join(extras)
    else:
        scan_content += "No extra files in bin/"
else:
    scan_content += "bin/ directory not found"

scan_content += f"""

## Summary
All required modules: {'✅ PRESENT' if all('✅' in r for r in results) else '❌ MISSING SOME'}
System ready for audit: {'YES' if all('✅' in r for r in results) else 'PARTIAL'}
"""

with open("reports/harmony_vFinal/system_audit/phase0_scan.md", "w") as f:
    f.write(scan_content)

print("✅ Module validation complete")
for r in results[:3]:
    print(f"  {r}")
