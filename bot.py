from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime, time
import pytz

# Your bot token
TOKEN = "8062248069:AAFeOBo-NxvTaINcZ-9poNvo-HqPMNffPx8"

# Log file (same folder as bot.py)
LOG_FILE = "ViewList.txt"

# --- Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command sets up daily job"""
    chat_id = update.effective_chat.id

    # schedule job at 12:30 UK time
    context.job_queue.run_daily(
        send_daily_message,
        time=time(hour=12, minute=30, tzinfo=pytz.timezone("Europe/London")),
        chat_id=chat_id,
        name=str(chat_id),
    )

    await update.message.reply_text("✅ Daily reminder scheduled for 12:30 UK time every day.")

async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    """Send the daily message with button"""
    chat_id = context.job.chat_id
    keyboard = [[InlineKeyboardButton("Click here", callback_data="join_waitlist")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="Click the button below to join the premium waitlist 👇",
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks and log them"""
    query = update.callback_query
    await query.answer()

    user = query.from_user.username or query.from_user.first_name
    timestamp = datetime.now(pytz.timezone("Europe/London")).strftime("%Y-%m-%d %H:%M:%S")

    # Save to ViewList.txt
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user} clicked at {timestamp}\n")

    # Confirm to user
    await query.message.reply_text(f"✅ @{user}, you’ve been added to the waitlist!")

# --- Main ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
