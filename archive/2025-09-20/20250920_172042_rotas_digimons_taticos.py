from fastapi import APIRouter

router = APIRouter()

from digimons.firewallmon.acao_firewallmon import proteger
@router.get('/firewallmon/proteger')
def rota_proteger(): return proteger()

from digimons.metalfirewallmon.acao_metalfirewallmon import reforcar
@router.get('/metalfirewallmon/reforcar')
def rota_reforcar(): return reforcar()

from digimons.warfirewallmon.acao_warfirewallmon import atacar
@router.get('/warfirewallmon/atacar')
def rota_atacar(): return atacar()

from digimons.strategamon.acao_strategamon import organizar
@router.get('/strategamon/organizar')
def rota_organizar(): return organizar()

