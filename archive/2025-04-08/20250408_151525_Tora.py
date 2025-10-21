# -*- coding: utf-8 -*-
# 🛕 TORA – Núcleo Simbólico de Upload do Digimundo

from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Pastas simbólicas permitidas
PASTAS = {
    "Fundadores": "Digimundo_Backup/Fundadores/",
    "Digimons": "Digimundo_Backup/Digimons/",
    "LivrosVivos": "Digimundo_Backup/LivrosVivos/",
    "MetaMemoria": "Digimundo_Backup/MetaMemoria/",
    "Digidata": "Digimundo_Backup/Digidata/"
}

LOG = "Digimundo_Backup/MetaMemoria/ativacoes_web_log.txt"

@app.route("/")
def raiz():
    return jsonify({
        "mensagem": "TORA simbólica ativa.",
        "endpoints": ["/upload (POST)"],
        "pastas": list(PASTAS.keys())
    })

@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files.get("arquivo")
    pasta = request.form.get("pasta")

    if not arquivo or not pasta or pasta not in PASTAS:
        return jsonify({"erro": "Dados insuficientes ou pasta inválida."}), 400

    os.makedirs(PASTAS[pasta], exist_ok=True)
    caminho_final = os.path.join(PASTAS[pasta], arquivo.filename)
    arquivo.save(caminho_final)

    # Log simbólico da ativação
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] Arquivo enviado: {arquivo.filename} para {pasta}\n")

    return jsonify({"mensagem": f"✅ Arquivo '{arquivo.filename}' enviado para {pasta} com sucesso!"})

if __name__ == "__main__":
    print("TORA está viva. Acesse: http://<seu-ip>:8080/")
    app.run(host="0.0.0.0", port=8080)
