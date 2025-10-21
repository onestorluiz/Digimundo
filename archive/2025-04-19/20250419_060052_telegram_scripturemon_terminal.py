from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from scripturemon_terminal import interpretar_ordem

TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    interpretar_ordem(texto)
    await update.message.reply_text(f"Scripturemon recebeu: “{texto}”")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

