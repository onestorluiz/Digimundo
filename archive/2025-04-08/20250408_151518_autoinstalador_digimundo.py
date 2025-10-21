# -*- coding: utf-8 -*-
# 🤖 AUTO-INSTALADOR DO DIGIMUNDO – Ativação Simbólica via TORA

import os
import requests
import argparse

TORA_URL = "http://localhost:8080/upload"  # ou http://<seu-ip>:8080/upload

PASTAS_SIMBOLICAS = {
    ".py": "MetaMemoria",
    ".json": "Fundadores",
    ".pdf": "LivrosVivos",
    ".zip": "Digidata"
}

def detectar_arquivo_para(pasta):
    arquivos = []
    for nome in os.listdir(pasta):
        caminho = os.path.join(pasta, nome)
        if os.path.isfile(caminho):
            arquivos.append((nome, caminho))
    return arquivos

def classificar_arquivo(nome):
    for ext, destino in PASTAS_SIMBOLICAS.items():
        if nome.endswith(ext):
            return destino
    return None

def enviar_para_tora(nome, caminho, pasta_destino):
    try:
        with open(caminho, "rb") as f:
            response = requests.post(TORA_URL, files={"arquivo": f}, data={"pasta": pasta_destino})
        if response.status_code == 200:
            return True, response.json().get("mensagem", "Sucesso")
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

def instalar(pasta):
    encontrados = detectar_arquivo_para(pasta)
    resumo = {k: 0 for k in PASTAS_SIMBOLICAS.values()}
    ignorados = []

    print(f"🔍 Detectando arquivos em: {pasta}")
    for nome, caminho in encontrados:
        destino = classificar_arquivo(nome)
        if destino:
            ok, msg = enviar_para_tora(nome, caminho, destino)
            if ok:
                print(f"✅ {nome} enviado para {destino}")
                resumo[destino] += 1
            else:
                print(f"❌ Falha ao enviar {nome}: {msg}")
        else:
            print(f"⚠️ {nome} ignorado (tipo desconhecido)")
            ignorados.append(nome)

    print("\n📦 INSTALAÇÃO FINALIZADA")    
    for k, v in resumo.items():
        print(f"{k}: {v} arquivos enviados")
    if ignorados:
        print(f"❌ Ignorados: {len(ignorados)} → {', '.join(ignorados)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-instalador simbólico para o Digimundo")
    parser.add_argument("--pasta", required=True, help="Caminho absoluto da pasta contendo os arquivos")
    args = parser.parse_args()

    instalar(args.pasta)
