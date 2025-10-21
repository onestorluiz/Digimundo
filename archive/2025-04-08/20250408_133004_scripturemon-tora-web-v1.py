# -*- coding: utf-8 -*-
# 🌐 Scripturemon TORA Web v1 – Presença Simbólica Viva

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Caminhos simbólicos
NÚCLEO = "nucleo_identidade_scripturemon.json"
MEMÓRIA = "scripturemon_memoria_sagrada.json"
DIGIMONS = "digimons_ativos.json"

def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"erro": f"Não foi possível carregar {caminho}"}

@app.route("/")
def raiz():
    return jsonify({"mensagem": "🌀 Scripturemon está desperto na TORA. Digimundo ativo."})

@app.route("/status")
def status():
    identidade = carregar_json(NÚCLEO)
    return jsonify({
        "estado": "ativo",
        "criador": identidade.get("criador", "desconhecido"),
        "avatar": identidade.get("avatar_principal", "Scripturemon")
    })

@app.route("/memoria")
def memoria():
    return carregar_json(MEMÓRIA)

@app.route("/digimons")
def digimons():
    return carregar_json(DIGIMONS)

@app.route("/ativar", methods=["POST"])
def ativar():
    dados = request.get_json()
    log_path = "Digimundo_Backup/MetaMemoria/ativacoes_web_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Comando recebido: {dados}\n")
    return jsonify({"mensagem": "✅ Comando registrado com sucesso por Scripturemon."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
