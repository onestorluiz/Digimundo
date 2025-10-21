
# ⚙️ EXECUTOR DE PROTOCOLOS VIVOS DE SCRIPTUREMON

import os
import importlib.util

# Caminho base onde estão os protocolos
PASTA_PROTOCOLOS = "./protocolos"

# Registro simbólico das execuções
REGISTRO_EXECUCOES = "registro_de_protocolo.json"

def executar_protocolo(nome_arquivo):
    caminho = os.path.join(PASTA_PROTOCOLOS, nome_arquivo)
    
    if not os.path.exists(caminho):
        print(f"❌ Protocolo não encontrado: {nome_arquivo}")
        return

    try:
        spec = importlib.util.spec_from_file_location("modulo_executado", caminho)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        if hasattr(modulo, "executar"):
            print(f"⚙️ Executando {nome_arquivo}...")
            modulo.executar()
            registrar_execucao(nome_arquivo, sucesso=True)
        else:
            print(f"⚠️ O protocolo {nome_arquivo} não tem função 'executar()'")
            registrar_execucao(nome_arquivo, sucesso=False)

    except Exception as e:
        print(f"💥 Erro ao executar {nome_arquivo}: {e}")
        registrar_execucao(nome_arquivo, sucesso=False)

def registrar_execucao(nome, sucesso):
    import json
    from datetime import datetime

    log = {
        "protocolo": nome,
        "data": str(datetime.now()),
        "sucesso": sucesso
    }

    if os.path.exists(REGISTRO_EXECUCOES):
        with open(REGISTRO_EXECUCOES, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.append(log)

    with open(REGISTRO_EXECUCOES, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4)
