# bot.py - Telegram Bot with HTTP Server for Render
import telebot
from flask import Flask, request
import threading

# Initialize bot
bot = telebot.TeleBot("8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA")
FRONTEND_URL = "https://congashop.netlify.app"

# Create a simple Flask app for port binding
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running!"

@app.route('/health')
def health():
    return "✅ Healthy"

# Start command - shows Mini App button
@bot.message_handler(commands=['start'])
def show_mini_app_button(message):
    markup = telebot.types.InlineKeyboardMarkup()
    web_app_btn = telebot.types.InlineKeyboardButton(
        text="🎮 Open Diamond Shop", 
        web_app=telebot.types.WebAppInfo(url=FRONTEND_URL)
    )
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id,
        "Welcome to Diamond Shop! Click below to open:",
        reply_markup=markup
    )

# Handle any other messages - also show Mini App button
@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    markup = telebot.types.InlineKeyboardMarkup()
    web_app_btn = telebot.types.InlineKeyboardButton(
        text="🎮 Open Diamond Shop", 
        web_app=telebot.types.WebAppInfo(url=FRONTEND_URL)
    )
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id,
        "Click to open Diamond Shop:",
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