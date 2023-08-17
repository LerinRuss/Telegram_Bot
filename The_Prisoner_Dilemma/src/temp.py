import telegram
import os


def main():
    bot = telegram.Bot(os.environ['TELEGRAM_BOT_TOKEN'])

    bot.send_message(chat_id=1136361832, text='Test')


if __name__ == '__main__':
    main()
