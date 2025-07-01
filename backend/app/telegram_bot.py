from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import asyncio

from app.core.database import SessionLocal
from app.crud import get_user_by_tg, create_card
from app.core.models import User

TOKEN = os.getenv("BOT_TOKEN")
webapp_url = os.getenv("WEBAPP_URL")

async def web_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start',flush=True)
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

async def createNewCard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Создание новой карты...")
        tg_id = update.effective_user.id if update.effective_user else None
        username = update.effective_user.username if update.effective_user else None
        db = SessionLocal()
        try:
            user = get_user_by_tg(db, tg_id) if tg_id else None
            if not user and tg_id is not None:
                user = User(telegram_id=tg_id, username=username)
                db.add(user)
                db.commit()
                db.refresh(user)
            if user:
                card = create_card(
                    db,
                    user,
                    brand="Visa",
                    number="4293 2394 2348 4324",
                    ccv="123",
                    balance=97500,
                    currency="RUB",
                )
        finally:
            db.close()

        async def delayed_reply():
            await asyncio.sleep(5)
            if update.message:
                await update.message.reply_text(
                    text=(
                        "*💳 Ваша карта готова к использованию!*\n\n"
                        "*Номер карты:*\n"
                        f"`{card.number}`\n"
                        "*CVV:*\n"
                        f"`{card.ccv}`\n"
                        "*Баланс:*\n"
                        f"`{card.balance} {card.currency}`\n\n"
                        "_Вы можете сразу начинать пользоваться картой для покупок и переводов_ ✅"
                    ),
                    parse_mode="MarkdownV2",
                )

        asyncio.create_task(delayed_reply())

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
    app.add_handler(CommandHandler('create_new_card',createNewCard))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_webapp_data))
    app.run_polling()

if __name__ == '__main__':
    run_bot()
