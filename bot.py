import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

BOT_TOKEN = "8551564266:AAHWUyO0PHUAntdnhtG04h8RgCecxXvWp2w"
DOWNLOAD_FILE = "music.mp3"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "HOLAAA! Woookie is online! \n"
        "Use the commands below: \n"
        "/song <song name or YouTube link>"
    )
    await update.message.reply_text(message)


async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Then what do you want me to play dude? \n")
        return

    search_query = " ".join(context.args)

    await update.message.reply_text("Searching for your music, please wait...")

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": "music.%(ext)s",
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(f"ytsearch1:{search_query}", download=True)

        if not info or "entries" not in info or not info["entries"]:
            await update.message.reply_text("No results found")
            return

        video = info["entries"][0]

        title = video.get("title", search_query)
        artist = video.get("artist") or video.get("uploader", "Unknown artist")
        duration = video.get("duration")

        with open(DOWNLOAD_FILE, "rb") as audio_file:
            await update.message.reply_audio(
                audio=audio_file, title=title, performer=artist, duration=duration
            )

    except Exception as error:
        print("An error occurred:", error)
        await update.message.reply_text("Failed to download the song.")

    finally:
        if os.path.exists(DOWNLOAD_FILE):
            os.remove(DOWNLOAD_FILE)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song))

    print("Music bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
