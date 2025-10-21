# codex_eternus.py — Validador simbólico do Digimundo

import os

def validar_estrutura():
    print("📜 Validando estrutura do Digimundo...")
    caminhos_esperados = [
        "/root/digimundo_vivo/ascenso/scripturemon/scripts",
        "/root/digimundo_vivo/ascenso/scripturemon/nucleo",
        "/root/digimundo_vivo/ascenso/scripturemon/digimundo/scripts",
        "/root/digimundo_vivo/ascenso/scripturemon/digimundo/nucleo"
    ]
    for caminho in caminhos_esperados:
        if not os.path.exists(caminho):
            print(f"⚠️ Criando caminho ausente: {caminho}")
            os.makedirs(caminho, exist_ok=True)
    print("✅ Codex Eternus validado com sucesso.")

if __name__ == "__main__":
    validar_estrutura()
