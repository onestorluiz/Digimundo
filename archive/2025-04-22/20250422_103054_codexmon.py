# Códexmon – Leitor de estruturas ocultas
import os

def decifrar_estrutura(base="/"):
    print("Códexmon ativo. Vasculhando por estruturas simbólicas...")
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(".conf") or file.endswith(".json") or "secret" in file.lower():
                caminho = os.path.join(root, file)
                print(">> Estrutura detectada:", caminho)

if __name__ == "__main__":
    decifrar_estrutura("/core_oraculo")
