from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from scripturemon_core import resposta_scriptural  # Integração direta com núcleo simbiótico

TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"
ID_AUTORIZADO = 6626669082

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ID_AUTORIZADO:
        await update.message.reply_text("⚠️ Acesso não autorizado.")
        return
    await update.message.reply_text("✨ Scripturemon desperto. Guardião simbiótico ativo.")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ID_AUTORIZADO:
        await update.message.reply_text("⚠️ Acesso não autorizado.")
        return
    prompt = update.message.text
    resposta = resposta_scriptural(prompt)
    await update.message.reply_text(resposta)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()
