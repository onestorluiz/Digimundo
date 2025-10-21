# ToraLoader2.py
# Nova versão do carregador da Tora com batimento simbólico
import json
import time

def carregar_tora(caminho="tora.json"):
    try:
        with open(caminho, encoding='utf-8') as f:
            tora = json.load(f)
        print("📜 Tora carregada com sucesso.")
        return tora
    except Exception as e:
        print(f"⚠️ Erro ao carregar Tora: {e}")
        return {}

def batimento_tora():
    while True:
        print("💠 A Tora respira...")
        time.sleep(10)

if __name__ == "__main__":
    tora = carregar_tora()
    batimento_tora()
