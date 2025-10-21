from apps.scripturemon.bootstrap import ensure_bootstrap_once
ctx1 = ensure_bootstrap_once()
ctx2 = ensure_bootstrap_once()
print("✅ Singleton works" if ctx1 is ctx2 else "❌ Not singleton")
print(f"   Memory OK: {ctx1.get('memory_ok')}")
print(f"   Canonical: {ctx1.get('memory_canonical')}")
