
import sys
import os
from googletrans import Translator
from deep_translator import GoogleTranslator

def traduzir_linha(linha, modo='googletrans'):
    try:
        if modo == 'googletrans':
            return Translator().translate(linha, dest='pt').text
        else:
            return GoogleTranslator(source='auto', target='pt').translate(linha)
    except Exception:
        if modo == 'googletrans':
            return traduzir_linha(linha, modo='deep')
        return "[ERRO] " + linha

def traduzir_arquivo(arquivo_entrada):
    base, ext = os.path.splitext(arquivo_entrada)
    arquivo_saida = f"{base}_translated{ext}"

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    print(f"📘 Traduzindo {len(linhas)} linhas...")
    traduzidas = [traduzir_linha(linha.strip()) + "\n" for linha in linhas]

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.writelines(traduzidas)

    print(f"✅ Tradução salva em {arquivo_saida}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Uso: python traductormon.py <arquivo.txt|.srt|.html>")
    else:
        traduzir_arquivo(sys.argv[1])
