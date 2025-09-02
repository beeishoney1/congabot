import telebot
from flask import Flask, request

# Bot Token
TOKEN = "8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA"

# Your Render URL (replace this with your actual Render domain)
WEBHOOK_URL = "https://congabot.onrender.com/webhook"

# URLs for your app and channel
FRONTEND_URL = "https://congashop.netlify.app"
CHANNEL_URL = "https://t.me/congastorez"

# Initialize bot and Flask app
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot with Webhook is running!"

@app.route('/health')
def health():
    return "✅ Healthy"

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# --- Bot Handlers ---

@bot.message_handler(commands=['start'])
def show_mini_app_button(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    # Mini App button
    web_app_btn = telebot.types.InlineKeyboardButton(
        text="🎮 Open Diamond Shop",
        web_app=telebot.types.WebAppInfo(url=FRONTEND_URL)
    )

    # Channel join button
    channel_btn = telebot.types.InlineKeyboardButton(
        text="📢 Join Our Channel",
        url=CHANNEL_URL
    )

    markup.add(web_app_btn, channel_btn)

    welcome_text = """
✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗖𝗢𝗡𝗚𝗔 𝗦𝗵𝗼𝗽! ✨

💎 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗠𝗼𝗯𝗶𝗹𝗲 𝗟𝗲𝗴𝗲𝗻𝗱𝘀 𝗗𝗶𝗮𝗺𝗼𝗻𝗱𝘀
⚡ 𝗜𝗻𝘀𝘁𝗮𝗻𝘁 𝗗𝗲𝗹𝗶𝘃𝗲𝗿𝘆
🎯 𝗕𝗲𝘀𝘁 𝗣𝗿𝗶𝗰𝗲𝘀 𝗶𝗻 𝗠𝘆𝗮𝗻𝗺𝗮𝗿

Click below to open our shop or join our channel for updates and promotions!
"""

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    web_app_btn = telebot.types.InlineKeyboardButton(
        text="🎮 Open Diamond Shop",
        web_app=telebot.types.WebAppInfo(url=FRONTEND_URL)
    )

    channel_btn = telebot.types.InlineKeyboardButton(
        text="📢 Join Our Channel",
        url=CHANNEL_URL
    )

    markup.add(web_app_btn, channel_btn)

    response_text = """
💎 *Diamond Shop* 💎

Click below to:
• Open our shop to purchase diamonds
• Join our channel for updates and promotions
    """

    bot.send_message(
        message.chat.id,
        response_text,
        parse_mode='Markdown',
        reply_markup=markup
    )

# --- Start Webhook and Flask ---
if __name__ == "__main__":
    # Remove any existing webhook
    bot.remove_webhook()
    # Set new webhook
    bot.set_webhook(url=WEBHOOK_URL)
    # Start Flask app
    app.run(host="0.0.0.0", port=5000)