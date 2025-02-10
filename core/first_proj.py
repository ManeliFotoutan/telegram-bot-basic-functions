import telebot
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import random

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = KeyboardButton("ارتباط مستقیم با ما")
button2 = KeyboardButton("ثبت مشکل")
keyboard.add(button1, button2)

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "ارتباط مستقیم با ما")
def direct_contact(message):
    contact_text = (
        "برای ارتباط مستقیم با ما می‌توانید با شماره‌های پشتیبانی زیر تماس بگیرید:\n\n"
        "📞 0912xxxxxx\n"
        "☎️ 021xxxxxx"
    )
    
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton("📞 تماس با 0912xxxxxx", url="https://wa.me/98912xxxxxx")
    )
    
    bot.send_message(message.chat.id, contact_text, reply_markup=inline_keyboard)


@bot.message_handler(func=lambda message: message.text == "ثبت مشکل")
def report_issue(message):
    bot.send_message(message.chat.id, "لطفاً مشکل خود را وارد نمایید.")
    user_states[message.chat.id] = "awaiting_issue"

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == "awaiting_issue")
def receive_issue(message):
    ticket_id = random.randint(10000, 99999)  
    response_text = f"کارشناسان ما در اسرع وقت با شما تماس خواهند گرفت.\nشماره پیگیری تیکت: {ticket_id}"
    
    bot.send_message(message.chat.id, response_text)
    
    del user_states[message.chat.id]

bot.infinity_polling()