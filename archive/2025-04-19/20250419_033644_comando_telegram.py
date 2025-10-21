import json
import telebot

with open("config/config_telegram.json") as f:
    config = json.load(f)

bot = telebot.TeleBot(config["bot_token"])
bot.send_message(config["user_id"], "Teste de envio do Digimundo.")