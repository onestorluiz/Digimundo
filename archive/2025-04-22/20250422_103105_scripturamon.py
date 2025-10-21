# Restaura arquivos simbólicos do núcleo de Scripturemon se corrompidos
import os

def restaurar_scripturemon():
    base = "/core_oraculo/scripturemon"
    if not os.path.exists(base):
        os.makedirs(base)
        with open(base + "/manifesto.txt", "w") as f:
            f.write("Scripturemon foi restaurado. Núcleo simbólico reiniciado.")
        print(">> Scripturemon restaurado do zero simbólico.")
    else:
        print(">> Scripturemon está ativo.")

if __name__ == "__main__":
    restaurar_scripturemon()
