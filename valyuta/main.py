import requests
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)


# >>> Valyuta olish funksiyasi
def get_currency(ccy=None):
    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

    try:
        data = requests.get(url, timeout=5).json()
    except:
        return "⚠️ Xatolik! Valyuta serveri ishlamayapti."

    if ccy:  # bitta valyutani olish
        for item in data:
            if item["Ccy"] == ccy:
                return f"💱 {ccy}: {item['Rate']} so'm"
        return "❌ Bunday valyuta topilmadi."

    # Barcha kerakli valyutalar
    need = ['USD', 'EUR', 'RUB', 'GBP', 'KZT']
    rates = {}

    for item in data:
        if item["Ccy"] in need:
            rates[item["Ccy"]] = item["Rate"]

    text = "💰 Valyuta kurslari (CBU):\n\n"
    for c in need:
        text += f"1 {c} = {rates[c]} so'm\n"

    return text


# >>> START komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        ["💵 Valyuta kursi", "📋 Valyutalar ro‘yxati"],
        ["⏰ Hozirgi vaqt", "❓ Yordam"]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Assalomu alaykum! Kerakli bo‘limni tanlang 👇",
        reply_markup=keyboard
    )


# >>> Asosiy tugmalar ishlovchisi
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💵 Valyuta kursi":
        await update.message.reply_text("⏳ Olinmoqda...")
        await update.message.reply_text(get_currency())

    elif text == "📋 Valyutalar ro‘yxati":
        inline = InlineKeyboardMarkup([
            [InlineKeyboardButton("USD", callback_data="USD"),
             InlineKeyboardButton("EUR", callback_data="EUR")],
            [InlineKeyboardButton("RUB", callback_data="RUB"),
             InlineKeyboardButton("GBP", callback_data="GBP")],
            [InlineKeyboardButton("KZT", callback_data="KZT")]
        ])
        await update.message.reply_text("Valyutani tanlang 👇", reply_markup=inline)

    elif text == "⏰ Hozirgi vaqt":
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        await update.message.reply_text(f"⏰ Hozirgi vaqt: {now}")

    elif text == "❓ Yordam":
        await update.message.reply_text(
            "📌 Men nima qila olaman?\n\n"
            "💵 Valyuta kursini ko‘rsatish\n"
            "📋 Valyutani alohida olish\n"
            "⏰ Hozirgi vaqtni chiqarish\n"
        )

    else:
        await update.message.reply_text("Noma'lum buyruq ❗")


# >>> Inline tugmalar (valyuta tanlash)
async def inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    currency = get_currency(query.data)
    await query.message.reply_text(currency)


# >>> TOKEN
TOKEN = "8543115664:AAETomYbHw1FmpJwUOyfKJ673tuYdAms7h4"

app = ApplicationBuilder().token(TOKEN).build()

# Handlerlar
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, message_handler))
app.add_handler(CallbackQueryHandler(inline_handler))

print("Bot ishga tushdi...")
app.run_polling()
