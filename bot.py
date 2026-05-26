import json
import os
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8899733758:AAEwDKgrFLNDwy9UcypFyTnSSj4wjnYclDY"
ADMIN_ID = 8009821901

CONTACT_LINK = "https://t.me/Johnynu"
DELETE_AFTER_SECONDS = 300

VIDEO1 = "BAACAgUAAxkBAAMFahWDA2mcxJTDM4kyIc-qx3-TkBgAAq4dAAIcXrBUU1zo-1hZfPg7BA"
VIDEO2 = "BAACAgUAAxkBAAMMahWEWc3CDeiCiyEivNdHuq0WnXcAAo8dAAIcXrBUDBNgSehFDY07BA"
VIDEO3 = "BAACAgUAAxkBAAMOahWFGGr4ZJnxxvMktPSauLdOri4AAtoeAAKWBRlU5ig23MTnFwABOwQ"
VIDEO4 = "BAACAgUAAxkBAAMCahWlqvLoHmUix054Lpi6GCXw9KEAArUgAAK7hmlXsufTu7J8BC87BA"
VIDEO5 = "BAACAgUAAxkBAAMDahWlqhQAAfSNOA983P7MjTcZJHvAAAK-IAACu4ZpV_Xiz9epwtfBOwQ"
VIDEO6 = "BAACAgUAAxkBAAMEahWlqtnpknAG6t0zbd2UBSouerIAAsMgAAK7hmlXzjamziU5Q_Y7BA"
VIDEO7 = "BAACAgUAAxkBAAMFahWlqsJ7qfpbWKqOdVuk7hY02z4AAsQgAAK7hmlXYqDrQReJ9fw7BA"
VIDEO8 = "BAACAgUAAxkBAAMGahWlqtQkc-lFKdjdRo6cgOjHpOwAAsYgAAK7hmlXSq2moK6AJs47BA"
VIDEO9 = "BAACAgUAAxkBAAMHahWlqgbxcBhmo4wmY3x4Qp1SMnQAAskgAAK7hmlX6lyg-e1ushA7BA"

DATA_FILE = "users.json"


def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)


async def delete_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id, message_id = context.job.data
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print("Delete error:", e)


async def followup(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Hi 👋\n\nDid you watch the demo videos?\n\nContact here:\n{CONTACT_LINK}"
        )
    except Exception as e:
        print("Followup error:", e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    users = load_users()
    user_id = str(user.id)

    if user_id not in users:
        users[user_id] = {
            "name": user.first_name,
            "username": user.username,
            "joined": datetime.now().isoformat()
        }
        save_users(users)

        context.job_queue.run_once(
            followup,
            when=timedelta(days=2),
            data=user.id
        )

    keyboard = [
        [InlineKeyboardButton("🎬 Watch Demo", callback_data="demo")]
    ]

    await update.message.reply_text(
        "Welcome Here 👋\n\nClick below for demo videos 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "demo":
        buttons = [
            [InlineKeyboardButton("📞 Contact For Access", url=CONTACT_LINK)]
        ]

        videos = [VIDEO1, VIDEO2, VIDEO3, VIDEO4, VIDEO5, VIDEO6, VIDEO7, VIDEO8, VIDEO9]

        for index, video in enumerate(videos, start=1):
            msg = await query.message.reply_video(
                video=video,
                caption=f"Demo Video {index}\n\n⏳ Auto delete in 5 minutes.",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

            context.job_queue.run_once(
                delete_message,
                when=DELETE_AFTER_SECONDS,
                data=(msg.chat_id, msg.message_id)
            )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    users = load_users()
    await update.message.reply_text(f"📊 Total Users: {len(users)}")


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Telegram ID:\n\n{update.message.from_user.id}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage:\n/broadcast Your message")
        return

    message = " ".join(context.args)
    users = load_users()

    success = 0
    failed = 0

    for user_id in users.keys():
        try:
            await context.bot.send_message(chat_id=int(user_id), text=message)
            success += 1
        except:
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast Complete\n\nSuccess: {success}\nFailed: {failed}"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()
