from flask import Blueprint
import os

painel_autonomia_bp = Blueprint("painel_autonomia", __name__)

@painel_autonomia_bp.route("/autonomia")
def autonomia():
    arquivos = os.listdir("controllers")
    rotas = [f for f in arquivos if f.endswith(".py")]
    return "Autonomia ativa. Módulos identificados: " + ", ".join(rotas)