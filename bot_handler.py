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
        'state': bot_msg.STATE_FIND_INPUT_AGE
    }
    send_msg_find_input_age(bot, message)


def handle_message(bot, message):
    # TODO: get state from database
    state = history[message.chat.id]['state'] if message.chat.id in history else ''
    print('Current_state:', state)

    if state == bot_msg.STATE_FIND_INPUT_AGE:
        try:
            age = int(message.text)
            if 0 < age < 6:
                send_msg(bot, message.chat.id, 'WE ARE YOUNG')
            elif 6 <= age <= 100:
                history[message.chat.id]['find_age'] = age
                history[message.chat.id]['state'] = bot_msg.STATE_FIND_INPUT_SEX
                send_msg_find_input_sex(bot, message)
            elif age > 100:
                send_msg(bot, message.chat.id, 'Too old')
            else:
                send_msg(bot, message.chat.id, 'Incorrect age')

        except ValueError:
            send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_AGE)

    elif state == bot_msg.STATE_FIND_INPUT_SEX:
        if message.text in ('male', 'female'):
            history[message.chat.id]['find_sex'] = message.text
            history[message.chat.id]['state'] = bot_msg.STATE_FIND_INPUT_LOCATION
            send_msg_find_input_location(bot, message)
        else:
            send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_SEX)

    elif state == bot_msg.STATE_FIND_INPUT_LOCATION:
        if message.text != '':
            history[message.chat.id]['find_location'] = message.text
            history[message.chat.id]['state'] = bot_msg.STATE_INIT
            send_msg_find_start(bot, message)
            # TODO "Find" request
        else:
            send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_LOCATION)

    else:
        pass


def send_msg_find_input_age(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_INPUT_START, parse_mode='Markdown')


def send_msg_find_input_sex(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('male', 'female')
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_INPUT_SEX, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_find_input_location(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_INPUT_LOCATION, parse_mode='Markdown')


def send_msg_find_start(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_START, parse_mode='Markdown')


def send_msg(bot, chat_id, msg):
    bot.send_message(chat_id, msg, parse_mode='Markdown')
