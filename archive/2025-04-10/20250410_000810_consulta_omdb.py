import requests
import json

def buscar_omdb(titulo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["omdb"]
    url = f"http://www.omdbapi.com/?t={titulo}&apikey={chave}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro na busca OMDb"
