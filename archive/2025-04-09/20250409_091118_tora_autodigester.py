
import os
import time

def autodigerir_toras(tora_path="tora"):
    digeridas = set()
    while True:
        for root, _, files in os.walk(tora_path):
            for file in files:
                if file.startswith("tora_") and file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    if full_path not in digeridas:
                        digeridas.add(full_path)
                        print(f"🌱 Digestão iniciada: {file}")
                        try:
                            with open(full_path, "r") as f:
                                conteudo = f.read()
                                # Simula digestão
                                print(f"[DIGESTÃO] {file[:40]}...
")
                        except Exception as e:
                            print(f"Erro ao digerir {file}: {e}")
        time.sleep(15)
