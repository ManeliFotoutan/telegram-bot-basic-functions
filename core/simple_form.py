import telebot
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

user_profiles = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "سلام! لطفاً نام خود را وارد کنید:")
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    chat_id = message.chat.id
    name = message.text
    user_profiles[chat_id] = {'name': name}
    bot.reply_to(message, f"خوش آمدید {name}! لطفاً سن خود را وارد کنید:")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    chat_id = message.chat.id
    age = message.text
    user_profiles[chat_id]['age'] = age
    bot.reply_to(message, f"اطلاعات شما ثبت شد:\nنام: {user_profiles[chat_id]['name']}\nسن: {age}")


bot.infinity_polling()