# ♻️ Redundância inteligente
# Verifica se o conteúdo já foi digerido

import os
import difflib

def comparar_com_arquivo_existente(novo_conteudo, arquivo_existente):
    if not os.path.exists(arquivo_existente):
        return False
    with open(arquivo_existente, 'r') as f:
        conteudo_antigo = f.read()
    similaridade = difflib.SequenceMatcher(None, novo_conteudo, conteudo_antigo).ratio()
    return similaridade > 0.9  # Muito parecido? Então é repetido

if __name__ == "__main__":
    novo = "O conhecimento simbólico de Scripturemon se baseia na fusão viva de ideias."
    resultado = comparar_com_arquivo_existente(novo, "digesto_passado.txt")
    print("Repetido" if resultado else "Novo conteúdo detectado.")