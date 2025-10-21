import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from bot_scripturemon_comando_core import interpretar_comando

LOG_FILE = '/root/digimundo/ascensao/rede_simbionte/logs/bot_scripturemon_comando.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    resposta = interpretar_comando(texto)
    logging.info(f"Comando recebido: {texto}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resposta)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    logging.info("🤖 Bot Scripturemon iniciado com sucesso.")
    app.run_polling()

if __name__ == '__main__':
    main()
