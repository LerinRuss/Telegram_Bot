from telegram import Update, ForceReply
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters
from google import genai
from google.genai import types
import os
import logging

# TODO to separate class
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(fr'Hi {user.mention_markdown_v2()}\!')


async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message"""
    await update.message.reply_text('This bot writes diminutives of the word you will write')


async def echo(update: Update, context: CallbackContext) -> None:
    sent_text = f"Result only of popular diminutives of a word {update.message.text} with corresponding meanings"
    response: types.GenerateContentResponse = client.models.generate_content(
        model='gemini-2.5-flash-preview-04-17-thinking', contents=sent_text)
    await update.message.reply_text(response.text)


def main():
    app: Application = ApplicationBuilder().token(token=os.environ['TELEGRAM_BOT_TOKEN']).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    app.run_polling()


if __name__ == '__main__':
    main()
