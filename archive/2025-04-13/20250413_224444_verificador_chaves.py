
from chaves_api import CHAVES_API

def verificar_chaves():
    for chave, valor in CHAVES_API.items():
        if isinstance(valor, str) and ("SUA_CHAVE" in valor or "SEU_TOKEN" in valor):
            print(f"⚠️ Chave não preenchida: {chave}")
        else:
            print(f"✅ Chave ativa: {chave}")

if __name__ == "__main__":
    verificar_chaves()
