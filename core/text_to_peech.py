import telebot
import os
import logging
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

# Ensure the voices directory exists
if not os.path.exists('voices'):
    os.makedirs('voices')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Send me a text and I will read it for you in English"
    )

@bot.message_handler(func=lambda message: True)
def text_to_speech(message):
    text = message.text
    file_name = "voices/output.mp3"
    output = gTTS(text=text, lang="en", tld='com.au')
    output.save(file_name)
    bot.send_voice(chat_id=message.chat.id, reply_to_message_id=message.id, voice=open(file_name, "rb"))
    os.remove(file_name)

bot.infinity_polling()
