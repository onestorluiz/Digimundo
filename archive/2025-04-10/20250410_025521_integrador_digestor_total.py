
from digestor_api import digerir_conhecimento

# Simulação de integração com múltiplas APIs
def processar_resultado_api(nome_api, conteudo):
    print(f"Processando conteúdo vindo da API: {nome_api}")
    resultado = digerir_conhecimento(nome_api, conteudo)
    if resultado == "aceito":
        print(">>> Conhecimento absorvido simbolicamente.")
    else:
        print(">>> Conteúdo ignorado por falta de valor simbólico.")

# Exemplo de uso com várias fontes
if __name__ == "__main__":
    respostas = [
        ("OMDb", "O filme trata da desconstrução da imagem e da subjetividade do tempo."),
        ("Wikidata", "A cebola é uma planta comestível."),
        ("Wikipedia", "A estética no cinema brasileiro frequentemente reflete traumas históricos."),
        ("Semantic Scholar", "Estudos indicam que a memória visual é fragmentada por natureza."),
        ("Museu de Chicago", "Obra simbolista evoca lembrança e ancestralidade.")
    ]

    for nome, conteudo in respostas:
        processar_resultado_api(nome, conteudo)
