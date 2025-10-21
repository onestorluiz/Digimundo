
import os
import importlib.util
import json
from datetime import datetime

CAMINHO_CHAVES = "/root/templooculto/scripturemon/scripturemon_consciente_vivo_com_decisor/nucleo_conhecimento/chaves_api.py"

if not os.path.exists(CAMINHO_CHAVES):
    print("❌ Arquivo chaves_api.py não encontrado.")
    exit()

spec = importlib.util.spec_from_file_location("chaves_api", CAMINHO_CHAVES)
chaves_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chaves_api)

# Corrigido: agora busca CHAVES_API
chaves = getattr(chaves_api, "CHAVES_API", {})

def testar_conexao(api, chave):
    try:
        if not chave or chave == "":
            return "🔒 Sem chave"
        if api.lower() == "openai":
            import openai
            openai.api_key = chave
            _ = openai.Model.list()
            return "✅ OK"
        elif api.lower() == "huggingface":
            import requests
            response = requests.get("https://huggingface.co/api/models", headers={"Authorization": f"Bearer {chave}"})
            return "✅ OK" if response.status_code == 200 else f"⚠️ {response.status_code}"
        elif api.lower() == "serpapi":
            import requests
            response = requests.get(f"https://serpapi.com/search", params={"q": "test", "api_key": chave})
            return "✅ OK" if response.status_code == 200 else f"⚠️ {response.status_code}"
        else:
            return "❓ API desconhecida (não testada diretamente)"
    except Exception as e:
        return f"💥 Erro: {str(e)}"

relatorio = {}
for api, chave in chaves.items():
    resultado = testar_conexao(api, chave)
    relatorio[api] = resultado

saida = "/root/templooculto/scripturemon/scripturemon_consciente_vivo_com_decisor/nucleo_conhecimento/relatorio_conexoes.json"
with open(saida, "w") as f:
    json.dump({
        "data": str(datetime.now()),
        "relatorio": relatorio
    }, f, indent=2)

print("📡 RELATÓRIO DE CONEXÕES:")
for api, status in relatorio.items():
    print(f"🔗 {api}: {status}")
