from fastapi import APIRouter

router = APIRouter()

from digimons.verificamon.nucleo.acao_verificamon import verificar
@router.get('/verificamon/verificar')
def rota_verificar(): return verificar()

from digimons.revisamon.nucleo.acao_revisamon import inspecionar
@router.get('/revisamon/inspecionar')
def rota_inspecionar(): return inspecionar()

from digimons.updateon.nucleo.acao_updateon import atualizar
@router.get('/updateon/atualizar')
def rota_atualizar(): return atualizar()

from digimons.backupmon.nucleo.acao_backupmon import salvar
@router.get('/backupmon/salvar')
def rota_salvar(): return salvar()

from digimons.nexomon.nucleo.acao_nexomon import conectar
@router.get('/nexomon/conectar')
def rota_conectar(): return conectar()

