from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import threading
import uvicorn
import app

TOKEN = os.getenv("BOT_TOKEN")
webapp_url = os.getenv("WEBAPP_URL")

async def web_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not webapp_url:
       raise EnvironmentError("WEBAPP_URL required")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Открыть Кошелёк", web_app=WebAppInfo(url=webapp_url))]
    ])
    if(update.message != None):
      await update.message.reply_text("Нажми кнопку ниже 👇", reply_markup=keyboard)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
   if(update.message):
      await update.message.reply_text('Ваш баланс 1000 долларов')     

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.message and update.message.web_app_data:
    data = update.message.web_app_data.data
    await update.message.reply_text(f"Ты отправил из WebApp: {data}")
  else:
    if update.message:
      await update.message.reply_text("Нет данных из WebApp.")

def run_bot():
    if not TOKEN:
      raise EnvironmentError("BOT_TOKEN is required in environment variables")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("app", web_app))
    app.add_handler(CommandHandler('balance',balance))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_webapp_data))
    app.run_polling()
    print('running')

def run_server():
    uvicorn.run(app.app, port=8000)

if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    run_bot()
