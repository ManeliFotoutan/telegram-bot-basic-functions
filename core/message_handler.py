import telebot
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

#Handle /help and /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hiii,Here is Maneli's bot!")
    bot.send_message(message.chat.id,json.dumps(message.chat.__dict__,indent=4,ensure_ascii=False))


# Handle document type
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    if message.content_type == "document":
        print("It's a document")
    elif message.content_type == "audio":
        print("It's an audio file")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "چه عکس زیبایی!")
    
@bot.message_handler(regexp="Maneli")
def handle_message(message):
    print("triggered")

@bot.message_handler(func=lambda message: message.text in ["hello", "hi"])
def handle_text_doc(message):
    bot.reply_to(message, "Hi!")

@bot.message_handler(func=lambda message: message.text == "سلام")
def greet(message):
    bot.reply_to(message, "سلام! چطوری؟")

print("Bot is starting...")
bot.infinity_polling()