
from flask import Blueprint, request, render_template

painel_ias_bp = Blueprint('painel_ias', __name__)

@painel_ias_bp.route('/ias', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_ias.py"
    return "Painel painel_ias.py pronto."
