from flask import Blueprint, render_template
import os
import time

painel_tora_viva_bp = Blueprint("painel_tora_viva", __name__)

@painel_tora_viva_bp.route("/tora_viva")
def tora_viva():
    blocos = []
    for root, dirs, files in os.walk("tora"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                modificado = time.ctime(os.path.getmtime(path))
                with open(path, "r") as fp:
                    conteudo = fp.read()
                blocos.append({
                    "nome": path,
                    "modificado": modificado,
                    "conteudo": conteudo
                })
    return render_template("painel_tora_viva.html", blocos=blocos)