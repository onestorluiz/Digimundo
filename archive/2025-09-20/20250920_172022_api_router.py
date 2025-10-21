# Código exemplo de roteador FastAPI para rotas de digimons
from fastapi import APIRouter
router = APIRouter()

# Exemplo de rota
@router.get('/remanemon')
def get_remanemon(): return {'digimon': 'remanemon'}