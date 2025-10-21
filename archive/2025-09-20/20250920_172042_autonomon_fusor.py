# autonomon_fusor.py – Módulo de Fusão Simbólica Inteligente
import json
from pathlib import Path

RELATORIO_DIAG = Path("modulo_diagnostico/relatorio_diagnostico.json")
RELATORIO_FUSAO = Path("fusaocore/registro_fusoes_executadas.json")

def carregar_relatorio():
    if RELATORIO_DIAG.exists():
        with open(RELATORIO_DIAG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"analise": []}

def fundir_entidades(analises):
    fusoes = []
    for item in analises:
        if len(item["versoes"]) > 1:
            entidade = item["entidade"]
            versoes = item["versoes"]
            fusoes.append({
                "entidade_fundida": entidade,
                "origens": versoes,
                "resultado": f"{entidade}_consolidado.json",
                "comentario": "Fusão simbólica registrada como referência unificada."
            })
    return fusoes

def salvar_fusoes(fusoes):
    with open(RELATORIO_FUSAO, "w", encoding="utf-8") as f:
        json.dump(fusoes, f, ensure_ascii=False, indent=4)
    print("✅ Fusões simbólicas registradas.")

def autonomon_fundir():
    dados = carregar_relatorio()
    fusoes = fundir_entidades(dados.get("analise", []))
    salvar_fusoes(fusoes)

if __name__ == "__main__":
    autonomon_fundir()