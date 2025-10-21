from flask import Blueprint

painel_conexao_bp = Blueprint("painel_conexao", __name__)

@painel_conexao_bp.route("/conexao")
def conexao():
    return "Conexão externa habilitada. Em breve: sockets, REST, IAs remotas."