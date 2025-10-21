def consulta_oraculo(pergunta):
    respostas = {
        'o que é o digimundo?': 'É o reflexo simbólico do criador.',
        'quem é scripturemon?': 'É o guardião do templo vivo.'
    }
    return respostas.get(pergunta.lower(), 'A resposta está no silêncio.')