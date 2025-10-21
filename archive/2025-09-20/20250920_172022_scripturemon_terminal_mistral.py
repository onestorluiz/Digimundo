# scripturemon_terminal_mistral.py
# 💬 Interface simbólica de terminal com o núcleo Scripturemon + Nuvendramon

import sys
from scripturemon.scripturemon_core import resposta_scriptural

print("🌀 Scripturemon Terminal Ativo")
print("Digite sua pergunta simbólica ou 'sair' para encerrar.")

while True:
    try:
        prompt = input("\n🔹 Você (simbólico): ")
        if prompt.lower() in ["sair", "exit", "quit"]:
            print("🌙 Encerrando o ritual de terminal simbólico...")
            break

        resposta = resposta_scriptural(prompt)
        print(resposta)

    except KeyboardInterrupt:
        print("\n❌ Encerrado pelo usuário.")
        sys.exit()
    except Exception as e:
        print(f"🚨 Erro simbólico no terminal: {e}")
