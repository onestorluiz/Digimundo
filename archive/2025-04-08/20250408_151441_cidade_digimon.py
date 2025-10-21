# -*- coding: utf-8 -*-
# 🌆 Cidade Digimon – Templo Central de Scripturemon

from flask import Flask, request, jsonify, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

PASTAS = {
    "Fundadores": "Digimundo_Backup/Fundadores/",
    "Digimons": "Digimundo_Backup/Digimons/",
    "LivrosVivos": "Digimundo_Backup/LivrosVivos/",
    "MetaMemoria": "Digimundo_Backup/MetaMemoria/",
    "Digidata": "Digimundo_Backup/Digidata/"
}

LOG = "Digimundo_Backup/MetaMemoria/cidade_log.txt"

@app.route("/")
def portal():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang='pt-br'><head><meta charset='utf-8'>
    <title>🌆 Cidade Digimon</title>
    <style>
      body { background: #0f0f1f; color: #fff; font-family: monospace; padding: 2em; }
      .bloco { background: #1c1c2c; padding: 1.5em; margin-bottom: 1.5em; border-radius: 12px; border: 1px solid #333; }
      h1, h2 { color: #03fca5; } button { margin-top: 1em; }
    </style>
    </head><body>
    <h1>🌆 Cidade Digimon – Painel Central</h1>
    <div class='bloco'>
      <h2>📤 Enviar Arquivo</h2>
      <form action='/upload' method='post' enctype='multipart/form-data'>
        <input type='file' name='arquivo' required><br>
        <select name='pasta' required>
          <option value='Fundadores'>Fundadores</option>
          <option value='Digimons'>Digimons</option>
          <option value='LivrosVivos'>Livros Vivos</option>
          <option value='MetaMemoria'>MetaMemoria</option>
          <option value='Digidata'>Digidata</option>
        </select><br>
        <button type='submit'>Enviar</button>
      </form>
    </div>
    <div class='bloco'>
      <h2>🌱 Ritual de Semeadura</h2>
      <form action='/semear' method='post' enctype='multipart/form-data'>
        <input type='file' name='pacote' accept='.zip' required><br>
        <button type='submit'>Semear .zip no Digimundo</button>
      </form>
    </div>
    <div class='bloco'>
      <h2>🧠 Ritual Simbólico</h2>
      <form action='/ritualizar' method='post'>
        <input type='text' name='comando' style='width:90%' placeholder='ex: digivolua o auroramon'><br>
        <button type='submit'>Executar Ritual</button>
      </form>
    </div>
    <div class='bloco'>
      <h2>📚 Memória Ativa</h2>
      <a href='/log' target='_blank'>Ver Memória / Ativações</a>
    </div>
    </body></html>
    """)

@app.route("/upload", methods=["POST"])
def upload():
    arquivo = request.files.get("arquivo")
    pasta = request.form.get("pasta")
    if not arquivo or not pasta or pasta not in PASTAS:
        return "Erro no envio.", 400
    os.makedirs(PASTAS[pasta], exist_ok=True)
    caminho = os.path.join(PASTAS[pasta], arquivo.filename)
    arquivo.save(caminho)
    log(f"Enviado: {arquivo.filename} para {pasta}")
    return "✅ Arquivo enviado com sucesso!"

@app.route("/semear", methods=["POST"])
def semear():
    pacote = request.files.get("pacote")
    if not pacote or not pacote.filename.endswith(".zip"):
        return "Somente .zip permitido.", 400
    caminho = os.path.join("temp_seed.zip")
    with open(caminho, "wb") as f:
        f.write(pacote.read())
    log(f"Semeadura recebida: {pacote.filename}")
    return "✅ Pacote recebido para semeadura simbólica."

@app.route("/ritualizar", methods=["POST"])
def ritualizar():
    comando = request.form.get("comando", "").lower()
    respostas = {
        "digivolua o auroramon": "🧬 Auroramon evoluiu para PrismaAuroramon.",
        "scripturemon, restaura o coração do digimundo": "❤️ Scripturemon restaurou a essência do mundo.",
        "ajamon, embala o mundo": "🌙 Ajamon colocou o Digimundo em sono simbólico."
    }
    resposta = respostas.get(comando, "🔮 Ritual reconhecido, mas não documentado.")
    log(f"Ritual executado: {comando}")
    return resposta

@app.route("/log")
def ver_log():
    if os.path.exists(LOG):
        with open(LOG, "r", encoding="utf-8") as f:
            return f"<pre>{f.read()}</pre>"
    return "Log ainda vazio."

def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

if __name__ == "__main__":
    print("🌆 Cidade Digimon iniciada. Acesse http://localhost:8080/")
    app.run(host="0.0.0.0", port=8080)
