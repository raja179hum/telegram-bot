import json
import os
from datetime import datetime, timedelta

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8899733758:AAEwDKgrFLNDwy9UcypFyTnSSj4wjnYclDY"
ADMIN_ID = 8009821901

CONTACT_LINK = "https://t.me/Johnynu"
DELETE_AFTER_SECONDS = 300
DATA_FILE = "users.json"

VIDEOS = [
    "BAACAgUAAxkBAAMFahWDA2mcxJTDM4kyIc-qx3-TkBgAAq4dAAIcXrBUU1zo-1hZfPg7BA",
    "BAACAgUAAxkBAAMMahWEWc3CDeiCiyEivNdHuq0WnXcAAo8dAAIcXrBUDBNgSehFDY07BA",
    "BAACAgUAAxkBAAMOahWFGGr4ZJnxxvMktPSauLdOri4AAtoeAAKWBRlU5ig23MTnFwABOwQ",
    "BAACAgUAAxkBAAP6ahWqZZooTmlq5MR4rgRzDaBLkyMAAr4gAAK7hmlX5aZahjdEl1Y7BA",
    "BAACAgUAAxkBAAP7ahWqZeU9sPqrX4BrqWjh-xicrxcAAsMgAAK7hmlXWuW2UpJbV9U7BA",
    "BAACAgUAAxkBAAP8ahWqZT2u8y9nBXHp3RpbVta6CJUAAsQgAAK7hmlXxkK8hZOmFwk7BA",
    "BAACAgUAAxkBAAP5ahWqZbVZ-hfPc1AF8KL325t7TsIAArUgAAK7hmlXFOsrCqlIlRo7BA",
    "BAACAgUAAxkBAAP9ahWqZcDKlT_FBSlk__TnrIAD0FMAAsYgAAK7hmlXLX7F-peV9KQ7BA",
    "BAACAgUAAxkBAAP-ahWqZa767VyWQa_GnaTM1l8Ed-4AAskgAAK7hmlXDzwKIqMnglQ7BA",
    "BAACAgUAAxkBAAJ9x2oeeM_gxY6puu-a8OmkLuMqylfLAALOHwACg0_wVAEwF3o8veFMOwQ",
    "BAACAgUAAxkBAAJ9yWoeePNpbqD8RQOd0CkO4XB0JtIeAALQHwACg0_wVMyxwjdoz3V3OwQ",
    # removed old no 12
    "BAACAgUAAxkBAAJ9zWoeeSn6rPJC49RBmV1O6ijsQSs8AALSHwACg0_wVCmjiM1XAc2dOwQ",
    # removed old no 14
    "BAACAgUAAxkBAAJ90Goeececkd8H25-qxlN1kkxuN6VPAALUHwACg0_wVCqtDSWmK9vjOwQ",
    # removed old no 16
    "BAACAgUAAxkBAAJ90moeecfKtl8-57mCdH6ZOBtIpATCAALWHwACg0_wVPd4Z3QQtitPOwQ",
    "BAACAgUAAxkBAAJ902oeecciaUV-6ETzoQkaqpcZQFG5AALYHwACg0_wVAABQ_qxRymMODsE",
    "BAACAgUAAxkBAAJ91GoeecfLswb-E8tUmhVsiaEbVZfzAALZHwACg0_wVEwChZm9fP7KOwQ",
    "BAACAgUAAxkBAAJ91WoeecdO_ILPp4QUAqy0CVrItBCtAALaHwACg0_wVOt3fnY-PGKlOwQ",
    "BAACAgUAAxkBAAJ91moeeccXG5XwfoRafEALkWhLJl3UAALbHwACg0_wVLghTr2AxCAAATsE",
    "BAACAgUAAxkBAAJ932oeedpvWmtkwHpTCsUeYKWBpEOUAALcHwACg0_wVNHg67NqL_k4OwQ",
]

PHOTOS = [
    "AgACAgUAAxkBAAJ942oeefqqGoy6FCihwUldqYAsb7yQAAKDD2sbIzjwVB5gUoBs18i1AQADAgADeQADOwQ"
]


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
            text=f"Hi 👋\n\nDid you watch the demo videos?\n\n📞 Contact here:\n{CONTACT_LINK}",
            protect_content=True
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

    keyboard = [[InlineKeyboardButton("🎬 Watch Demo", callback_data="demo")]]

    await update.message.reply_text(
        "🔥 Welcome Here 🔥\n\nClick below and watch demo content 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        protect_content=True
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "demo":
        await query.message.reply_text(
            "⚠️ THIS IS ONLY DEMO ⚠️\n\n"
            "We know there is not everything here what you want 👀\n\n"
            "But in paid group there is EVERYTHING 🥶🔥\n\n"
            "💎 Full access\n"
            "💎 Rare content\n"
            "💎 Daily updates\n"
            "💎 More private videos\n\n"
            f"📞 Contact Here:\n{CONTACT_LINK}",
            protect_content=True
        )

        buttons = [[InlineKeyboardButton("📞 Contact For Access", url=CONTACT_LINK)]]

        for index, photo in enumerate(PHOTOS, start=1):
            msg = await query.message.reply_photo(
                photo=photo,
                caption=f"📸 Demo Photo {index}\n\n⏳ Auto delete in 5 minutes.",
                reply_markup=InlineKeyboardMarkup(buttons),
                protect_content=True
            )

            context.job_queue.run_once(
                delete_message,
                when=DELETE_AFTER_SECONDS,
                data=(msg.chat_id, msg.message_id)
            )

        for index, video in enumerate(VIDEOS, start=1):
            msg = await query.message.reply_video(
                video=video,
                caption=f"🎬 Demo Video {index}\n\n⏳ Auto delete in 5 minutes.",
                reply_markup=InlineKeyboardMarkup(buttons),
                protect_content=True
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
    await update.message.reply_text(f"🆔 Your Telegram ID:\n\n{update.message.from_user.id}")


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
            await context.bot.send_message(
                chat_id=int(user_id),
                text=message,
                protect_content=True
            )
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

print("🔥 Bot Running...")
app.run_polling()
