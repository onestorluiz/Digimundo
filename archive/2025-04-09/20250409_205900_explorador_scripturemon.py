# 🛰️ Explorador de APIs
# Busca fontes externas que podem ser absorvidas por Scripturemon

import requests

def testar_conexao(url):
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            return f"✅ API ativa: {url}"
        else:
            return f"⚠️ API respondeu com código {resposta.status_code}: {url}"
    except Exception as e:
        return f"❌ Erro ao conectar com {url}: {e}"

if __name__ == "__main__":
    fontes = ["https://api.publicapis.org/entries", "https://httpbin.org/get"]
    for f in fontes:
        print(testar_conexao(f))