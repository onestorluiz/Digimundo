import requests

def buscar_obra_museu_chicago(termo):
    url = f"https://api.artic.edu/api/v1/artworks/search?q={termo}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro no museu"
