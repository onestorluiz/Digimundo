from flask import Blueprint
import os

painel_fluxo_bp = Blueprint("painel_fluxo", __name__)

@painel_fluxo_bp.route("/fluxo")
def fluxo():
    logs = os.listdir("logs")
    return "Analisando fluxo de ações. Logs disponíveis: " + ", ".join(logs)