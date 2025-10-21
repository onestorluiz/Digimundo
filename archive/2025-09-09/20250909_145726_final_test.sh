#!/bin/bash
echo "================================"
echo "FINAL BOOTSTRAP & ENTRYPOINT TEST"
echo "================================"
echo ""

echo "1. Testing unified entrypoint (bin/scripturemon)..."
bin/scripturemon help 2>&1 | grep -q "usage:" && echo "✅ Help works" || echo "❌ Help failed"

echo ""
echo "2. Testing symlink compatibility (bin/scripturemon-cli)..."
bin/scripturemon-cli version 2>&1 | grep -q "Scripturemon" && echo "✅ Symlink works" || echo "❌ Symlink failed"

echo ""
echo "3. Testing canonical memory status..."
STATUS=$(bin/scripturemon status 2>&1)
echo "$STATUS" | grep -q "Implementation: apps.scripturemon" && echo "✅ Shows implementation path" || echo "❌ Missing impl path"
echo "$STATUS" | grep -q "Probe: pass" && echo "✅ Probe passes" || echo "❌ Probe fails"

echo ""
echo "4. Testing memory persistence..."
cat > test_mem.py << 'INNER'
from apps.scripturemon.canonical.memory_manager import get_memory_manager
mm = get_memory_manager()
mm.save("Final test content")
results = mm.get_context("final")
print("✅ Memory works" if len(results) > 0 else "❌ Memory failed")
INNER
python3 test_mem.py

echo ""
echo "5. Testing bootstrap singleton..."
cat > test_bootstrap.py << 'INNER'
from apps.scripturemon.bootstrap import ensure_bootstrap_once
ctx1 = ensure_bootstrap_once()
ctx2 = ensure_bootstrap_once()
print("✅ Singleton works" if ctx1 is ctx2 else "❌ Not singleton")
print(f"   Memory OK: {ctx1.get('memory_ok')}")
print(f"   Canonical: {ctx1.get('memory_canonical')}")
INNER
python3 test_bootstrap.py

echo ""
echo "================================"
echo "SUMMARY"
echo "================================"
