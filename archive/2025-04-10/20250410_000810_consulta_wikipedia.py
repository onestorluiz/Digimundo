import requests

def buscar_wikipedia(termo):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{termo}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json().get('extract', 'Nada encontrado.')
    else:
        return 'Erro ao buscar na Wikipedia.'
