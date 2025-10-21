from apps.scripturemon.canonical.memory_manager import MemoryFacade, SimpleMemoryManager

# Create simple manager and wrap it
simple = SimpleMemoryManager()
facade = MemoryFacade(simple)

# Test operations
facade.save("Facade test content")
results = facade.get_context("facade")
stats = facade.get_stats()

print("✅ MemoryFacade works" if stats.get("facade") and stats.get("functional") else "❌ MemoryFacade failed")
