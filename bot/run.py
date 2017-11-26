import telebot

from bot import config as bot_cfg
from bot.handler import handle_commands


def main():
    bot = telebot.TeleBot(bot_cfg.BOT_TOKEN)

    handle_commands(bot)

    # start long-polling
    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()
