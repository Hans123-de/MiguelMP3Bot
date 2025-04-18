from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp
import os

TOKEN = "7276157668:AAE58JVVNPT4eIjxdilHIe5N7_L9ZWr4Qfo"

welcome_message_fr = "Yo , c'est comment? Tu veux l'audio n'est ce pas? Colle juste le lien Youtube et tu pourras recevoir ton audio."
welcome_message_en = "Yo, what's up? You want the audio, right? Just paste the YouTube link and you'll get your audio."

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"{welcome_message_fr}\n\n{welcome_message_en}")

def download_audio(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    update.message.reply_text("Téléchargement en cours...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open("audio.mp3", "rb") as audio:
            update.message.reply_audio(audio)
        os.remove("audio.mp3")
    except Exception as e:
        update.message.reply_text("Erreur lors du téléchargement 😢")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_audio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()