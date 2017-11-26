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
    send_msg(bot, message.chat.id, bot_msg.MSG_FIND_INPUT_START)
    send_msg_input_age(bot, message)


def handle_login(bot, message):
    history[message.chat.id] = {
        'state': bot_msg.STATE_LOGIN_INPUT_AGE
    }
    send_msg_input_age(bot, message)


def validate_name(bot, message, new_status):
    if message.text != '':
        history[message.chat.id]['login_name'] = message.text
        history[message.chat.id]['state'] = new_status
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_NAME)


def validate_age(bot, message, new_status):
    try:
        age = int(message.text)
        if 0 < age < 6:
            send_msg(bot, message.chat.id, 'WE ARE YOUNG')
        elif 6 <= age <= 100:
            history[message.chat.id]['age'] = age
            history[message.chat.id]['state'] = new_status
            return True
        elif age > 100:
            send_msg(bot, message.chat.id, 'Too old')
        else:
            send_msg(bot, message.chat.id, 'Incorrect age')

    except ValueError:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_AGE)


def validate_sex(bot, message, new_status):
    if message.text in ('male', 'female'):
        history[message.chat.id]['sex'] = message.text
        history[message.chat.id]['state'] = new_status
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_SEX)


def validate_location(bot, message, new_status):
    if message.location != '':
        print(message.location)
        history[message.chat.id]['location'] = message.location
        history[message.chat.id]['state'] = new_status
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_LOCATION)


def validate_time(bot, message, new_status):
    if message.text in ('15', '30', '60', '90'):
        history[message.chat.id]['time'] = message.text
        history[message.chat.id]['state'] = new_status
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_TIME)


def handle_message(bot, msg):
    # TODO: get state from database
    state = history[msg.chat.id]['state'] if msg.chat.id in history else ''
    print('Current_state:', state)

    if state == bot_msg.STATE_FIND_INPUT_AGE and validate_age(bot, msg, bot_msg.STATE_FIND_INPUT_SEX):
        send_msg_input_sex(bot, msg)

    elif state == bot_msg.STATE_FIND_INPUT_SEX and validate_sex(bot, msg, bot_msg.STATE_FIND_INPUT_LOCATION):
        send_msg_input_location(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_AGE and validate_age(bot, msg, bot_msg.STATE_LOGIN_INPUT_SEX):
        send_msg_input_sex(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_SEX and validate_sex(bot, msg, bot_msg.STATE_LOGIN_INPUT_LOCATION):
        send_msg_input_location(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_TIME and validate_time(bot, msg, bot_msg.STATE_INIT):
        send_msg_login_start(bot, msg)
        # TODO "LOGIN" request
        user = history[msg.chat.id]
        print('REQUEST: Username=%s, Age=%s, Sex=%s, Location=%s, Time=%s' %
              (
                  msg.from_user.username,
                  user.get('age', ''),
                  user.get('sex', ''),
                  user.get('location', ''),
                  user.get('time', '')
              )
              )
    else:
        pass


def handle_location(bot, msg):
    # TODO: get state from database
    state = history[msg.chat.id]['state'] if msg.chat.id in history else ''
    print('Current_state:', state)

    if state == bot_msg.STATE_FIND_INPUT_LOCATION and validate_location(bot, msg, bot_msg.STATE_INIT):
        send_msg_find_start(bot, msg)
        # TODO "Find" request
        user = history[msg.chat.id]
        print('REQUEST: Age=%s, Sex=%s, Location=%s' %
              (
                  user.get('age', ''),
                  user.get('sex', ''),
                  user.get('location', '')
              )
              )

    elif state == bot_msg.STATE_LOGIN_INPUT_LOCATION and validate_location(bot, msg, bot_msg.STATE_LOGIN_INPUT_TIME):
        send_msg_input_time(bot, msg)


def send_msg_input_age(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_INPUT_AGE, parse_mode='Markdown')


def send_msg_input_sex(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('male', 'female')
    bot.send_message(message.chat.id, bot_msg.MSG_INPUT_SEX, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_input_location(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_INPUT_LOCATION, parse_mode='Markdown')


def send_msg_input_time(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('15', '30')
    markup_start.row('60', '90')
    bot.send_message(message.chat.id, bot_msg.MSG_INPUT_TIME, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_find_start(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_FIND_START, parse_mode='Markdown')


def send_msg_login_start(bot, message):
    bot.send_message(message.chat.id, bot_msg.MSG_LOGIN_START, parse_mode='Markdown')


def send_msg(bot, chat_id, msg):
    bot.send_message(chat_id, msg, parse_mode='Markdown')
