import telebot
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = KeyboardButton("دستور اول")
button2 = KeyboardButton("دستور دوم")
keyboard.add(button1, button2)

@bot.message_handler(commands=['/choice'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! یکی از دستورات زیر را انتخاب کنید:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text, reply_markup=keyboard)

bot.infinity_polling()
