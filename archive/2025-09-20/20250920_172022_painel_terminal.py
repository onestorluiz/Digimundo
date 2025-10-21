
from flask import Blueprint, request, render_template

painel_terminal_bp = Blueprint('painel_terminal', __name__)

@painel_terminal_bp.route('/terminal', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_terminal.py"
    return "Painel painel_terminal.py pronto."
