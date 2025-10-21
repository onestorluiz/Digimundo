# Estrutura inicial para integração com Notion
# Precisa de token e ID de database (adicionar manualmente depois)
import requests
import json

def adicionar_entrada_notion(titulo, conteudo):
    with open("scripturemon_conexoes_maximo/chaves_api.json") as f:
        chave = json.load(f)["notion"]
    headers = {
        "Authorization": f"Bearer {chave}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    url = "https://api.notion.com/v1/pages"
    data = {"parent": {"database_id": "SEU_DATABASE_ID"}, "properties": {
        "Name": {"title": [{"text": {"content": titulo}}]}
    }}
    r = requests.post(url, headers=headers, json=data)
    return "Criado" if r.status_code == 200 else r.text
