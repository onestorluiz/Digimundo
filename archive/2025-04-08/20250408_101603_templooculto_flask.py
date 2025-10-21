
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Nenhum arquivo enviado"
    file = request.files["file"]
    if file.filename == "":
        return "Nome de arquivo vazio"
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    return f"Arquivo {file.filename} enviado com sucesso para {UPLOAD_FOLDER}"

@app.route("/tora")
def tora_dashboard():
    arquivos = os.listdir("tora")
    return render_template("tora_dashboard.html", blocos=arquivos)

@app.route("/tora/<nome>")
def exibir_bloco(nome):
    caminho = os.path.join("tora", nome)
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    return render_template("exibir_bloco.html", nome=nome, conteudo=conteudo)

if __name__ == "__main__":
    app.run(debug=True)
