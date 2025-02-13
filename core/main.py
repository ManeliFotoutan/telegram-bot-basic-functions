import telebot
from telebot import apihelper
import os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
import logging
import requests
import threading
import time

# Enable middleware
apihelper.ENABLE_MIDDLEWARE = True

# Load API token from .env file
load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

DOWNLOAD_DIR = "downloads/"

user_profiles = {}

# Regular Reply Keyboard
keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = KeyboardButton("وارد کردن اطلاعات")
button2 = KeyboardButton("url")
keyboard.add(button1, button2)

# Inline Keyboard
def get_inline_keyboard():
    inline_keyboard = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("👤 مشاهده پروفایل", callback_data="view_profile")
    btn2 = InlineKeyboardButton("✏️ ویرایش اطلاعات", callback_data="edit_info")
    inline_keyboard.add(btn1, btn2)
    return inline_keyboard

@bot.message_handler(commands=['start'])  
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! یکی از دستورات زیر را انتخاب کنید:", reply_markup=keyboard)

@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    try:
        results = []

        results.append( 
            types.InlineQueryResultArticle(
                id='1', 
                title='Join the Bot',
                description="Click to join Maneli's bot",
                input_message_content=types.InputTextMessageContent(
                    message_text="Join the bot here: https://t.me/mnl_ftr_bot"
                )
            )
        )

        results.append( 
            types.InlineQueryResultArticle(
                id='2', 
                title='Say Hello!',
                description="Send a greeting message to the bot.",
                input_message_content=types.InputTextMessageContent(
                    message_text="Hello! How can I assist you today?"
                )
            )
        )

        bot.answer_inline_query(query.id, results, cache_time=0)
    except Exception as e:
        print(e)


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
    bot.send_message(chat_id, f"✅ اطلاعات شما ثبت شد:\nنام: {user_profiles[chat_id]['name']}\nسن: {message.text}",
                     reply_markup=get_inline_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    chat_id = call.message.chat.id

    if call.data == "view_profile":
        if chat_id in user_profiles:
            name = user_profiles[chat_id].get("name", "نامشخص")
            age = user_profiles[chat_id].get("age", "نامشخص")
            bot.send_message(chat_id, f"👤 پروفایل شما:\nنام: {name}\nسن: {age}")
        else:
            bot.send_message(chat_id, "⛔ شما هنوز اطلاعاتی وارد نکرده‌اید.")

    elif call.data == "edit_info":
        bot.send_message(chat_id, "🔄 اطلاعات قبلی حذف شد. لطفاً نام خود را دوباره وارد کنید:")
        bot.register_next_step_handler(call.message, save_name)

@bot.message_handler(func=lambda message: message.text == "url")
def request_url(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "لطفاً لینک مورد نظر را ارسال کنید:")
    bot.register_next_step_handler(message, process_url)

def process_url(message):
    url = message.text
    chat_id = message.chat.id

    if not url.startswith("http"):
        bot.send_message(chat_id, "لینک نامعتبر است. لطفاً یک لینک معتبر ارسال کنید.")
        return

    try:
        file_path = download_file(url)
        with open(file_path, "rb") as file:
            bot.send_document(
                chat_id=chat_id,
                document=file,
                caption="فایل شما با موفقیت دانلود شد!"
            )
        schedule_deletion(file_path, delay=60)  # Delete after 60 seconds

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        bot.send_message(chat_id, "مشکلی در دانلود فایل موردنظر پیش آمد.")

def download_file(url):
    local_filename = os.path.join(DOWNLOAD_DIR, url.split("/")[-1])

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return local_filename

def schedule_deletion(file_path, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")

    threading.Thread(target=delete, daemon=True).start()
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "دستور نامعتبر است. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=keyboard)

bot.infinity_polling()
