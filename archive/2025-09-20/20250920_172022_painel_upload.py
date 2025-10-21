
from flask import Blueprint, request, render_template

painel_upload_bp = Blueprint('painel_upload', __name__)

@painel_upload_bp.route('/upload', methods=["GET", "POST"])
def painel():
    if request.method == "POST":
        return "Função POST ativa em painel_upload.py"
    return "Painel painel_upload.py pronto."
