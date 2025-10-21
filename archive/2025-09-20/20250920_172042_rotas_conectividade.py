from fastapi import APIRouter

router = APIRouter()

from digimons.linkmon.nucleo.acao_linkmon import verificar_links
@router.get('/linkmon/verificar_links')
def rota_verificar_links(): return verificar_links()

from digimons.routermon.nucleo.acao_routermon import verificar_rotas
@router.get('/routermon/verificar_rotas')
def rota_verificar_rotas(): return verificar_rotas()

from digimons.bridgemon.nucleo.acao_bridgemon import criar_pontes
@router.get('/bridgemon/criar_pontes')
def rota_criar_pontes(): return criar_pontes()

from digimons.htmlmon.nucleo.acao_htmlmon import revisar_paineis
@router.get('/htmlmon/revisar_paineis')
def rota_revisar_paineis(): return revisar_paineis()

from digimons.pulsemon.nucleo.acao_pulsemon import medir_fluxo
@router.get('/pulsemon/medir_fluxo')
def rota_medir_fluxo(): return medir_fluxo()

