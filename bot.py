from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8899733758:AAGgZXAubFb34AOyAms9AWpRD-mK23ShB_U"

# YOUR VIDEO FILE IDs
VIDEO1 = "BAACAgUAAxkBAAMFahWDA2mcxJTDM4kyIc-qx3-TkBgAAq4dAAIcXrBUU1zo-1hZfPg7BA"
VIDEO2 = "BAACAgUAAxkBAAMMahWEWc3CDeiCiyEivNdHuq0WnXcAAo8dAAIcXrBUDBNgSehFDY07BA"
VIDEO3 = "BAACAgUAAxkBAAMOahWFGGr4ZJnxxvMktPSauLdOri4AAtoeAAKWBRlU5ig23MTnFwABOwQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("🎬 Watch Demo", callback_data="demo")]
    ]

    await update.message.reply_text(
        "Welcome Here\nClick below for demo 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton("📞 Contact For Access", url="https://t.me/Johnynu@Johny_Demo_bot")]
    ]

    # VIDEO 1
    await query.message.reply_video(
        video=VIDEO1,
        caption="Demo Video 1",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    # VIDEO 2
    await query.message.reply_video(
        video=VIDEO2,
        caption="Demo Video 2",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    # VIDEO 3
    await query.message.reply_video(
        video=VIDEO3,
        caption="Demo Video 3",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()