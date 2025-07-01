from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler
import os
import asyncio
import random
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

# Этапы диалога
CHOOSE_BRAND, CHOOSE_CURRENCY = range(2)

brands = ["Visa", "MasterCard", "Mir"]
currencies = ["RUB", "USD", "EUR"]

user_params = {}

async def start_card_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[b] for b in brands]
    await update.message.reply_text(
        "Выберите тип карты:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return CHOOSE_BRAND

async def choose_brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    brand = update.message.text
    if brand not in brands:
        await update.message.reply_text("Пожалуйста, выберите из списка.")
        return CHOOSE_BRAND

    context.user_data['brand'] = brand

    keyboard = [[c] for c in currencies]
    await update.message.reply_text(
        "Теперь выберите валюту:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return CHOOSE_CURRENCY

async def create_new_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currency = update.message.text
    if currency not in currencies:
        await update.message.reply_text("Пожалуйста, выберите из списка.")
        return CHOOSE_CURRENCY

    brand = context.user_data['brand']

    def generate_card_number():
        digits = [str(random.randint(0, 9)) for _ in range(16)]
        return ' '.join(''.join(digits[i:i+4]) for i in range(0, 16, 4))

    def generate_cvv():
        return f"{random.randint(100, 999)}"

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
                brand=brand,
                number=generate_card_number(),
                ccv=generate_cvv(),
                balance=random.randint(10000, 150000),
                currency=currency,
            )
    finally:
        db.close()

    async def delayed_reply():
        await asyncio.sleep(5)
        if update.message:
            await update.message.reply_text(
                text=(
                    "*💳 Ваша карта готова к использованию\\!*\n\n"
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
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Создание карты отменено.")
    return ConversationHandler.END


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
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("create_new_card", start_card_dialog)],
        states={
            CHOOSE_BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_brand)],
            CHOOSE_CURRENCY: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_new_card)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("app", web_app))
    app.add_handler(CommandHandler('balance',balance))
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_webapp_data))
    app.run_polling()

if __name__ == '__main__':
    run_bot()
