
from flask import Blueprint, request, render_template

painel_auth_bp = Blueprint('painel_auth', __name__)

@painel_auth_bp.route('/auth', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_auth.py"
    return "Painel painel_auth.py pronto."
