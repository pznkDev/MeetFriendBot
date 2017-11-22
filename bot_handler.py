import telebot

import bot_messages as bot_msg

# mock database for a time
history = {}


def handle_start(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('/login', '/find')
    bot.send_message(message.chat.id, bot_msg.MSG_START, parse_mode='Markdown', reply_markup=markup_start)


def handle_find(bot, message):
    history[message.chat.id] = {
        'state': bot_msg.STATE_FIND_START
    }
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_START, parse_mode='Markdown')


def send_msg(bot, chat_id, msg):
    bot.send_message(chat_id, msg, parse_mode='Markdown')


def handle_message(bot, message):
    # TODO: get state from database
    state = history[message.chat.id]['state'] if message.chat.id in history else ''
    print('Current_state:', state)

    if state == bot_msg.STATE_FIND_START:
        try:
            age = int(message.text)
            if 0 < age < 6:
                send_msg(bot, message.chat.id, 'WE ARE YOUNG')
            elif 6 <= age <= 100:
                history[message.chat.id]['find_age'] = age
                history[message.chat.id]['state'] = bot_msg.STATE_FIND_INPUT_AGE
                print(history)
            elif age > 100:
                send_msg(bot, message.chat.id, 'Too old')
            else:
                send_msg(bot, message.chat.id, 'Incorrect age')

        except ValueError:
            send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_AGE)
    else:
        pass
