import requests

def buscar_duckduckgo(termo):
    url = f"https://api.duckduckgo.com/?q={termo}&format=json"
    r = requests.get(url)
    return r.json().get("Abstract", "Nada encontrado") if r.status_code == 200 else "Erro na busca DuckDuckGo"
