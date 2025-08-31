# bot.py - Telegram Bot for Diamond Shop
import telebot
import requests
import json
from datetime import datetime

# Initialize bot
bot = telebot.TeleBot("8042603273:AAFZpfKNICr57kYBkexm1MmcJLU_2mTSRmA")
BACKEND_URL = "https://congabackend.onrender.com"

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🎮 <b>Welcome to Diamond Shop Bot!</b>

I can help you with:
• Buying diamonds for your games
• Checking your purchase history
• Getting order status updates

<b>Available Commands:</b>
/register - Create a new account
/login - Login to your account  
/buy - Buy diamonds
/history - View your purchase history
/help - Show all commands

Visit our website: https://congashop.netlify.app/
    """
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

# Help command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
🎮 <b>Diamond Shop Bot Commands</b>

/start - Start the bot
/help - Show this help message
/register - Register a new account
/login - Login to your account
/buy - Buy diamonds
/history - View purchase history

<b>For purchases:</b>
Visit our website: https://congashop.netlify.app/
to select games, servers, and diamond amounts.
    """
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

# Register command
@bot.message_handler(commands=['register'])
def register_user(message):
    try:
        # Extract username and password from message
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "📝 <b>Usage:</b> /register username password\n\nExample: /register john123 secretpass", parse_mode='HTML')
            return
        
        username, password = parts[1], parts[2]
        
        # Call backend API
        response = requests.post(f"{BACKEND_URL}/register", json={
            "username": username,
            "password": password,
            "telegram_id": message.chat.id
        })
        
        if response.status_code == 201:
            bot.reply_to(message, "✅ <b>Registration successful!</b>\n\nYou can now use /login to access your account", parse_mode='HTML')
        else:
            error = response.json().get('error', 'Unknown error')
            bot.reply_to(message, f"❌ <b>Registration failed:</b> {error}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode='HTML')

# Login command  
@bot.message_handler(commands=['login'])
def login_user(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "🔐 <b>Usage:</b> /login username password\n\nExample: /login john123 secretpass", parse_mode='HTML')
            return
        
        username, password = parts[1], parts[2]
        
        # Call backend API
        response = requests.post(f"{BACKEND_URL}/login", json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            user = data['user']
            bot.reply_to(message, f"✅ <b>Login successful!</b>\n\nWelcome back, {user['username']}!\n\nUser ID: {user['id']}\nTelegram ID: {user['telegram_id']}\nAdmin: {'Yes' if user['is_admin'] else 'No'}", parse_mode='HTML')
        else:
            error = response.json().get('error', 'Invalid credentials')
            bot.reply_to(message, f"❌ <b>Login failed:</b> {error}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode='HTML')

# Buy command - provides instructions
@bot.message_handler(commands=['buy'])
def buy_diamonds(message):
    instructions = """
🎮 <b>How to Buy Diamonds</b>

To purchase diamonds, please visit our website:

🌐 <b>Website:</b> https://congashop.netlify.app/

<b>Steps:</b>
1. Visit the website above
2. Login to your account
3. Select your game and server
4. Choose diamond amount
5. Enter your game ID
6. Upload payment slip
7. Submit your order

<b>Features:</b>
• Multiple games supported
• Competitive prices
• Secure payment processing
• Instant delivery

We'll notify you here when your order is processed!
    """
    bot.send_message(message.chat.id, instructions, parse_mode='HTML')

# History command
@bot.message_handler(commands=['history'])
def purchase_history(message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.reply_to(message, "📋 <b>Usage:</b> /history user_id\n\nExample: /history 123", parse_mode='HTML')
            return
        
        user_id = parts[1]
        
        # Call backend API
        response = requests.get(f"{BACKEND_URL}/purchase-history?user_id={user_id}")
        
        if response.status_code == 200:
            data = response.json()
            purchases = data['purchases']
            
            if not purchases:
                bot.reply_to(message, "📭 <b>No purchases found</b>\n\nYou haven't made any purchases yet.", parse_mode='HTML')
                return
            
            history_text = "📋 <b>Your Purchase History</b>\n\n"
            
            for purchase in purchases[:5]:  # Show last 5 purchases
                history_text += f"🎮 <b>Game:</b> {purchase['game_id']}\n"
                history_text += f"🌐 <b>Server:</b> {purchase['server_id']}\n"
                history_text += f"💎 <b>Diamonds:</b> {purchase['amount']}\n"
                history_text += f"📊 <b>Status:</b> {purchase['status']}\n"
                history_text += f"📅 <b>Date:</b> {purchase['created_at'][:10]}\n"
                history_text += "────────────────────\n"
            
            if len(purchases) > 5:
                history_text += f"\n📄 <i>Showing 5 of {len(purchases)} purchases</i>"
                history_text += f"\n🌐 <b>View all on:</b> https://congashop.netlify.app/history"
            
            bot.send_message(message.chat.id, history_text, parse_mode='HTML')
        else:
            error = response.json().get('error', 'Failed to fetch history')
            bot.reply_to(message, f"❌ <b>Error:</b> {error}", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode='HTML')

# Admin stats command
@bot.message_handler(commands=['admin_stats'])
def admin_stats(message):
    try:
        # This would require admin authentication in a real implementation
        # For now, we'll just show a message
        
        bot.reply_to(message, "👨‍💼 <b>Admin Statistics</b>\n\nAdmin features are available on our web dashboard:\n\n🌐 https://congashop.netlify.app/admin\n\n• View all purchases\n• Update order status\n• Manage diamond prices\n• Filter by users", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode='HTML')

# Handle any other text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "🤖 <b>Diamond Shop Bot</b>\n\nI can help you with diamond purchases!\n\nUse /help to see all available commands.", parse_mode='HTML')

# Start the bot
if __name__ == '__main__':
    print("🤖 Diamond Shop Telegram Bot started...")
    bot.polling()