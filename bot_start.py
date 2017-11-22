import telebot

import bot_config as bot_cfg
import bot_handler as handler

bot = telebot.TeleBot(bot_cfg.BOT_TOKEN)


def handle_commands():
    @bot.message_handler(commands=['start'])
    def handle_command(message):
        handler.handle_start(bot, message)

    @bot.message_handler(content_types=['text'])
    def handle_command(message):
        print(message)


def main():
    handle_commands()

    # start long-polling
    bot.polling(none_stop=True, interval=1)


if __name__ == '__main__':
    main()
