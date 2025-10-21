
from flask import Blueprint, request, render_template

painel_sonhos_bp = Blueprint('painel_sonhos', __name__)

@painel_sonhos_bp.route('/sonhos', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_sonhos.py"
    return "Painel painel_sonhos.py pronto."
