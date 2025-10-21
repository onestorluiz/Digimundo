import json
import os

def avaliar_logs(diretorio_logs):
    resultados = []
    for arquivo in os.listdir(diretorio_logs):
        if arquivo.endswith(".json"):
            caminho = os.path.join(diretorio_logs, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                resultado = dados.get("resultado", "").lower()

                if "sucesso" in resultado:
                    status = "eficiente"
                elif "latente" in resultado or "aguarda" in resultado:
                    status = "latente"
                elif "falha" in resultado:
                    status = "ineficiente"
                else:
                    status = "potencial"

                resultados.append({
                    "digimon": dados.get("digimon"),
                    "acao": dados.get("acao"),
                    "avaliacao": status
                })
    return resultados

if __name__ == "__main__":
    logs_dir = "logs"
    avaliacoes = avaliar_logs(logs_dir)
    for a in avaliacoes:
        print(f"[{a['digimon']}] Ação: {a['acao']} → {a['avaliacao']}")