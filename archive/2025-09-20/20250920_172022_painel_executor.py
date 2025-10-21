
from flask import Blueprint, request, render_template

painel_executor_bp = Blueprint('painel_executor', __name__)

@painel_executor_bp.route('/executor', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_executor.py"
    return "Painel painel_executor.py pronto."
