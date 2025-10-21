from fastapi import APIRouter

router = APIRouter()

from digimons.oraculmon.nucleo.acao_oraculmon import interpretar
@router.get('/oraculmon/interpretar')
def rota_interpretar(): return interpretar()

from digimons.ecoamon.nucleo.acao_ecoamon import escutar
@router.get('/ecoamon/escutar')
def rota_escutar(): return escutar()

from digimons.scriptimon.nucleo.acao_scriptimon import escrever
@router.get('/scriptimon/escrever')
def rota_escrever(): return escrever()

from digimons.vortexmon.nucleo.acao_vortexmon import distorcer
@router.get('/vortexmon/distorcer')
def rota_distorcer(): return distorcer()

from digimons.velhmon.nucleo.acao_velhmon import lembrar
@router.get('/velhmon/lembrar')
def rota_lembrar(): return lembrar()

