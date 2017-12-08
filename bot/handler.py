import json

import requests
import telebot

from bot import utils as bot_msg

# mock database for a time
history = {}


def handle_commands(bot):
    @bot.message_handler(commands=['start'])
    def handle_command(message):
        handle_start(bot, message)

    @bot.message_handler(commands=['find'])
    def handle_command(message):
        handle_find(bot, message)

    @bot.message_handler(commands=['login'])
    def handle_command(message):
        handle_login(bot, message)

    @bot.message_handler(content_types=['text'])
    def handle_command(message):
        handle_message(bot, message)

    @bot.message_handler(content_types=['location'])
    def handle_command(message):
        handle_location(bot, message)


def get_cur_state(chat_id):
    """ Returns current user's state from table 'states' by chat_id """
    response = requests.get('http://127.0.0.1:8080/states/%s/' % str(chat_id))
    return json.loads(response.text)


def set_cur_state(chat_id, new_state):
    """ Sets new user's state in db by chat_id """
    # TODO insert request to server
    history[chat_id] = {
        'state': new_state
    }


def update_cur_form(chat_id, d):
    """ Updates user's form for login/find in db """
    # TODO insert request to server
    history[chat_id].update(d)


def handle_start(bot, message):
    """ Handles command /start"""
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('/login', '/find')
    bot.send_message(message.chat.id, bot_msg.MSG_START, parse_mode='Markdown', reply_markup=markup_start)


def handle_find(bot, message):
    """
        Handles command /find. Find is used to find some people by following params:
        -age
        -sex
        -location (choose top 3 people with minimum distances)
    """
    set_cur_state(message.chat.id, bot_msg.STATE_FIND_INPUT_AGE)
    send_msg(bot, message.chat.id, bot_msg.MSG_FIND_INPUT_START)
    send_msg_input_age(bot, message)


def handle_login(bot, message):
    """ Handles command /login. Login is used to become visible for other people. """
    set_cur_state(message.chat.id, bot_msg.STATE_LOGIN_INPUT_AGE)
    send_msg_input_age(bot, message)


def handle_message(bot, msg):
    """ Realization of finite-state machine of user_journey with simple text=messages"""
    form = get_cur_state(msg.chat.id)
    state = form.get('state')

    if state == bot_msg.STATE_FIND_INPUT_AGE and update_age(bot, msg, bot_msg.STATE_FIND_INPUT_SEX):
        send_msg_input_sex(bot, msg)

    elif state == bot_msg.STATE_FIND_INPUT_SEX and update_sex(bot, msg, bot_msg.STATE_FIND_INPUT_LOCATION):
        send_msg_input_location(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_AGE and update_age(bot, msg, bot_msg.STATE_LOGIN_INPUT_SEX):
        send_msg_input_sex(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_SEX and update_sex(bot, msg, bot_msg.STATE_LOGIN_INPUT_LOCATION):
        send_msg_input_location(bot, msg)

    elif state == bot_msg.STATE_LOGIN_INPUT_TIME and update_time(bot, msg, bot_msg.STATE_INIT):
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


def handle_location(bot, msg):
    """ Additional handler, as addition for finite-state machine, as support of location attachments. """
    form = get_cur_state(msg.chat.id)
    state = form.get('state')

    if state == bot_msg.STATE_FIND_INPUT_LOCATION and update_location(bot, msg, bot_msg.STATE_INIT):
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

    elif state == bot_msg.STATE_LOGIN_INPUT_LOCATION and update_location(bot, msg, bot_msg.STATE_LOGIN_INPUT_TIME):
        send_msg_input_time(bot, msg)


def update_age(bot, message, new_status):
    try:
        age = int(message.text)
        if 0 < age < 6:
            send_msg(bot, message.chat.id, 'TOO YOUNG')
        elif 6 <= age <= 100:
            new_data = {
                'age': age,
                'state': new_status
            }
            update_cur_form(message.chat.id, new_data)
            return True
        elif age > 100:
            send_msg(bot, message.chat.id, 'TOO OLD')
        else:
            send_msg(bot, message.chat.id, 'Wrong input')

    except ValueError:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_AGE)


def update_sex(bot, message, new_status):
    if message.text in ('male', 'female'):
        new_data = {
            'sex': message.text,
            'state': new_status
        }
        update_cur_form(message.chat.id, new_data)
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_SEX)


def update_location(bot, message, new_status):
    if message.location != '':
        new_data = {
            'location': message.location,
            'state': new_status
        }
        update_cur_form(message.chat.id, new_data)
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_LOCATION)


def update_time(bot, message, new_status):
    if message.text in ('15', '30', '60', '90'):
        new_data = {
            'time': message.text,
            'state': new_status
        }
        update_cur_form(message.chat.id, new_data)
        return True
    else:
        send_msg(bot, message.chat.id, bot_msg.MSG_ERROR_TIME)


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
