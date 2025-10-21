from fastapi import APIRouter
from digimons.cannesdramon.reservador import reservar
from digimons.obscuramon.sombra import escavar

router = APIRouter()

@router.get('/cannesdramon/reservar')
def rota_cannes():
    return reservar()

@router.get('/obscuramon/escavar')
def rota_obscura():
    return escavar()
