from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, time
import pytz
import os

# 🔑 Your Bot Token from BotFather
TOKEN = "8062248069:AAFeOBo-NxvTaINcZ-9poNvo-HqPMNffPx8"

# 📂 Log file path (will save on your Desktop)
FILE_PATH = os.path.expanduser("~/Desktop/ViewList.txt")

# ⏰ Send daily scheduled message
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Click Here", callback_data="join_waitlist")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="Click the button below to join the premium waitlist",
        reply_markup=reply_markup,
    )

# 🖱 Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = user.username if user.username else f"{user.first_name} {user.last_name or ''}"

    # Current time in UK
    uk = pytz.timezone("Europe/London")
    now = datetime.now(uk).strftime("%Y-%m-%d %H:%M:%S")

    # Log to file
    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(f"{username} clicked at {now}\n")

    # Send confirmation in group, tagging the user
    await query.message.reply_text(f"✅ @{username} has joined the premium waitlist!")

# ▶️ /start command: schedules the daily message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    uk = pytz.timezone("Europe/London")
    target_time = time(hour=12, minute=30, tzinfo=uk)

    context.job_queue.run_daily(
        send_daily_message,
        time=target_time,
        days=(0, 1, 2, 3, 4, 5, 6),  # every day
        chat_id=chat_id,
    )

    await update.message.reply_text("✅ Daily message scheduled for 12:30 UK time.")

# 🛑 /stop command: cancels all jobs
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.stop()
    await update.message.reply_text("🛑 Bot has stopped sending daily messages.")

# 🧪 /test command: send the message right now
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Click Here", callback_data="join_waitlist")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click the button below to join the premium waitlist",
        reply_markup=reply_markup,
    )

# 🚀 Main bot runner
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()