from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Hardcoded bot token
BOT_TOKEN = "8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA"

# Your Netlify frontend
WEB_APP_URL = "https://congashop.netlify.app/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = InlineKeyboardButton(
        text="Open Mini App",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )
    markup = InlineKeyboardMarkup([[button]])
    await update.message.reply_text(
        "Click below to open the mini app:",
        reply_markup=markup
    )

if __name__ == "__main__":
    print("Starting Telegram bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
