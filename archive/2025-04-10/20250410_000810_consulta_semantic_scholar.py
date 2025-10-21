import requests

def buscar_artigos_semantic(termo):
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={termo}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro na busca Semantic Scholar"
