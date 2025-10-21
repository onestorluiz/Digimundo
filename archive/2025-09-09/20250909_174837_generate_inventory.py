#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime

root = Path(".")
py_files = []
db_files = []

for path in root.rglob("*"):
    if path.is_file():
        path_str = str(path)
        if "backup" in path_str or ".git" in path_str or "__pycache__" in path_str or ".venv" in path_str:
            continue
        if path.suffix == ".py":
            py_files.append(str(path.relative_to(root)))
        elif path.suffix == ".db":
            db_files.append(str(path.relative_to(root)))

py_files.sort()
db_files.sort()

inventory = {
    "timestamp": datetime.now().isoformat(),
    "root": str(root.absolute()),
    "statistics": {
        "python_files": len(py_files),
        "database_files": len(db_files),
        "total": len(py_files) + len(db_files)
    },
    "python_files": py_files[:500],  # First 500 to avoid huge JSON
    "database_files": db_files,
    "truncated": len(py_files) > 500
}

# Save JSON
os.makedirs("reports/harmony_vFinal", exist_ok=True)
with open("reports/harmony_vFinal/phase0_inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Generate Markdown
md_content = f"""# Phase 0 - Complete File Inventory

Generated: {inventory['timestamp']}
Root: {inventory['root']}

## Statistics
- Python files: {inventory['statistics']['python_files']}
- Database files: {inventory['statistics']['database_files']}
- **Total: {inventory['statistics']['total']}**

## Python Files ({len(py_files)} files)
"""

for i, f in enumerate(py_files[:100], 1):
    md_content += f"{i}. `{f}`\n"

if len(py_files) > 100:
    md_content += f"\n... and {len(py_files) - 100} more Python files\n"

md_content += f"\n## Database Files ({len(db_files)} files)\n"
for i, f in enumerate(db_files, 1):
    md_content += f"{i}. `{f}`\n"

if not db_files:
    md_content += "No database files found.\n"

with open("reports/harmony_vFinal/phase0_inventory.md", "w") as f:
    f.write(md_content)

print(f"Inventory complete: {len(py_files)} .py, {len(db_files)} .db")
