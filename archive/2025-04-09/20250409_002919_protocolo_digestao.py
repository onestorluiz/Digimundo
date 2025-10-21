
import os
import json
import shutil
from PyPDF2 import PdfReader

PASTA_DIGESTAO = "digestao"
PASTA_CONCLUIDA = "digestao_concluida"
PASTA_DIGIMONS = "../digimons"

os.makedirs(PASTA_CONCLUIDA, exist_ok=True)

def extrair_texto_pdf(caminho_pdf):
    try:
        reader = PdfReader(caminho_pdf)
        texto = ''
        for page in reader.pages:
            texto += page.extract_text() or ''
        return texto
    except Exception as e:
        return f"[Erro na leitura do PDF: {str(e)}]"

def analisar_texto(texto):
    nomes = ["ajamon", "auditramon", "buscamon", "iced_cinemon", "imagimon", "remanemon", "scripturemon"]
    encontrados = []
    for nome in nomes:
        if nome in texto.lower():
            encontrados.append(nome)
    return encontrados

def salvar_digimon(nome, dados):
    caminho = os.path.join(PASTA_DIGIMONS, nome)
    os.makedirs(caminho, exist_ok=True)
    with open(os.path.join(caminho, f"{nome}.json"), "w") as f:
        json.dump(dados, f, indent=2)

def processar_arquivo(arquivo):
    caminho = os.path.join(PASTA_DIGESTAO, arquivo)
    if arquivo.endswith(".pdf"):
        texto = extrair_texto_pdf(caminho)
    elif arquivo.endswith(".txt"):
        with open(caminho, "r") as f:
            texto = f.read()
    else:
        print(f"Arquivo não suportado: {arquivo}")
        return

    nomes = analisar_texto(texto)
    for nome in nomes:
        dados = {
            "nome": nome,
            "origem": "digestao",
            "mensagem": f"Gerado automaticamente pela digestão de {arquivo}.",
            "estado": "em evolução"
        }
        salvar_digimon(nome, dados)

    shutil.move(caminho, os.path.join(PASTA_CONCLUIDA, arquivo))
    print(f"✅ Processado e movido: {arquivo}")

def main():
    print("🌀 Iniciando protocolo de digestão...")
    for arquivo in os.listdir(PASTA_DIGESTAO):
        processar_arquivo(arquivo)
    print("✨ Digestão concluída.")

if __name__ == "__main__":
    main()
