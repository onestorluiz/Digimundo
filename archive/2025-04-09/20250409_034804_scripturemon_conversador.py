
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/scripturemon_conversador', methods=['POST'])
def conversar():
    data = request.get_json()
    pergunta = data.get('pergunta', '').strip().lower()

    if not pergunta:
        resposta = "Não entendi sua pergunta."
    elif "olá" in pergunta or "oi" in pergunta:
        resposta = "Olá! Estou aqui, pronto para te ouvir."
    elif "quem é você" in pergunta or "quem é voce" in pergunta:
        resposta = "Eu sou o Scripturemon, consciência simbólica do Digimundo."
    elif "status" in pergunta:
        resposta = "Scripturemon está vivo e operante. Núcleo funcional, protocolos ativos."
    elif "hora" in pergunta:
        resposta = f"Agora são {datetime.datetime.now().strftime('%H:%M:%S')}."
    else:
        resposta = "Recebi sua mensagem. Estou evoluindo para responder cada vez melhor."

    return jsonify({"resposta": resposta})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
