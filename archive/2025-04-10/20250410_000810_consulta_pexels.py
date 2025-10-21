import requests
import json

def buscar_imagem_pexels(termo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["pexels"]
    url = f"https://api.pexels.com/v1/search?query={termo}"
    headers = {"Authorization": chave}
    r = requests.get(url, headers=headers)
    return r.json() if r.status_code == 200 else "Erro na busca Pexels"
