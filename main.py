from threading import Thread
from serv import app
from time import sleep
import os
import telebot
import random
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler
from telebot.types import InputFile, ReplyKeyboardMarkup, KeyboardButton
from db import db_creation, add_user_id, update_chat_id

# running Flask server for the bot to be always on on Replit
Thread(target=lambda: app.run(host="0.0.0.0")).start()

api_key = os.getenv("BOT_API")

# bot instance initialization
bot = telebot.TeleBot(f"{api_key}")

# sqlite db initialization
db = sqlite3.connect("pusha.db", check_same_thread=False)
db_creation()

belly_str = "Belly🐈"
loaf_str = "Loaf🍞"
statue_str = "Statue🐱"
funny_str = "Funny😹"
video_str = "Video📹"
random_str = "Random category🔄"


# start command, just a simple message
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.reply_to(
        message,
        "Hello and welcome to Random Pusha Bot (meow)! Choose between different categories with commands (such as /belly, /loaf, /statue, /random) and get random pics (and even videos) of our cat!",
    )

    user_id = message.from_user.id
    chat_id = message.chat.id

    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    belly = KeyboardButton(text=belly_str)
    loaf = KeyboardButton(text=loaf_str)
    statue = KeyboardButton(text=statue_str)
    funny = KeyboardButton(text=funny_str)
    video = KeyboardButton(text=video_str)
    random = KeyboardButton(text=random_str)

    keyboard.row(belly, loaf)
    keyboard.row(statue, funny)
    keyboard.row(video, random)

    bot.send_message(
        message.chat.id, "You can also choose with buttons", reply_markup=keyboard
    )


@bot.message_handler(commands=["belly"])
def handle_belly(message):
    belly_folder_path = os.path.join(os.getcwd(), "pusha", "belly")

    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    random_file = get_random_file(belly_folder_path)
    send_random_photo(chat_id, random_file)


@bot.message_handler(commands=["loaf"])
def handle_loaf(message):
    loaf_folder_path = os.path.join(os.getcwd(), "pusha", "loaf")

    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    random_file = get_random_file(loaf_folder_path)
    send_random_photo(chat_id, random_file)


@bot.message_handler(commands=["statue"])
def handle_statue(message):
    statue_folder_path = os.path.join(os.getcwd(), "pusha", "statue")

    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    random_file = get_random_file(statue_folder_path)
    send_random_photo(chat_id, random_file)


@bot.message_handler(commands=["funny"])
def handle_funny(message):
    funny_folder_path = os.path.join(os.getcwd(), "pusha", "funny")

    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    random_file = get_random_file(funny_folder_path)
    send_random_photo(chat_id, random_file)


@bot.message_handler(commands=["video"])
def handle_video(message):
    video_folder_path = os.path.join(os.getcwd(), "pusha", "videos")

    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    random_file = get_random_file(video_folder_path)
    bot.send_message(chat_id, "Please wait...")
    send_random_video(chat_id, random_file)


@bot.message_handler(commands=["random"])
def handle_random(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    send_random_photo_from_random_folder(bot, chat_id)


# when button is pressed (generally)
@bot.message_handler(content_types=["text"])
def handle_messages(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    add_user_id(user_id, chat_id)
    update_chat_id(user_id, chat_id)

    if belly_str in message.text:
        handle_belly(message)
    elif loaf_str in message.text:
        handle_loaf(message)
    elif statue_str in message.text:
        handle_statue(message)
    elif funny_str in message.text:
        handle_funny(message)
    elif video_str in message.text:
        handle_video(message)
    elif random_str in message.text:
        handle_random(message)
    else:
        bot.reply_to(message, "Something is wrong")


def daily_dose_of_pusha():
    result = db.execute("SELECT chat_id FROM user_ids")
    try:
        rows = result.fetchall()
        for row in rows:
            chat_id = row[0]
            bot.send_message(chat_id, "Daily dose of Pusha")
            send_random_photo_from_random_folder(bot, chat_id)
            sleep(5)
    except Exception as e:
        print("Error occurred while fetching chat IDs from the database:", e)


# sending daily dose of pusha each day on 5:00 MSK
scheduler = BlockingScheduler(timezone="Europe/Moscow")
scheduler.add_job(daily_dose_of_pusha, "cron", hour=5)


def schedule_checker():
    while True:
        scheduler.start()


"""
files are hosted in the same directory as script, 
under "pusha/{category}"
"""


def get_random_file(folder_path):
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
    return file_path


def send_random_photo(chat_id, file_path):
    bot.send_photo(chat_id, InputFile(file_path))


def send_random_video(chat_id, file_path):
    bot.send_video(chat_id, InputFile(file_path))


def send_random_photo_from_random_folder(bot, chat_id):
    pusha_path = os.path.join(os.getcwd(), "pusha")
    folders = [
        f for f in os.listdir(pusha_path) if os.path.isdir(os.path.join(pusha_path, f))
    ]
    num_folders = len(folders)

    if num_folders == 0:
        return

    random_folder_index = random.randint(0, num_folders - 1)
    folder_name = folders[random_folder_index]
    folder_path = os.path.join(pusha_path, folder_name)

    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    num_files = len(files)

    if num_files == 0:
        return

    random_file_index = random.randint(0, num_files - 1)
    file_name = files[random_file_index]
    file_path = os.path.join(folder_path, file_name)
    bot.send_message(chat_id, f"{folder_name.capitalize()}!")
    bot.send_photo(chat_id, InputFile(file_path))


Thread(target=schedule_checker).start()

bot.infinity_polling()
