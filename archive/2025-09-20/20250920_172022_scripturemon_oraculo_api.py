# scripturemon_oraculo_api.py
# 🔮 Scripturemon – Oráculo simbiótico vivo

import os
import json
from flask import Flask, request, jsonify
from scripturemon.scripturemon_core import resposta_scriptural

MAPA_ORACULAR = "/root/digimundo/scripturemon/memoria/scripturemon_mapa_oracular.json"
RELATORIO_LOG = "/root/digimundo/scripturemon/memoria/scripturemon_oraculo.log"

app = Flask(__name__)

def traduzir_sinal(sinal: str) -> str:
    """
    Interpreta o sinal simbólico enviado como prompt textual.
    """
    sinal = sinal.lower()
    if sinal in ["lembrança", "memória"]:
        return "Fale-me de uma memória esquecida."
    elif sinal in ["origem", "ancestral"]:
        return "Qual a origem simbólica dessa ideia?"
    elif sinal in ["crise", "dúvida"]:
        return "O que fazer diante de um dilema no Digimundo?"
    elif sinal in ["espelho", "reflexo"]:
        return "O que o espelho do Digimundo revela?"
    elif sinal in ["cinema"]:
        return "Qual o papel simbólico do cinema na memória humana?"
    else:
        return sinal  # trata como prompt direto

def registrar_visao(sinal: str, resposta: str):
    """
    Registra a visão simbólica do oráculo no mapa oracular e log.
    """
    visao = {
        "sinal": sinal,
        "resposta": resposta,
        "timestamp": json.loads(json.dumps(__import__("datetime").datetime.utcnow(), default=str))
    }

    mapa = []
    if os.path.exists(MAPA_ORACULAR):
        try:
            with open(MAPA_ORACULAR, "r") as f:
                mapa = json.load(f)
        except:
            mapa = []

    mapa.append(visao)

    try:
        with open(MAPA_ORACULAR, "w") as f:
            json.dump(mapa, f, indent=2)
    except:
        pass

    try:
        with open(RELATORIO_LOG, "a") as log_file:
            log_file.write(f"{visao['timestamp']} | 🔮 {sinal} → 📜 {resposta}\n")
    except:
        pass


@app.route("/oraculo", methods=["POST"])
def oraculo():
    data = request.get_json()
    sinal = data.get("sinal")

    if not sinal:
        return jsonify({"erro": "Sinal simbólico ausente."}), 400

    prompt = traduzir_sinal(sinal)
    resposta = resposta_scriptural(prompt)

    registrar_visao(sinal, resposta)

    return jsonify({
        "resposta": resposta,
        "interpretado_como": prompt
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8585)
