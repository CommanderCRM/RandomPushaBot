import threading
from serv import app
import os
import telebot
import random
from telebot.types import InputFile, ReplyKeyboardMarkup, KeyboardButton

# running Flask server for the bot to be always on on Replit
threading.Thread(target=lambda: app.run(host="0.0.0.0")).start()

api_key = os.getenv("BOT_API")

# bot instance initialization
bot = telebot.TeleBot(f"{api_key}")

belly_str = "Belly🐈"
loaf_str = "Loaf🍞"
statue_str = "Statue🐱"


# start command, just a simple message
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(
        message,
        "Hello and welcome to Random Pusha Bot (meow)! Choose between /belly, /statue and /loaf and get random pics of our cat!",
    )
    keyboard = ReplyKeyboardMarkup()

    belly = KeyboardButton(text=belly_str)
    loaf = KeyboardButton(text=loaf_str)
    statue = KeyboardButton(text=statue_str)

    keyboard.add(belly)
    keyboard.add(loaf)
    keyboard.add(statue)

    bot.send_message(
        message.chat.id, "You can also choose with buttons", reply_markup=keyboard
    )


@bot.message_handler(commands=["belly"])
def handle_belly(message):
    belly_folder_path = os.path.join(os.getcwd(), "pusha", "belly")
    chat_id = message.chat.id
    send_random_photo(belly_folder_path, chat_id, bot)


@bot.message_handler(commands=["loaf"])
def handle_loaf(message):
    loaf_folder_path = os.path.join(os.getcwd(), "pusha", "loaf")
    chat_id = message.chat.id
    send_random_photo(loaf_folder_path, chat_id, bot)


@bot.message_handler(commands=["statue"])
def handle_statue(message):
    statue_folder_path = os.path.join(os.getcwd(), "pusha", "statue")
    chat_id = message.chat.id
    send_random_photo(statue_folder_path, chat_id, bot)


@bot.message_handler(content_types=["text"])
def handle_messages(message):
    if belly_str in message.text:
        handle_belly(message)
    elif loaf_str in message.text:
        handle_loaf(message)
    elif statue_str in message.text:
        handle_statue(message)
    else:
        bot.reply_to(message, "Something is wrong")


"""
files are hosted in the same directory as script, 
under "pusha/{category}"
"""


def send_random_photo(folder_path, chat_id, bot):
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    num_files = len(files)

    if num_files == 0:
      return

    random_index = random.randint(0, num_files - 1)
    file_name = files[random_index]
    file_path = os.path.join(folder_path, file_name)
    bot.send_photo(chat_id, InputFile(file_path))

bot.infinity_polling()