import telebot
import yt_dlp
import os
import scrapetube
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "video.mp4"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "سلام! من یک ربات دانلود ویدئو از یوتیوب هستم. لطفاً لینک ویدئو را ارسال کنید.")

@bot.message_handler(func=lambda message: message.text.startswith("https://www.youtube.com") or message.text.startswith("https://youtu.be"))
def handle_youtube_link(message):
    url = message.text
    bot.send_message(message.chat.id, "⏳ در حال دانلود ویدئو... لطفاً منتظر بمانید.")
    try:
        video_path = download_youtube_video(url)
        with open(video_path, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, reply_to_message_id=message.message_id, caption="ویدئوی شما آماده است!")
        os.remove(video_path)  
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطا در دانلود ویدئو: {str(e)}")

bot.polling()