import requests
import json

def buscar_filme_tmdb(titulo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["tmdb"]
    url = f"https://api.themoviedb.org/3/search/movie?api_key={chave}&query={titulo}"
    r = requests.get(url)
    if r.status_code == 200 and r.json()["results"]:
        return r.json()["results"][0]
    else:
        return "Filme não encontrado."
