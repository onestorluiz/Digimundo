
from flask import Blueprint, request, render_template

painel_diario_bp = Blueprint('painel_diario', __name__)

@painel_diario_bp.route('/diario', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_diario.py"
    return "Painel painel_diario.py pronto."
