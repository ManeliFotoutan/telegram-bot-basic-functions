import logging
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.reply_to(message, """Hi this is a sample for learning telegram bot in python""")

bot.infinity_polling()