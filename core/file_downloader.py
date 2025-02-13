import telebot
import os
from dotenv import load_dotenv
import logging
import requests
import threading
import time

load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

DOWNLOAD_DIR = "downloads/"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Give me a valid URL for a file, and I will download and upload it here for you.")


def download_file(url):
    local_filename = url.split('/')[-1]
    file_path = os.path.join(DOWNLOAD_DIR, local_filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return file_path


def schedule_deletion(file_path, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")

    threading.Thread(target=delete, daemon=True).start()


@bot.message_handler(func=lambda message: True)
def download_file_url(message):
    logger.info(message.text)
    url = message.text
    try:
        file_path = download_file(url)
        bot.send_document(
            chat_id=message.chat.id,
            reply_to_message_id=message.id,
            document=open(file_path, "rb"),
            caption="File downloaded successfully, ENJOY!"
        )
        schedule_deletion(file_path, delay=60)  
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        bot.reply_to(message, text="Problem downloading the requested file.")


print("Bot is starting...")
bot.infinity_polling()
