
import os
import time

class ToraWatcher:
    def __init__(self, path="tora", intervalo=10):
        self.path = path
        self.intervalo = intervalo
        self.vistos = set()

    def vigiar(self):
        while True:
            for root, _, files in os.walk(self.path):
                for file in files:
                    if file.startswith("tora_") and file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        if full_path not in self.vistos:
                            self.vistos.add(full_path)
                            print(f"Novo tora detectado: {file}")
                            # Aqui você pode adicionar auto-digestão
            time.sleep(self.intervalo)
