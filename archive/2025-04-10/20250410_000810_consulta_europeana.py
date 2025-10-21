import requests
import json

def buscar_europeana(termo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["europeana"]
    url = f"https://api.europeana.eu/record/v2/search.json?wskey={chave}&query={termo}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro Europeana"
