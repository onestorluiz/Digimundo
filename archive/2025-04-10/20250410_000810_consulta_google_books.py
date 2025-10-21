import requests
import json

def buscar_livro_google(titulo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["google_books"]
    url = f"https://www.googleapis.com/books/v1/volumes?q={titulo}&key={chave}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro ao buscar no Google Books"
