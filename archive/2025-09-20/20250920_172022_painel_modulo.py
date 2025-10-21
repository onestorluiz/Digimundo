
from flask import Blueprint, request, render_template

painel_modulo_bp = Blueprint('painel_modulo', __name__)

@painel_modulo_bp.route('/modulo', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_modulo.py"
    return "Painel painel_modulo.py pronto."
