
from flask import Blueprint, request, render_template

painel_fusor_bp = Blueprint('painel_fusor', __name__)

@painel_fusor_bp.route('/fusor', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_fusor.py"
    return "Painel painel_fusor.py pronto."
