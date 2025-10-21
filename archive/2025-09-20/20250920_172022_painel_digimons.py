
from flask import Blueprint, request, render_template

painel_digimons_bp = Blueprint('painel_digimons', __name__)

@painel_digimons_bp.route('/digimons', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_digimons.py"
    return "Painel painel_digimons.py pronto."
