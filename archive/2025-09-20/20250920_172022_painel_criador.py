from flask import Blueprint, request
import os

painel_criador_bp = Blueprint("painel_criador", __name__)

@painel_criador_bp.route("/criar", methods=["POST"])
def criar():
    nome = request.form.get("nome")
    with open(f"controllers/{nome}.py", "w") as f:
        f.write(f"# Arquivo gerado automaticamente para IA: {nome}")
    return f"IA {nome} criada com sucesso."