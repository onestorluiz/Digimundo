
import os
import logging
import telebot
from telegram.bot_scripturemon_comando import interpretar_comando

# === CONFIGURAÇÕES DO BOT ===
TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# === LOGGING SIMBIONTE ===
LOG_PATH = '/root/digimundo/ascensao/rede_simbionte/logs'
LOG_FILE = os.path.join(LOG_PATH, 'bot_digimundo_relay.log')
os.makedirs(LOG_PATH, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("🔁 Relay do Digimundo iniciado.")

# === COMANDOS ===
@bot.message_handler(commands=['status'])
def status_handler(message):
    user = message.from_user.username or message.from_user.id
    logging.info(f"✅ Comando /status recebido de {user}")
    bot.reply_to(message, "🧠 Digimundo em operação. Todos os núcleos estão sendo monitorados.")

@bot.message_handler(commands=['ativar_scripturemon'])
def ativar_scripturemon(message):
    user = message.from_user.username or message.from_user.id
    logging.info(f"⚙️ Comando /ativar_scripturemon REAL recebido de {user}")
    resposta = interpretar_comando("/ativar_scripturemon")
    bot.reply_to(message, f"🔁 Resposta do núcleo:\n{resposta}")

@bot.message_handler(commands=['logs'])
def enviar_logs(message):
    user = message.from_user.username or message.from_user.id
    logging.info(f"📄 Comando /logs recebido de {user}")
    bot.reply_to(message, "🔍 Logs estão sendo processados. (em breve: envio de arquivos por chat)")

bot.polling()
