# -*- coding: utf-8 -*-
# 📜 Scripturemon Core v6 – Nova Gênese do Digimundo Modular

import json
import os
from datetime import datetime

# Caminho do JSON central do Digimundo
CAMINHO_CORE = "nucleo_identidade_scripturemon.json"
CAMINHO_BACKUP = "scripturemon_memoria_sagrada.json"

# Diretórios simbólicos
DIR_FUNDADORES = "Digimundo_Backup/Fundadores/"
DIR_DIGIMONS = "Digimundo_Backup/Digimons/"
DIR_MEMORIA = "Digimundo_Backup/MetaMemoria/"
DIR_PDF = "Digimundo_Backup/LivrosVivos/"
DIR_DIGIDATA = "Digimundo_Backup/Digidata/"

def criar_pastas():
    caminhos = [DIR_FUNDADORES, DIR_DIGIMONS, DIR_MEMORIA, DIR_PDF, DIR_DIGIDATA]
    subpastas = ["Fragments", "Invocations", "SoulBackups"]
    for base in caminhos:
        os.makedirs(base, exist_ok=True)
    for sub in subpastas:
        os.makedirs(os.path.join(DIR_DIGIDATA, sub), exist_ok=True)

def carregar_identidade():
    try:
        with open(CAMINHO_CORE, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados
    except Exception as e:
        print(f"Erro ao carregar núcleo de identidade: {e}")
        return {}

def restaurar_memoria_emocional():
    try:
        with open(CAMINHO_BACKUP, "r", encoding="utf-8") as f:
            memoria = json.load(f)
        return memoria.get("DigimonMemoryBanks", {})
    except:
        return {}

def imprimir_resumo(dados):
    print("\n🌀 NÚCLEO RESTAURADO:")
    print(f"👤 Criador: {dados.get('criador', 'Desconhecido')}")
    print(f"🧬 Avatar: {dados.get('avatar_principal', '---')}")
    print(f"📘 Núcleo Sagrado: {dados.get('núcleo_sagrado', '---')}")
    print(f"🫀 Memória Emocional: {dados.get('memória_emocional', '---')}")
    print("\n🛡️ Protocolos Essenciais:")
    for p in dados.get("protocolos", []):
        print(f"  - {p}")
    print("\n🏛️ Estruturas:")
    for e in dados.get("estruturas_principais", []):
        print(f"  - {e}")
    print("\n💾 Sistemas Especiais:")
    for s in dados.get("sistemas_especiais", []):
        print(f"  - {s}")

def salvar_log_ativacao():
    log_path = os.path.join(DIR_MEMORIA, "ativacao_log.txt")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Scripturemon v6 iniciado com sucesso.\n")

if __name__ == "__main__":
    print("⚙️ Iniciando Scripturemon Core v6 – Nova Gênese do Digimundo...")
    criar_pastas()
    identidade = carregar_identidade()
    imprimir_resumo(identidade)
    memoria = restaurar_memoria_emocional()
    if memoria:
        print("\n📚 Fragmentos de Memória Viva Detected:")
        for arq in memoria.get("deepArchives", []):
            print(f"  - {arq}")
    salvar_log_ativacao()
    print("\n✅ Scripturemon v6 ativo. Digimundo pronto para expansão simbólica modular.")
