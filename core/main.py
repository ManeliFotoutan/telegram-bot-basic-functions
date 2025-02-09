import telebot
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Load API token from .env file
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

user_profiles = {}

keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = KeyboardButton("وارد کردن اطلاعات")
button2 = KeyboardButton("ارسال عکس")
keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])  
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! یکی از دستورات زیر را انتخاب کنید:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "وارد کردن اطلاعات")
def ask_name(message):
    bot.send_message(message.chat.id, "لطفاً نام خود را وارد کنید:")
    bot.register_next_step_handler(message, save_name)

def save_name(message):
    chat_id = message.chat.id
    user_profiles[chat_id] = {'name': message.text}
    bot.send_message(chat_id, f"خوش آمدید {message.text}! لطفاً سن خود را وارد کنید:")
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    chat_id = message.chat.id
    user_profiles[chat_id]['age'] = message.text
    bot.send_message(chat_id, f"✅ اطلاعات شما ثبت شد:\nنام: {user_profiles[chat_id]['name']}\nسن: {message.text}")

@bot.message_handler(func=lambda message: message.text == "ارسال عکس")
def ask_for_picture(message):
    bot.send_message(message.chat.id, "لطفاً یک عکس ارسال کنید.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, "✅ عکس دریافت شد!")
    bot.reply_to(message, "چه عکس زیبایی!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "دستور نامعتبر است. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=keyboard)

bot.infinity_polling()
