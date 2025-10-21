import requests
import json

def buscar_imagem_unsplash(termo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["unsplash"]
    url = f"https://api.unsplash.com/search/photos?query={termo}&client_id={chave}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro na busca Unsplash"
