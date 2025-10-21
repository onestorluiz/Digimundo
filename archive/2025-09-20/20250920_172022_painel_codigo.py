
from flask import Blueprint, request, render_template

painel_codigo_bp = Blueprint('painel_codigo', __name__)

@painel_codigo_bp.route('/codigo', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_codigo.py"
    return "Painel painel_codigo.py pronto."
