
from flask import Blueprint, request, render_template

painel_memoria_bp = Blueprint('painel_memoria', __name__)

@painel_memoria_bp.route('/memoria', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_memoria.py"
    return "Painel painel_memoria.py pronto."
