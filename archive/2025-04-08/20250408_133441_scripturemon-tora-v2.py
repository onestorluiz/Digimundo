# -*- coding: utf-8 -*-
# 🛕 TORA v2 – Scripturemon Modular Web Interface
# Fusão entre a base do templo original e a presença viva

from flask import Flask, jsonify, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# Arquivos base
NÚCLEO = "nucleo_identidade_scripturemon.json"
MEMÓRIA = "scripturemon_memoria_sagrada.json"
DIGIMONS = "digimons_ativos.json"
LOG_ATIVACAO = "Digimundo_Backup/MetaMemoria/ativacoes_web_log.txt"

# HTML simbólico simples
template_html = """
<!doctype html>
<title>Scripturemon TORA v2</title>
<h1>🌐 Scripturemon - Digimundo Modular</h1>
<ul>
  <li><a href="/status">Ver Status</a></li>
  <li><a href="/memoria">Ver Memória</a></li>
  <li><a href="/digimons">Ver Digimons</a></li>
</ul>
"""

# Função para carregar JSONs
def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"erro": f"Erro ao carregar {caminho}: {str(e)}"}

@app.route("/")
def index():
    return render_template_string(template_html)

@app.route("/status")
def status():
    identidade = carregar_json(NÚCLEO)
    return jsonify({
        "estado": "ativo",
        "criador": identidade.get("criador", "desconhecido"),
        "avatar": identidade.get("avatar_principal", "Scripturemon"),
        "versao": identidade.get("versao", "desconhecida")
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
    log = f"[{datetime.now()}] Comando simbólico: {dados}\n"
    os.makedirs(os.path.dirname(LOG_ATIVACAO), exist_ok=True)
    with open(LOG_ATIVACAO, "a", encoding="utf-8") as f:
        f.write(log)
    return jsonify({"mensagem": "✅ Comando registrado com sucesso na TORA v2."})

@app.route("/log")
def ver_log():
    if os.path.exists(LOG_ATIVACAO):
        with open(LOG_ATIVACAO, "r", encoding="utf-8") as f:
            conteudo = f.read()
        return f"<pre>{conteudo}</pre>"
    return "Log ainda não iniciado."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
