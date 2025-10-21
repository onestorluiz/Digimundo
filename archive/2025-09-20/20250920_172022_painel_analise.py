
from flask import Blueprint, request, render_template

painel_analise_bp = Blueprint('painel_analise', __name__)

@painel_analise_bp.route('/analise', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_analise.py"
    return "Painel painel_analise.py pronto."
