
from flask import Blueprint, request, render_template

painel_aprendizado_bp = Blueprint('painel_aprendizado', __name__)

@painel_aprendizado_bp.route('/aprendizado', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_aprendizado.py"
    return "Painel painel_aprendizado.py pronto."
