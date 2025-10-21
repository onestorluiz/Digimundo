from flask import Blueprint, request, jsonify

api_chat_bp = Blueprint("api_chat", __name__)

@api_chat_bp.route("/api/chat/<digimon>", methods=["POST"])
def chat(digimon):
    entrada = request.json.get("mensagem")
    resposta = f"{digimon} diz: Recebi sua mensagem — '{entrada}'"
    return jsonify({ "resposta": resposta })