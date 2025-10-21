import sys
import json
import requests

# Substitua esta URL se seu Mistral estiver em outro endpoint
MISTRAL_URL = "http://127.0.0.1:11434/api/generate"
OUTPUT_FILE = "/root/digimundo/scripturemon/terminal/ultima_resposta.txt"

# Pegando a pergunta via argumento
if len(sys.argv) < 2:
    resposta = "❌ Nenhuma entrada fornecida."
else:
    pergunta = sys.argv[1]

    payload = {
        "model": "mistral",
        "prompt": pergunta,
        "stream": False
    }

    try:
        r = requests.post(MISTRAL_URL, json=payload)
        r.raise_for_status()
        resposta = r.json().get("response", "⚠️ Mistral não retornou resposta.")
    except Exception as e:
        resposta = f"❌ Erro ao chamar o Mistral: {e}"

# Salvando a resposta
with open(OUTPUT_FILE, "w") as f:
    f.write(resposta)
