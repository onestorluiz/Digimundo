#!/usr/bin/env python3
import json
import os
from datetime import datetime

# Check results
inventory_exists = os.path.exists("reports/harmony_vFinal/phase0_inventory.json") and \
                  os.path.exists("reports/harmony_vFinal/phase0_inventory.md")

backup_exists = os.path.exists("reports/harmony_vFinal/phase0_backup.json")

help_exists = os.path.exists("reports/harmony_vFinal/phase0/help.txt")
if help_exists:
    with open("reports/harmony_vFinal/phase0/help.txt") as f:
        help_content = f.read()
        help_valid = len(help_content) > 50 and ("usage" in help_content.lower() or "help" in help_content.lower())
else:
    help_valid = False

status_exists = os.path.exists("reports/harmony_vFinal/phase0/status.txt")  
if status_exists:
    with open("reports/harmony_vFinal/phase0/status.txt") as f:
        status_content = f.read()
        status_valid = len(status_content) > 50 and ("status" in status_content.lower() or "persona" in status_content.lower())
else:
    status_valid = False

# Determine overall status
all_pass = inventory_exists and backup_exists and help_valid and status_valid
overall_status = "PASS" if all_pass else "FAIL"

# Notes
notes = []
if not inventory_exists:
    notes.append("Inventory files missing")
if not backup_exists:
    notes.append("Backup metadata missing")
if not help_valid:
    notes.append("Help command invalid or missing")
if not status_valid:
    notes.append("Status command invalid or missing")

if not notes:
    notes.append("All phase 0 tasks completed successfully")

acceptance = {
    "timestamp": datetime.now().isoformat(),
    "inventory": inventory_exists,
    "backup": backup_exists,
    "help": help_valid,
    "status": status_valid,
    "overall_status": overall_status,
    "notes": "; ".join(notes)
}

with open("reports/harmony_vFinal/phase0/acceptance.json", "w") as f:
    json.dump(acceptance, f, indent=2)

print(f"Acceptance report generated: {overall_status}")
print(f"Inventory: {inventory_exists}, Backup: {backup_exists}, Help: {help_valid}, Status: {status_valid}")
