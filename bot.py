# bot.py - Pure Notification Bot with Mini App
import telebot

# Initialize bot
bot = telebot.TeleBot("8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA")
FRONTEND_URL = "https://congashop.netlify.app"

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

# Start the bot
if __name__ == '__main__':
    print("🤖 Notification Bot with Mini App started...")
    bot.polling()