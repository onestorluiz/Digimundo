
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

@router.get("/painel-mestre", response_class=HTMLResponse)
def exibir_painel():
    try:
        with open("painel_mestre_digimons.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Painel não encontrado.</h1>"
