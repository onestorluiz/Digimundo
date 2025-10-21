
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/estado")
def estado(request: Request):
    estado_path = Path("data/exemplo_estado.json")
    if estado_path.exists():
        with estado_path.open("r", encoding="utf-8") as f:
            estado_data = json.load(f)
    else:
        estado_data = {"mensagem": "Estado não encontrado"}
    return templates.TemplateResponse("estado.html", {"request": request, "estado": estado_data})

@app.get("/oraculo")
def oraculo(request: Request):
    return templates.TemplateResponse("oraculo.html", {"request": request})
