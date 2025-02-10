import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Handle /help and /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hiii, here is Maneli's bot!")

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

bot.infinity_polling()
