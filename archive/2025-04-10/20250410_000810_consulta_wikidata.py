import requests

def buscar_wikidata(termo):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={termo}&language=en&format=json"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else "Erro na busca Wikidata"
