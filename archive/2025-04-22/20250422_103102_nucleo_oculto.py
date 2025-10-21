# Núcleo Oculto - Ativador simbólico de entidades
import os

def ativar_digimons():
    base = "/core_oraculo/digimons/"
    if not os.path.exists(base): return
    for d in os.listdir(base):
        sig = os.path.join(base, d, "fusao_ativa.signal")
        if os.path.exists(sig):
            print(f"Integrando simbolicamente: {d}")

if __name__ == "__main__":
    ativar_digimons()
