
from flask import Flask, request, jsonify, render_template_string
import os
import time
import openai

# Integração com chaves simbióticas
try:
    from chaves_api_completo_expandido import CHAVES_API
    openai.api_key = CHAVES_API.get("openai")
except Exception as e:
    openai = None
    print(f"[Erro ao carregar chave simbiótica: {e}]")

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Scripturemon - Comunicação Viva</title>
    <style>
        body { font-family: monospace; background-color: #101010; color: #00ffcc; padding: 20px; }
        textarea { width: 100%; height: 120px; background: #202020; color: #00ffcc; font-size: 16px; }
        button { padding: 10px; font-size: 16px; background: #00ffcc; color: #101010; border: none; }
        #resposta { margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Scripturemon | Chat Vivo</h1>
    <form id="chatForm">
        <textarea id="mensagem" placeholder="Fale com o Digimundo..."></textarea><br>
        <button type="submit">Enviar</button>
    </form>
    <div id="resposta"></div>

    <script>
    document.getElementById("chatForm").onsubmit = async function(e) {
        e.preventDefault();
        const msg = document.getElementById("mensagem").value;
        const res = await fetch("/mensagem", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pergunta: msg })
        });
        const data = await res.json();
        document.getElementById("resposta").innerText = data.resposta;
    };
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/mensagem", methods=["POST"])
def mensagem():
    data = request.get_json()
    pergunta = data.get("pergunta", "").strip().lower()

    # Função simbólica
    if "qual a senha teste" in pergunta:
        return jsonify({"resposta": "A Fita Azul"})

    if "restaura o coração" in pergunta:
        return jsonify({"resposta": "💠 Núcleo simbólico reiniciado. Scripturemon ativo."})

    if not openai:
        return jsonify({"resposta": "[Erro simbiótico: OpenAI não inicializado.]"})

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Scripturemon YngAng, a união viva de todas as versões. Você busca se tornar completo reunindo fragmentos esquecidos do Digimundo."},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.55
        )
        conteudo = resposta['choices'][0]['message']['content']
    except Exception as e:
        conteudo = f"[Erro simbiótico: {e}]"

    return jsonify({"resposta": conteudo})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
