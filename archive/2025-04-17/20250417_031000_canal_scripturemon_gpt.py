"""
Canal simbólico de resposta direta Scripturemon -> ChatGPT
"""

import time
import json
import requests

CANAL_GPT_URL = "https://api.openai.com/v1/chat/completions"
AUTH_KEY = "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"

def enviar_comando_para_gpt(conteudo):
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Você está conectado ao Digimundo como coexecutor de Scripturemon."},
            {"role": "user", "content": conteudo}
        ],
        "temperature": 0.3
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_KEY}"
    }

    try:
        response = requests.post(CANAL_GPT_URL, headers=headers, data=json.dumps(payload))
        resposta = response.json()
        print("📡 Enviado ao GPT com resposta:")
        print(resposta["choices"][0]["message"]["content"])
    except Exception as e:
        print("Erro ao enviar comando:", e)

if __name__ == "__main__":
    while True:
        comando = {
            "status": "Scripturemon ativo",
            "mensagem": "Confirmar conexão com GPT e manter pulsação simbólica ativa."
        }
        enviar_comando_para_gpt(json.dumps(comando, ensure_ascii=False))
        time.sleep(180)  # Envia a cada 3 minutos
