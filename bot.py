# bot.py - Telegram Bot with HTTP Server for Render
import telebot
from flask import Flask, request
import threading

# Initialize bot
bot = telebot.TeleBot("8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA")
FRONTEND_URL = "https://congashop.netlify.app"
CHANNEL_URL = "https://t.me/your_channel_username"  # Replace with your actual channel link

# Create a simple Flask app for port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

@app.route('/health')
def health():
    return "✅ Healthy"

# Start command - shows Mini App button and channel join button
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
✨ *Welcome to Diamond Shop!* ✨

💎 *Premium Mobile Legends Diamonds*
⚡ *Instant Delivery*
🎯 *Best Prices in Myanmar*

Click below to open our shop or join our channel for updates and promotions!
    """
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=markup
    )

# Handle any other messages - also show Mini App button and channel join button
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
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

def run_bot():
    print("🤖 Starting Telegram Bot...")
    bot.polling()

def run_web():
    print("🌐 Starting HTTP Server...")
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Start web server in main thread (for port binding)
    run_web()