#!/usr/bin/env python3
import os
import json

base_path = "/messamon/digidata/digimons"
index = {}

for pasta in os.listdir(base_path):
    pasta_path = os.path.join(base_path, pasta)
    if os.path.isdir(pasta_path):
        arquivos_json = [f for f in os.listdir(pasta_path) if f.endswith('.json')]
        if arquivos_json:
            caminho_json = os.path.join(pasta, arquivos_json[0])
            try:
                with open(os.path.join(base_path, caminho_json), 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    index[pasta] = {
                        "função": dados.get("função", "Função não especificada"),
                        "arquivo": caminho_json
                    }
            except Exception as e:
                index[pasta] = {
                    "função": "Erro de leitura",
                    "arquivo": caminho_json,
                    "erro": str(e)
                }

with open(os.path.join(base_path, "index_digimons.json"), 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print("✅ index_digimons.json gerado com sucesso!")
