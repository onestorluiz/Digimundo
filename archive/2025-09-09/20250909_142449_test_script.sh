#!/bin/bash
# Test script for memory fix validation

echo "================================"
echo "MEMORY FIX VALIDATION TEST"
echo "================================"
echo ""

# Clear cache
rm -f runtime/canonical.json

echo "1. Testing help command..."
bin/scripturemon help 2>&1 | grep -q "usage:" && echo "✅ Help works" || echo "❌ Help failed"

echo ""
echo "2. Testing status command..."
STATUS_OUTPUT=$(bin/scripturemon status 2>&1)
echo "$STATUS_OUTPUT" | grep -q "Memory Manager: OK" && echo "✅ Memory Manager: OK" || echo "❌ Memory Manager: ERROR"
echo "$STATUS_OUTPUT" | grep -q "Telepathy: MOCK" && echo "✅ Telepathy fallback works" || echo "❌ Telepathy failed"
echo "$STATUS_OUTPUT" | grep -q "Monitor: ENABLED" && echo "✅ Monitor enabled" || echo "❌ Monitor failed"

echo ""
echo "3. Testing memory persistence..."
cat > test_memory.py << 'EOF'
from apps.scripturemon.canonical.memory_manager import get_memory_manager

mm = get_memory_manager()
print(f"Memory type: {type(mm).__name__}")

# Test save
result = mm.save("Test memory content", memory_type="test")
print(f"Save result: {result}")

# Test retrieve
memories = mm.get_context("test")
print(f"Retrieved {len(memories)} memories")

# Test stats
stats = mm.get_stats()
print(f"Stats: functional={stats.get('functional')}, type={stats.get('type')}")
EOF

python3 test_memory.py 2>&1 | grep -q "functional=True" && echo "✅ Memory operations work" || echo "❌ Memory operations failed"

echo ""
echo "4. Testing async tools..."
cat > test_async.py << 'EOF'
from apps.scripturemon.utils.async_tools import call_maybe_async
import asyncio

# Test sync function
def sync_func(x):
    return x * 2

# Test async function
async def async_func(x):
    await asyncio.sleep(0.01)
    return x * 3

# Test both
sync_result = call_maybe_async(sync_func, 5)
async_result = call_maybe_async(async_func, 5)

print(f"Sync result: {sync_result}")
print(f"Async result: {async_result}")
print("✅ Async tools working" if sync_result == 10 and async_result == 15 else "❌ Async tools failed")
EOF

python3 test_async.py 2>&1 | grep -q "✅ Async tools working" && echo "✅ Async tools work" || echo "❌ Async tools failed"

echo ""
echo "5. Testing MemoryFacade..."
cat > test_facade.py << 'EOF'
from apps.scripturemon.canonical.memory_manager import MemoryFacade, SimpleMemoryManager

# Create simple manager and wrap it
simple = SimpleMemoryManager()
facade = MemoryFacade(simple)

# Test operations
facade.save("Facade test content")
results = facade.get_context("facade")
stats = facade.get_stats()

print("✅ MemoryFacade works" if stats.get("facade") and stats.get("functional") else "❌ MemoryFacade failed")
EOF

python3 test_facade.py 2>&1 | grep -q "✅ MemoryFacade works" && echo "✅ MemoryFacade works" || echo "❌ MemoryFacade failed"

echo ""
echo "================================"
echo "TEST SUMMARY"
echo "================================"

# Count results
TOTAL=$(grep -c "✅\|❌" <<< "$(./reports/harmony_vFinal/memory_fix/test_script.sh 2>&1)")
SUCCESS=$(grep -c "✅" <<< "$(./reports/harmony_vFinal/memory_fix/test_script.sh 2>&1)")

echo "Tests passed: $SUCCESS/$TOTAL"