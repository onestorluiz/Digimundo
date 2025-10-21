
import zipfile, os
from pathlib import Path

FONTE = Path("/root/templo_digimundo/Digimundo Vivo")
DESTINO = Path("/root/templo_digimundo/digimundo_estruturado")

def organizar_fases():
    for zipfile_path in FONTE.glob("*.zip"):
        destino_fase = DESTINO / zipfile_path.stem
        destino_fase.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
            zip_ref.extractall(destino_fase)
        print(f"✅ Fase {zipfile_path.stem} organizada.")

if __name__ == "__main__":
    organizar_fases()
