import telebot
from telebot import apihelper
import os
from dotenv import load_dotenv
import json
from telebot import types

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

keyboard = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton("MaktabKhoneh", url="https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B3%D8%A7%D8%AE%D8%AA-%D8%B1%D8%A8%D8%A7%D8%AA-%D8%AA%D9%84%DA%AF%D8%B1%D8%A7%D9%85-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86-mk7147/%D9%81%D8%B5%D9%84-%D8%B3%D9%88%D9%85-%D8%B9%D9%85%D9%84%DA%A9%D8%B1%D8%AF-%D9%BE%D8%A7%DB%8C%D9%87-ch16019/%D9%88%DB%8C%D8%AF%DB%8C%D9%88-%D8%A8%D8%B1%D8%B1%D8%B3%DB%8C-inline-keyboard-button/")
button2 = types.InlineKeyboardButton(text="گزینه دیگر", callback_data="option1")
keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "option1":
        bot.answer_callback_query(call.id, "شما گزینه دیگر را انتخاب کردید.")

bot.infinity_polling()
