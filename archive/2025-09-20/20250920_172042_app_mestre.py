
from fastapi import FastAPI
from rotas_visuais import router as visual_router

app = FastAPI(title="Painel Mestre Digimons")
app.include_router(visual_router)

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo ao Painel Mestre do Digimundo"}
