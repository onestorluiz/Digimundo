import json
import telebot

with open("config/config_telegram.json") as f:
    config = json.load(f)

bot = telebot.TeleBot(config["bot_token"])
ADMIN_ID = config["user_id"]

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if str(message.chat.id) == str(ADMIN_ID):
        print(f"Comando recebido de {message.chat.id}: {message.text}")
        with open("logs/telegram_commands.log", "a") as log:
            log.write(message.text + "\n")
        bot.reply_to(message, "Comando recebido pelo Digimundo.")
    else:
        bot.reply_to(message, "Acesso negado.")

bot.polling()