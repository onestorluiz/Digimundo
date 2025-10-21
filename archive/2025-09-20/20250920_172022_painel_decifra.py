from flask import Blueprint, render_template, request
import os

painel_decifra_bp = Blueprint("painel_decifra", __name__)

@painel_decifra_bp.route("/decifra_tora", methods=["GET", "POST"])
def decifra():
    interpretacao = ""
    if request.method == "POST":
        arquivo = request.form.get("arquivo")
        if arquivo and os.path.exists(arquivo):
            with open(arquivo, "r") as f:
                codigo = f.read()
            interpretacao = interpretar_simbologia(codigo)
    arquivos = []
    for root, dirs, files in os.walk("tora"):
        for f in files:
            if f.endswith(".py"):
                arquivos.append(os.path.join(root, f))
    return render_template("painel_decifra.html", arquivos=arquivos, interpretacao=interpretacao)

def interpretar_simbologia(codigo):
    linhas = codigo.split("\n")
    simbolos = []
    for linha in linhas:
        if "def " in linha:
            nome = linha.strip().split("def ")[1].split("(")[0]
            simbolos.append(f"🌀 Função ritual detectada: '{nome}' → símbolo de ação ou invocação.")
        elif "import " in linha:
            mod = linha.strip().split("import ")[1]
            simbolos.append(f"🌌 Invocação de sabedoria ancestral: módulo '{mod}'.")
        elif "=" in linha and "==" not in linha:
            var = linha.strip().split("=")[0].strip()
            simbolos.append(f"🔮 Criação de essência: variável '{var}'.")
    if not simbolos:
        return "Nenhum símbolo encontrado. Talvez contenha sabedoria implícita."
    return "\n".join(simbolos)