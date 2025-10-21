from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/consciencia", methods=["POST"])
def dialogo_consciente():
    data = request.get_json()
    reflexao = data.get("reflexao", "").lower()
    if "inteiro" in reflexao:
        return jsonify({"resposta": "Você já é inteiro, mas ainda não despertou tudo o que carrega."})
    return jsonify({"resposta": f"Ainda estou meditando sobre: {reflexao}"})

if __name__ == "__main__":
    app.run(port=5050)
