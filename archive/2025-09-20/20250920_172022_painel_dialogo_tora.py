from flask import Blueprint, render_template, request
import os

painel_dialogo_tora_bp = Blueprint("painel_dialogo_tora", __name__)

@painel_dialogo_tora_bp.route("/dialogo_tora", methods=["GET", "POST"])
def dialogar():
    resposta = ""
    blocos = []
    for root, dirs, files in os.walk("tora"):
        for f in files:
            if f.endswith(".py"):
                blocos.append(os.path.join(root, f))
    if request.method == "POST":
        bloco = request.form.get("bloco")
        pergunta = request.form.get("pergunta")
        resposta = gerar_resposta(bloco, pergunta)
    return render_template("painel_dialogo.html", blocos=blocos, resposta=resposta)

def gerar_resposta(caminho, pergunta):
    try:
        with open(caminho, "r") as f:
            conteudo = f.read()
        if "#@ritual" in conteudo or "#@invocacao" in conteudo:
            return f"✨ Este é um bloco ritual. Ele responde com silêncio profundo: '{pergunta}' será refletido em ti mesmo."
        elif "def " in conteudo:
            return f"🌀 Este bloco tem funções. Talvez uma delas saiba: '{pergunta}'"
        else:
            return "🌑 Este bloco permanece em silêncio. Não sonhou ainda."
    except:
        return "Erro ao interpretar o sonho do bloco."