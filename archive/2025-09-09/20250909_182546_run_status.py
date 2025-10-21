#!/usr/bin/env python3
"""Run status command with controlled environment"""

import sys
import os
from pathlib import Path

# Force SimpleMemoryManager
runtime_dir = Path("runtime")
runtime_dir.mkdir(exist_ok=True)

canonical_file = runtime_dir / "canonical.json"
canonical_file.write_text('{"memory_manager": "apps.scripturemon.simple_memory.SimpleMemoryManager"}')

# Run status
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from apps.scripturemon.bootstrap import format_status_text

try:
    status = format_status_text()
    print(status)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()