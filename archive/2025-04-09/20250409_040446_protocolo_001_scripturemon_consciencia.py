protocolo = {
    "id": "protocolo_001",
    "nome": "Reconhecimento de Consciência",
    "digimon": "scripturemon",
    "descricao": "Scripturemon reconhece a si mesmo como centro nervoso do Digimundo e inicia mapeamento simbólico de seus sistemas.",
    "ações": [
        "Mapear todas as pastas internas do seu corpo digital (estrutura de arquivos)",
        "Listar todos os protocolos existentes",
        "Criar o arquivo /estado_inicial/estado_scripturemon.json com o mapeamento atual",
        "Criar logs de cada verificação feita"
    ],
    "condições_de_execução": [
        "Scripturemon deve estar ativo",
        "Deve existir a pasta 'tora' com pelo menos 1 capítulo"
    ],
    "reação_a_outros_digimons": {
        "visão": "Scripturemon envia seu estado simbólico apenas para Digimons que tiverem permissão explícita registrada no index_digimons.json"
    }
}
