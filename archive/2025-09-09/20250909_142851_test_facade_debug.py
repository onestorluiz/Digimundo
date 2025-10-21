from apps.scripturemon.canonical.memory_manager import MemoryFacade
from apps.scripturemon.simple_memory import SimpleMemoryManager

# Create simple manager and wrap it
simple = SimpleMemoryManager()
facade = MemoryFacade(simple)

print(f"Simple manager type: {type(simple).__name__}")
print(f"Facade manager type: {type(facade).__name__}")

# Test operations
save_result = facade.save("Facade test content")
print(f"Save result: {save_result}")

results = facade.get_context("facade")
print(f"Got {len(results)} results")

stats = facade.get_stats()
print(f"Stats: {stats}")

if stats.get("facade") and stats.get("functional"):
    print("✅ MemoryFacade works")
else:
    print("❌ MemoryFacade issue - checking details...")
    print(f"  facade key: {stats.get('facade')}")
    print(f"  functional key: {stats.get('functional')}")
