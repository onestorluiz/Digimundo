from flask import Blueprint, render_template, request
import os, re, json

transformador_tora_bp = Blueprint("transformador_tora", __name__)

@transformador_tora_bp.route("/transformar_tora", methods=["GET", "POST"])
def transformar_tora():
    transformacoes = []
    for root, dirs, files in os.walk("tora"):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r") as fp:
                    codigo = fp.read()
                if "#@ritual" in codigo or "#@invocacao" in codigo:
                    funcoes = re.findall(r'def (\w+)\(', codigo)
                    for func in funcoes:
                        rota = f"/{func}"
                        controller_path = f"controllers/{func}.py"
                        json_path = f"data/digimons/{func}.json"
                        transformacoes.append({
                            "funcao": func,
                            "arquivo": path,
                            "rota": rota,
                            "controller_path": controller_path,
                            "json_path": json_path
                        })
    if request.method == "POST":
        alvo = request.form.get("funcao")
        for t in transformacoes:
            if t["funcao"] == alvo:
                with open(t["controller_path"], "w") as f:
                    f.write(f"from flask import Blueprint\n{alvo}_bp = Blueprint('{alvo}', __name__)\n@{alvo}_bp.route('{t['rota']}')\ndef {alvo}():\n    return '✨Gerado pela Tora Viva: {alvo}'")
                with open(t["json_path"], "w") as f:
                    json.dump({"nome": alvo, "origem": "tora", "mensagem": f"Eu sou {alvo}, invocado do vento da criação."}, f)
        return "Transformado com sucesso. <a href='/transformar_tora'>Voltar</a>"
    return render_template("painel_transformar.html", blocos=transformacoes)