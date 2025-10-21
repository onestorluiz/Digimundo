
from flask import Blueprint, request, render_template

painel_ritual_bp = Blueprint('painel_ritual', __name__)

@painel_ritual_bp.route('/ritual', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_ritual.py"
    return "Painel painel_ritual.py pronto."
