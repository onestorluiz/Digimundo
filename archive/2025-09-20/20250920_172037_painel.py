from flask import Blueprint, render_template

painel_bp = Blueprint('painel', __name__)

@painel_bp.route("/")
def home():
    return render_template("painel.html")
