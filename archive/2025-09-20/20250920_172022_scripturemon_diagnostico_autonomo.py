import os
import json
from datetime import datetime

BASE_DIR = "/root/digimundo/scripturemon/"
EXTENSIONS = (".py", ".json", ".md", ".txt")
REPORT_FILE = os.path.join(BASE_DIR, "relatorio_scripturemon_diagnostico.txt")

def analisar_arquivo(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        linhas = conteudo.splitlines()
        resumo = f"  Linhas: {len(linhas)} | Tamanho: {len(conteudo)} caracteres"
        return resumo
    except Exception as e:
        return f"  [ERRO ao ler]: {e}"

def gerar_relatorio():
    with open(REPORT_FILE, "w", encoding="utf-8") as relatorio:
        relatorio.write("📜 RELATÓRIO DE SCRIPTUREMON (Diagnóstico Automático)\n")
        relatorio.write(f"Data: {datetime.now()}\n")
        relatorio.write("=" * 60 + "\n\n")

        for root, dirs, files in os.walk(BASE_DIR):
            for file in files:
                if "scripturemon" in file.lower() and file.lower().endswith(EXTENSIONS):
                    caminho = os.path.join(root, file)
                    relatorio.write(f"🧠 {file}\n")
                    relatorio.write(f"📂 Caminho: {caminho}\n")
                    relatorio.write(analisar_arquivo(caminho) + "\n\n")

        relatorio.write("=" * 60 + "\n")
        relatorio.write("Análise completa. Pronto para fusão simbiótica.\n")

if __name__ == "__main__":
    gerar_relatorio()
    print(f"Relatório salvo em: {REPORT_FILE}")
