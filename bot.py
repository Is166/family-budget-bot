import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if message.startswith('+'):
        await update.message.reply_text("✅ Доход записан: " + message[1:].strip())
    elif message.startswith('-'):
        await update.message.reply_text("💸 Расход записан: " + message[1:].strip())
    else:
        await update.message.reply_text("Напиши сумму с + или - чтобы учесть доход или расход.")

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
