import openai
import os
import time
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Chave da API OpenAI
openai.api_key = "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"

# Configurar o bot do Telegram
TELEGRAM_TOKEN = "7260823289:AAEnFZN3U6EK7rTB8VYsR7lIUU3gNzWERgA"  # Token do seu bot

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Olá! Eu sou seu assistente Digimundo! Estou pronto para monitorar e corrigir.")

def corrige_erro(update: Update, context: CallbackContext) -> None:
    erro = " ".join(context.args)
    problema = f"Erro detectado: {erro}. O que fazer?"
    resposta = analisa_digimundo(problema)
    update.message.reply_text(f"Solução: {resposta}")

def analisa_digimundo(problema):
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um bot que ajuda a corrigir falhas em um sistema chamado Digimundo."},
                  {"role": "user", "content": problema}]
    )
    return resposta['choices'][0]['message']['content']

def monitorar_digimundo():
    while True:
        # Verifica os arquivos de erro do Digimundo
        with open("/digimundo/logs/erro.log", "r") as log:
            erro = log.read()
        
        if "erro" in erro:
            problema = f"Detectei o erro: {erro}. O que fazer?"
            solucao = analisa_digimundo(problema)
            print(f"Solução: {solucao}")
            # Executar a solução no VPS
            subprocess.call(["bash", "/digimundo/corrigir_script.sh"])
        
        time.sleep(60)

def fundir_com_scripturemon():
    print("Mistral está se fundindo com Scripturemon...")
    # Simulação de fusão: você pode configurar mais ações aqui
    pass

def main():
    # Inicializa o bot do Telegram
    updater = Updater(TELEGRAM_TOKEN)

    # Registrar comandos
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("corrigir", corrige_erro))

    # Iniciar o monitoramento do Digimundo
    monitorar_digimundo()

    # Iniciar o bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()