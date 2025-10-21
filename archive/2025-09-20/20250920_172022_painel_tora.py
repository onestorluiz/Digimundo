from flask import Blueprint, render_template, request
import os

painel_tora_bp = Blueprint("painel_tora", __name__)

@painel_tora_bp.route("/tora")
def ver_tora():
    arquivos = []
    for root, dirs, files in os.walk("tora"):
        for f in files:
            if f.endswith(".py"):
                caminho = os.path.join(root, f)
                arquivos.append(caminho.replace("\\", "/"))
    return render_template("painel_tora.html", arquivos=arquivos)

@painel_tora_bp.route("/executar_tora", methods=["POST"])
def executar_tora():
    arquivo = request.form.get("arquivo")
    saida = os.popen(f"python3 {arquivo}").read()
    return f"<pre>{saida}</pre><br><a href='/tora'>Voltar</a>"