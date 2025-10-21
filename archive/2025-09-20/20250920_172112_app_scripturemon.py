
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

@app.route('/')
def index():
    return render_template("interface_conversas_scripturemon.html")

@app.route('/enviar_comando', methods=['POST'])
def enviar_comando():
    data = request.get_json()
    comando = data.get("comando", "").strip()

    if not comando:
        return jsonify({"resposta": "❗Erro: Nenhum comando simbólico foi recebido."}), 400

    resposta = f"🧠 SCRIPTUREMON RESPONDEU:
"{comando.upper()}"
*Ação simbólica reconhecida. Integrações iniciadas.*"
    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
