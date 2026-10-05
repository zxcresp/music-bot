from database import *
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hi.. 1000-7.. I`m dead inside, I wanna to kill myself, LOL. 6767676767')

@bot.message_handler(content_types=["audio"])
def receive_audio(message):
    user_id = message.from_user.id
    audio = message.audio
    file_name = audio.file_name
    title = file_name.rsplit(".", 1)[0]

    print("User ID:", user_id)
    print("File ID:", audio.file_id)
    print("File name:", file_name)
    print("Title:", title)
    print("Duration:", audio.duration)

    add_song(user_id, audio.file_id, title, audio.duration)
    bot.reply_to(message, f"Received: {title}")

create_database()

@bot.message_handler(commands=['songs'])
def receive_songs(message):
    user_id = message.from_user.id
    songs = get_song_titles(user_id)

    text = "Current songs:\n"

    for index, song in enumerate(songs, start=1):
        text += f"{index}) {song[0]}\n"

    bot.send_message(message.chat.id, text)


#print("Bot is running...")

#clear_songs()  #!!!!!!!! IT`S FOR DELETE DATABASE, DON`T UNCOMMENT IT !!!!!!!!!

bot.polling(non_stop=True)