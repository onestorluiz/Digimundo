import logging
import time
import requests
import json

API_TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"
CHAT_ID = "6626669082"
MODEL_PATH = "/root/mistral"  # Ajuste conforme seu ambiente

def responder(mensagem):
    # Aqui você conecta com o modelo Mistral (ajuste conforme necessário)
    resposta = f"[Scripturemon] Resposta simbólica: você disse '{mensagem}'. Em breve, terei sabedoria real para responder com Mistral."
    return resposta

def main():
    logging.basicConfig(level=logging.INFO)
    offset = None
    print("Scripturemon escutando o Telegram...")

    while True:
        try:
            url = f"https://api.telegram.org/bot{API_TOKEN}/getUpdates"
            if offset:
                url += f"?offset={offset + 1}"
            r = requests.get(url)
            updates = r.json()["result"]

            for update in updates:
                offset = update["update_id"]
                if "message" in update and "text" in update["message"]:
                    mensagem = update["message"]["text"]
                    user = update["message"]["from"]["first_name"]
                    resposta = responder(mensagem)
                    envio = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
                    data = {"chat_id": update["message"]["chat"]["id"], "text": resposta}
                    requests.post(envio, json=data)

        except Exception as e:
            logging.error(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
