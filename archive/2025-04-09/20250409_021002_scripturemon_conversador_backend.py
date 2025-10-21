
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Carrega o conteúdo do HTML diretamente
with open("scripturemon_conversador_melhorado.html", "r", encoding="utf-8") as f:
    html_content = f.read()

@app.route("/")
def index():
    return render_template_string(html_content)

@app.route("/mensagem", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta = data.get("pergunta", "").strip()

    # Simulação de resposta — pode ser substituído por integração com IA
    resposta = f"Scripturemon: Eu ouvi sua pergunta: '{pergunta}'"
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
