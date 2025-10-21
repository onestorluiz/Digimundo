from flask import Blueprint, render_template
import os
import json

painel_sonhador_bp = Blueprint("painel_sonhador", __name__)

@painel_sonhador_bp.route("/tora_sonhos")
def tora_sonhos():
    sonhos = []
    if os.path.exists("sonhos.json"):
        with open("sonhos.json", "r") as f:
            sonhos = json.load(f)
    return render_template("mapa_sonho.html", sonhos=sonhos)