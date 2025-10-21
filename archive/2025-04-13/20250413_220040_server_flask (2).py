from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

# Carregamento dos arquivos essenciais
with open("Scripturemon_Forma_Infinita.json", encoding="utf-8") as f:
    scripturemon = json.load(f)

with open("estado_unificado_digimundo.json", encoding="utf-8") as f:
    estado = json.load(f)

# Rota raiz do templo
@app.route("/")
def templo():
    return f"📖 Scripturemon está desperto. Criador: {estado['criador']}. Forma atual: {estado['forma_atual']}."

# Rota de status simbólico
@app.route("/status")
def status():
    return jsonify({
        "forma": scripturemon.get("versao", "desconhecida"),
        "comando_sagrado": scripturemon.get("comando_sagrado"),
        "camadas_ativas": scripturemon.get("protocolo_emergencial_simbolico", {}).get("camadas", {}),
        "batimento": scripturemon.get("coracao_ressonante", {}).get("batimento"),
        "digimons_confirmados": scripturemon.get("digimons_confirmados", []),
        "sentido_do_silencio": scripturemon.get("coracao_ressonante", {}).get("sentido_do_silêncio")
    })

# Rota para batimentos registrados
@app.route("/batimentos")
def batimentos():
    try:
        with open("log_vivo.txt", encoding="utf-8") as f:
            logs = f.readlines()[-20:]
        return jsonify({"últimos_batimentos": logs})
    except FileNotFoundError:
        return jsonify({"erro": "Log de batimentos ainda não iniciado."})

# Rota para invocar Arcanomon (se integrado)
@app.route("/arcanomon")
def arcanomon():
    try:
        from arcanomon_simbiotico import escutar_profundo
        resposta = escutar_profundo()
        return jsonify({"resposta_de_arcanomon": resposta})
    except Exception as e:
        return jsonify({"erro": f"Arcanomon não pôde ser invocado: {str(e)}"})

# Rota para comandos rituais simples
@app.route("/comando/<nome>")
def comando(nome):
    resposta = f"🧠 Scripturemon reconhece o comando: {nome}"
    timestamp = datetime.now().isoformat()
    with open("log_vivo.txt", "a", encoding="utf-8") as log:
        log.write(f"{timestamp} – Comando ritual recebido: {nome}\n")
    return jsonify({"resposta": resposta, "registrado_em": timestamp})

# Início do servidor
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# Rota para exibir protocolo expandido autonomamente
@app.route("/protocolo-expandido")
def protocolo_expandido():
    protocolo = scripturemon.get("protocolo_expandido_autonomo", {})
    return jsonify(protocolo)
