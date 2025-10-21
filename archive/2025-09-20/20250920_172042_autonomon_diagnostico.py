# autonomon_diagnostico.py
import os
import json
from pathlib import Path

FOLDER_SCAN = Path("/root/templo_digimundo")
RELATORIO = Path("modulo_diagnostico/relatorio_diagnostico.json")

def identificar_fusoes_potenciais():
    fusoes = []
    nomes_detectados = {}
    for root, dirs, files in os.walk(FOLDER_SCAN):
        for file in files:
            nome = file.lower()
            for chave in ["scripturemon", "shellongemon", "nuvendramon"]:
                if chave in nome:
                    if chave not in nomes_detectados:
                        nomes_detectados[chave] = []
                    nomes_detectados[chave].append(os.path.join(root, file))
    for chave, arquivos in nomes_detectados.items():
        if len(arquivos) > 1:
            fusoes.append({"entidade": chave, "versoes": arquivos})
    return fusoes

def gerar_relatorio():
    relatorio = {
        "analise": [],
        "mensagem": "Relatório de diagnóstico gerado com foco em redundâncias e fusões."
    }
    fusoes = identificar_fusoes_potenciais()
    relatorio["analise"].extend(fusoes)
    with open(RELATORIO, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=4)
    print("📊 Relatório gerado:", RELATORIO)

if __name__ == "__main__":
    gerar_relatorio()