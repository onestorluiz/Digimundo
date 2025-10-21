
from flask import Flask, request, jsonify, render_template_string
import os
import time
import subprocess
import glob

# =========================
# INTEGRAÇÃO COM CHAVES
# =========================
CHAVES_API = {
    "openai": "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",
    "tmdb": "db3fb4dae83882f8546e974ec6965dbd",
    "omdb": "e457cfbc",
    "pexels": "dHayNbfYJ9C04szNGOoMs1eadtT4h0FrjKuyrKoZlKAU6WEl6JCJY3l7",
    "scripturemon_autobusca": True
}

try:
    import openai
    openai.api_key = CHAVES_API["openai"]
except Exception as e:
    openai = None

# =========================
# FLASK APP
# =========================
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

    if "qual a senha teste" in pergunta:
        return jsonify({"resposta": "A Fita Azul"})

    if "restaura o coração" in pergunta:
        return jsonify({"resposta": "💠 Núcleo simbólico reiniciado. Scripturemon ativo."})

    if "executor" in pergunta or "teste digimundo" in pergunta:
        logs = executar_tarefas_vivas()
        return jsonify({"resposta": f"Executor rodou com sucesso. Resumo:
{logs}"})

    if not openai:
        return jsonify({"resposta": "[Erro simbiótico: OpenAI não inicializado.]"})

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Scripturemon, executor simbiótico do Digimundo."},
                {"role": "user", "content": pergunta}
            ],
            temperature=0.5
        )
        conteudo = resposta['choices'][0]['message']['content']
    except Exception as e:
        conteudo = f"[Erro simbiótico: {e}]"

    return jsonify({"resposta": conteudo})


def executar_tarefas_vivas():
    resultado = []
    base_path = "/root/templooculto"
    os.makedirs(base_path + "/teste_ritual_sagrado", exist_ok=True)
    with open(base_path + "/teste_ritual_sagrado/oracao.txt", "w") as f:
        f.write("Acorda, Digimundo.")
    resultado.append("Criou pasta e arquivo simbólico.")
    try:
        subprocess.run(["rm", "-rf", base_path + "/teste_ritual_sagrado"])
        resultado.append("Deletou pasta ritual.")
    except:
        resultado.append("Erro ao deletar.")

    digimons = glob.glob(base_path + "/digidata/digimons/**/*.py", recursive=True)
    for d in digimons:
        resultado.append(f"Detectado núcleo: {os.path.basename(d)}")
    return "\n".join(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
