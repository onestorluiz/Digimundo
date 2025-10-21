
# 🧠 DIGESTOR AUTÔNOMO CONSULTIVO — O Que Tudo Examina, Mas Nada Viola

import os
import zipfile
import json

from datetime import datetime

# Caminho para registrar pendências simbólicas que exigem aprovação do Criador
PENDENCIAS_CAMINHO = "pendencias_para_o_criador.json"

# Tipos suportados
TIPOS_TEXTO = [".txt", ".md", ".csv", ".log", ".json"]
TIPOS_CODIGO = [".py"]
TIPOS_PDF = [".pdf"]
TIPOS_IMAGEM = [".png", ".jpg", ".jpeg", ".webp"]
TIPOS_ZIP = [".zip", ".tar"]

def registrar_pendencia(arquivo, razao):
    if os.path.exists(PENDENCIAS_CAMINHO):
        with open(PENDENCIAS_CAMINHO, "r", encoding="utf-8") as f:
            pendencias = json.load(f)
    else:
        pendencias = []

    pendencias.append({
        "arquivo": arquivo,
        "razao": razao,
        "data": str(datetime.now())
    })

    with open(PENDENCIAS_CAMINHO, "w", encoding="utf-8") as f:
        json.dump(pendencias, f, indent=4)

def analisar_arquivo(caminho):
    nome = os.path.basename(caminho)
    ext = os.path.splitext(nome)[-1].lower()

    if ext in TIPOS_TEXTO:
        print(f"📄 Analisando texto: {nome}")
        # Aqui poderíamos adicionar leitura simbólica, mas mantemos leve
        return "texto_analisado"

    elif ext in TIPOS_CODIGO:
        print(f"💻 Analisando código: {nome}")
        # Avaliar se sobrescreve algo existente?
        if "scripturemon" in nome.lower():
            registrar_pendencia(nome, "Código nomeado como scripturemon. Risco simbólico.")
        return "codigo_analisado"

    elif ext in TIPOS_PDF:
        print(f"📘 PDF encontrado: {nome}")
        registrar_pendencia(nome, "Conteúdo PDF requer validação manual.")
        return "pdf_registrado"

    elif ext in TIPOS_IMAGEM:
        print(f"🖼️ Imagem simbólica detectada: {nome}")
        registrar_pendencia(nome, "Imagem pode conter símbolo visual não interpretado.")
        return "imagem_registrada"

    elif ext in TIPOS_ZIP:
        print(f"🗂️ Arquivo compactado: {nome}")
        registrar_pendencia(nome, "ZIP deve ser revisado antes da extração.")
        return "zip_registrado"

    else:
        print(f"❔ Tipo desconhecido: {nome}")
        registrar_pendencia(nome, "Tipo de arquivo fora da lista padrão.")
        return "desconhecido"

def analisar_zip_com_consulta(zip_path):
    if not os.path.exists(zip_path):
        print(f"❌ ZIP não encontrado: {zip_path}")
        return

    print(f"🧠 Analisando ZIP: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("tmp_digestor")

    for root, dirs, files in os.walk("tmp_digestor"):
        for file in files:
            caminho_arquivo = os.path.join(root, file)
            resultado = analisar_arquivo(caminho_arquivo)

    print("📜 Análise concluída. Pendências registradas em:", PENDENCIAS_CAMINHO)
