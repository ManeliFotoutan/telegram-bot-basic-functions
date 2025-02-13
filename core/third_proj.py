import telebot
import os
from dotenv import load_dotenv
import logging
from PIL import Image

load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

print("Bot is starting...")

def compress_image(file_path):
    with Image.open(file_path) as img:
        img.save(file_path, quality=50, optimize=True)

@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_text = (
        "سلام! به ربات فشرده‌سازی تصویر خوش آمدید.\n"
        "شما می‌توانید تصاویر خود را ارسال کنید تا به صورت خودکار فشرده شوند.\n"
        "برای استفاده از ربات، کافیست عکسی ارسال کنید."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        
        with open("temp_image.jpg", "wb") as new_file:
            new_file.write(downloaded_file)
        
        compress_image("temp_image.jpg")
        
        with open("temp_image.jpg", "rb") as compressed_image:
            bot.send_photo(message.chat.id, compressed_image)
        
        os.remove("temp_image.jpg")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا در پردازش تصویر: {e}")
        logger.error(f"Error while processing image: {e}")

@bot.inline_handler(lambda query: query.query == '')
def handle_inline_query(inline_query):
    results = [
        telebot.types.InlineQueryResultArticle(
            id='1',
            title="دسترسی به ربات",
            input_message_content=telebot.types.InputTextMessageContent("ربات شما در دسترس است"),
            url="https://t.me/mnl_frtn_bot"
        ),
        telebot.types.InlineQueryResultArticle(
            id='2',
            title="دسترسی به سایت",
            input_message_content=telebot.types.InputTextMessageContent("لینک به سایت: https://yoursite.com"),
            url="https://www.youtube.com/watch?v=Vz9APFI-zTs&list=PLMrD0rlQosDbq6_g0VU9PmDZCar3Y-r1M"
        ),
        telebot.types.InlineQueryResultArticle(
            id='3',
            title="توضیحات ربات",
            input_message_content=telebot.types.InputTextMessageContent("این ربات قادر است تصاویر شما را فشرده کند.")
        ),
    ]
    
    bot.answer_inline_query(inline_query.id, results)

bot.infinity_polling()
