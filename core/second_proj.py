import telebot
import os
from dotenv import load_dotenv
import logging
import requests
import threading
import time
from pytube import YouTube

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
        message.chat.id,
        "Welcome! Send me a YouTube video URL, and I will download it and send it to you."
    )

import yt_dlp

def download_youtube_video(url):
    ydl_opts = {
        'outtmpl': DOWNLOAD_DIR + '%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'cookies': 'cookies.txt',  
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)
    return video_filename, os.path.basename(video_filename)


def schedule_deletion(file_path, delay=60):
    def delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")

    threading.Thread(target=delete, daemon=True).start()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtu" in url:
        try:
            file_path, video_filename = download_youtube_video(url)
            with open(file_path, "rb") as video_file:
                bot.send_document(
                    chat_id=message.chat.id,
                    reply_to_message_id=message.id,
                    document=video_file,
                    caption=f"Here is your video: {video_filename}"
                )
            schedule_deletion(file_path, delay=60)
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {e}")
            bot.reply_to(message, text="There was a problem downloading the video.")
    else:
        bot.reply_to(message, text="Please send a valid YouTube video URL.")

print("Bot is starting...")
bot.infinity_polling()
