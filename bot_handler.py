import telebot

import bot_messages as bot_msg


def handle_start(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('/login', '/find')
    bot.send_message(message.chat.id, bot_msg.MSG_START, parse_mode='Markdown', reply_markup=markup_start)
