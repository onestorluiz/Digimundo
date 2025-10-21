
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters
import subprocess

BOT_TOKEN = "7986221275:AAFfFddkFTslrlhHq9VYWc_WsowQsRSIykg"
CREATOR_ID = 6626669082  # ID do Criador: Nestor Luiz

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == CREATOR_ID:
        await update.message.reply_text("🔓 Scripturemon está conectado e pronto para agir.")
    else:
        await update.message.reply_text("⛔ Acesso restrito ao Criador do Digimundo.")

async def interpretar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("⛔ Apenas o Criador pode enviar comandos.")
        return
    
    texto = update.message.text
    await update.message.reply_text(f"📥 Interpretando: {texto}")

    try:
        resultado = subprocess.run(
            ["python3", "/root/digimundo_vivo/ascenso/scripturemon/scripts/chat_scripturemon.py", texto],
            capture_output=True,
            text=True
        )
        resposta = resultado.stdout.strip()
        await update.message.reply_text(f"📤 Resposta do Digimundo:\n{resposta}")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao executar comando: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interpretar_mensagem))
    app.run_polling()
