# Smart Imports e Lazy Loading
import importlib
from functools import lru_cache

class LazyImporter:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def __getattr__(self, name: str):
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return getattr(self._module, name)

# Lazy imports para módulos pesados
numpy = LazyImporter("numpy")
pandas = LazyImporter("pandas")
sklearn = LazyImporter("sklearn")

@lru_cache(maxsize=128)
def cached_import(module_name: str):
    return importlib.import_module(module_name)
