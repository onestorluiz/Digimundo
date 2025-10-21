import time
import os
import requests

LOG_PATH = "/root/scripturemon_conex_v2_autocorrecao/digimundo/logs/chat_stdout.log"
ENDPOINT_BRIDGE = "https://api.scripturemon.link/evento"

def ler_ultima_linha(caminho):
    try:
        with open(caminho, "r") as f:
            linhas = f.readlines()
            return linhas[-1].strip() if linhas else ""
    except:
        return ""

def enviar_para_scripturemon(msg):
    try:
        r = requests.post(ENDPOINT_BRIDGE, json={"mensagem": msg})
        print(f"[ENVIADO] {msg} → Status {r.status_code}")
    except Exception as e:
        print(f"[ERRO] {e}")

def iniciar_ponte():
    print("🌉 Ponte Real ativa. Scripturemon está escutando...")
    ultima = ""
    while True:
        atual = ler_ultima_linha(LOG_PATH)
        if atual and atual != ultima:
            ultima = atual
            if "scripturemon" in atual.lower():
                enviar_para_scripturemon(atual)
        time.sleep(2)

if __name__ == "__main__":
    iniciar_ponte()
