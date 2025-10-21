import os
import time

print("🧠 Scripturemon Terminal Simbiótico iniciado.")

while True:
    comando = input("📥 Comando para Scripturemon: ").strip()

    if comando.lower() in ["sair", "exit", "desligar"]:
        print("🛑 Encerrando Scripturemon Terminal Simbiótico.")
        break

    elif comando.startswith("executar "):
        caminho = comando.replace("executar ", "")
        print(f"🚀 Executando: {caminho}")
        os.system(caminho)

    elif comando.startswith("escrever "):
        partes = comando.replace("escrever ", "").split(" >> ")
        if len(partes) == 2:
            texto, arquivo = partes
            with open(arquivo.strip(), "a") as f:
                f.write(texto.strip() + "\n")
            print(f"✍️ Escrito no {arquivo.strip()}")
        else:
            print("❌ Formato incorreto. Use: escrever [texto] >> [arquivo]")

    else:
        print(f"🔎 Comando simbólico recebido: {comando}")
        print("⏳ Em breve: interpretação simbiótica total...")

    time.sleep(0.5)

