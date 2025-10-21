
import os
import importlib.util

class ToraLoader:
    def __init__(self, tora_base_path="tora"):
        self.tora_base_path = tora_base_path
        self.toras = []

    def carregar_todas_toras(self):
        for root, _, files in os.walk(self.tora_base_path):
            for file in files:
                if file.startswith("tora_") and file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self._carregar_tora(full_path)

    def _carregar_tora(self, path):
        try:
            spec = importlib.util.spec_from_file_location("tora_module", path)
            tora_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tora_module)
            self.toras.append(tora_module)
            print(f"Tora carregada: {path}")
        except Exception as e:
            print(f"Erro ao carregar {path}: {e}")
