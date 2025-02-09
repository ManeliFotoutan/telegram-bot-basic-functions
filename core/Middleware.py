import telebot
from telebot import apihelper
import os
from dotenv import load_dotenv
import json

load_dotenv()

# 🔹 فعال‌سازی Middleware قبل از مقداردهی bot
apihelper.ENABLE_MIDDLEWARE = True

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Handle /help and /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hiii, Here is Maneli's bot!")
    bot.send_message(message.chat.id, json.dumps(message.chat.__dict__, indent=4, ensure_ascii=False))

# Middleware function
def modify_message_handler(bot_instance, message):
    if "مانلی" or "maneli" in message.text:
        message.modified_text = message.text + '❤️'

bot.add_middleware_handler(modify_message_handler, update_types=['message'])

@bot.message_handler(func=lambda message: True)
def reply_modified(message):
    bot.reply_to(message, message.modified_text if hasattr(message, 'modified_text') else message.text)

print("Bot is starting...")
bot.infinity_polling()
