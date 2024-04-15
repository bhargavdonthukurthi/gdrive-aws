from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler,ContextTypes

TOKEN: Final = '6371335193:AAFfG2jOgM6wwDGJLdrIGDqPzPFUKdEXuM8'
BOT_USERNAME: Final = '@praveenchija_bot'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Videos kavalentra niku")

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("ok")

if __name__ == '__main__':
    print("Starting bot")
    app = Application.builder().token(TOKEN).build()

  #
    app.add_handler(CommandHandler('list',list_command))
    print("")
    print("polling")
    app.run_polling()
