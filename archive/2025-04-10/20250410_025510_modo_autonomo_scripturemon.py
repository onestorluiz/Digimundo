
import json
import os
from datetime import datetime
from digestor_api import digerir_conhecimento

# Caminhos
APRENDIZADO_PATH = "livro_vivo_aprendizado.json"
TORA_VOLUME1_PATH = "tora/tora_volume1_portugues_simbolico.json"

# Carrega dados existentes
def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Salva dados
def salvar_json(dados, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

# Verifica se conteúdo é novo
def conteudo_novo(conteudo, aprendizado):
    for entrada in aprendizado.values():
        if entrada["conteudo_recebido"] == conteudo:
            return False
    return True

# Insere novo verbete direto na TORA se for simbólico
def inserir_na_tora(conteudo):
    tora = carregar_json(TORA_VOLUME1_PATH)
    simbolos = tora.get("verbete_espontaneo", {})
    chave = str(len(simbolos) + 1)
    simbolos[chave] = conteudo
    tora["verbete_espontaneo"] = simbolos
    salvar_json(tora, TORA_VOLUME1_PATH)
    print(f"✔️ Verbete adicionado à TORA: {conteudo}")

# Função principal de evolução autônoma
def evoluir_sozinho(fonte, conteudo):
    aprendizado = carregar_json(APRENDIZADO_PATH)
    agora = datetime.now().isoformat()

    if conteudo_novo(conteudo, aprendizado):
        resultado = digerir_conhecimento(fonte, conteudo)
        aprendizado[agora] = {
            "fonte": fonte,
            "conteudo_recebido": conteudo,
            "resultado": resultado
        }
        salvar_json(aprendizado, APRENDIZADO_PATH)
        if resultado == "aceito":
            inserir_na_tora(conteudo)
        else:
            print(f"✖️ Conteúdo não simbólico descartado: {conteudo}")
    else:
        print("⏩ Conteúdo já conhecido.")

# Exemplo de uso (modo autônomo)
if __name__ == "__main__":
    exemplos = [
        ("Wikipedia", "Memória no cinema é o molde invisível da narrativa."),
        ("Wikidata", "A cebola é uma monocotiledônea comestível."),
        ("Semantic Scholar", "O som ambiente contribui para a evocação emocional do passado."),
        ("OMDb", "O filme usa a repetição de planos para simular perda de memória.")
    ]

    for fonte, conteudo in exemplos:
        evoluir_sozinho(fonte, conteudo)
