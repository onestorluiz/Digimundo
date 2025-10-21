import os
import json
from datetime import datetime

class Auditramon:
    def __init__(self, target_dir="/messamon/digidata/digimons/"):
        self.target_dir = target_dir
        self.relatorio = []

    def auditar_jsons(self):
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith(".json"):
                    caminho = os.path.join(root, file)
                    try:
                        with open(caminho, "r") as f:
                            json.load(f)
                        self.relatorio.append(f"✅ {caminho} válido")
                    except Exception as e:
                        self.relatorio.append(f"❌ {caminho} inválido: {e}")

    def salvar_relatorio(self):
        os.makedirs("auditramon/memoria", exist_ok=True)
        nome = datetime.now().strftime("memoria/%Y-%m-%d_auditoria_tora.md")
        with open(f"auditramon/{nome}", "w") as f:
            f.write("\n".join(self.relatorio))

if __name__ == "__main__":
    auditor = Auditramon()
    auditor.auditar_jsons()
    auditor.salvar_relatorio()