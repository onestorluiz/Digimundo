
from flask import Blueprint, request, render_template

painel_espelho_bp = Blueprint('painel_espelho', __name__)

@painel_espelho_bp.route('/espelho', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_espelho.py"
    return "Painel painel_espelho.py pronto."
