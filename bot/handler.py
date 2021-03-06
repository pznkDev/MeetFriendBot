from ast import literal_eval
import json
from time import sleep
from random import randint

import requests
import telebot

from bot import utils as const

URL = 'http://127.0.0.1:8080/'


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


def make_request_get(url):
    attempt = 0
    while True:
        if attempt == 5:
            return
        attempt += 1
        try:
            response = requests.get(url)
            if response.status_code == 500:
                sleep(attempt * randint(1, 3))
            else:
                return response.text
        except:
            sleep(attempt * randint(1, 3))


def make_request_post(url, data):
    attempt = 0
    while True:
        if attempt == 5:
            return
        attempt += 1
        try:
            response = requests.post(url, data=data)
            if response.status_code == 500:
                sleep(attempt * randint(1, 3))
        except:
            sleep(attempt * randint(1, 3))


def make_request_put(url, data):
    attempt = 0
    while True:
        if attempt == 5:
            return
        attempt += 1
        try:
            response = requests.put(url, data=data)
            if response.status_code == 500:
                sleep(attempt * randint(1, 3))

        except:
            sleep(attempt * randint(1, 3))


def get_cur_state(chat_id):
    """ Returns current user's state from table 'states' by chat_id """
    response = make_request_get(URL + 'states/%s/' % str(chat_id))
    return literal_eval(json.loads(response.text).get('state'))


def update_cur_form(data):
    """ Updates user's form for login/find in db """
    make_request_put(URL + 'states/', data=json.dumps(data))


def handle_start(bot, message):
    """ Handles command /start"""
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('/login', '/find')
    bot.send_message(message.chat.id, const.MSG_START, parse_mode='Markdown', reply_markup=markup_start)


def handle_find(bot, message):
    """
        Handles command /find. Find is used to find some people by following params:
        -age
        -sex
        -location (choose top 3 people with minimum distances)
    """
    state = {
        'chat_id': message.chat.id,
        'state': const.STATE_FIND_INPUT_AGE,
        'age': None,
        'location': None,
        'time': None
    }
    update_cur_form(state)
    send_msg(bot, message.chat.id, const.MSG_FIND_INPUT_START)
    send_msg_input_age(bot, message)


def handle_login(bot, message):
    """ Handles command /login. Login is used to become visible for other people. """
    state = {
        'chat_id': message.chat.id,
        'state': const.STATE_LOGIN_INPUT_AGE,
        'age': None,
        'location': None,
        'time': None
    }
    update_cur_form(state)
    send_msg_input_age(bot, message)


def handle_message(bot, msg):
    """ Realization of finite-state machine of user_journey with simple text=messages"""
    form = get_cur_state(msg.chat.id)
    state = form.get('state')

    if state in (const.STATE_FIND_INPUT_AGE, const.STATE_LOGIN_INPUT_AGE) and valid_age(bot, msg):
        form.update(
            {
                'age': msg.text,
                'state': const.STATE_FIND_INPUT_SEX if state == const.STATE_FIND_INPUT_AGE else const.STATE_LOGIN_INPUT_SEX
            }
        )
        update_cur_form(form)
        send_msg_input_sex(bot, msg)

    elif state in (const.STATE_FIND_INPUT_SEX, const.STATE_LOGIN_INPUT_SEX) and valid_sex(bot, msg):
        form.update(
            {
                'sex': msg.text,
                'state': const.STATE_FIND_INPUT_LOCATION if state == const.STATE_FIND_INPUT_SEX else const.STATE_LOGIN_INPUT_LOCATION
            }
        )
        update_cur_form(form)
        send_msg_input_location(bot, msg)

    elif state == const.STATE_LOGIN_INPUT_TIME and valid_time(bot, msg):
        form.update(
            {
                'expires_at': msg.text,
                'state': const.STATE_INIT,
                'username': '@slava_ko'
            }
        )
        form.pop('time', None)
        form.pop('state', None)
        form.pop('id', None)

        make_request_post(URL + 'users/', data=json.dumps(form))
        send_msg_login_start(bot, msg)


def handle_location(bot, msg):
    """ Additional handler, as addition for finite-state machine, as support of location attachments. """
    form = get_cur_state(msg.chat.id)
    state = form.get('state')

    if state in (const.STATE_FIND_INPUT_LOCATION, const.STATE_LOGIN_INPUT_LOCATION) and valid_location(bot, msg):
        form.update(
            {
                'location': str(msg.location),
                'state': const.STATE_INIT if state == const.STATE_FIND_INPUT_LOCATION else const.STATE_LOGIN_INPUT_TIME
            }
        )
        update_cur_form(form)

        if state == const.STATE_FIND_INPUT_LOCATION:
            send_msg_find_start(bot, msg)

            response = make_request_get(URL + ('users/find?age=%s&sex=%s&location=%s' %
                                               (
                                                   form.get('age'),
                                                   form.get('sex'),
                                                   str(form.get('location'))
                                               ))
                                        )
            send_msg_find_result(bot, msg.chat.id, literal_eval(json.loads(response.text).get('users')))
        else:
            send_msg_input_time(bot, msg)


def valid_age(bot, message):
    try:
        age = int(message.text)
        if 0 < age < 6:
            send_msg(bot, message.chat.id, 'TOO YOUNG')
        elif 6 <= age <= 100:
            return True
        elif age > 100:
            send_msg(bot, message.chat.id, 'TOO OLD')
        else:
            send_msg(bot, message.chat.id, 'Wrong input')
    except ValueError:
        send_msg(bot, message.chat.id, const.MSG_ERROR_AGE)


def valid_sex(bot, message):
    if message.text in ('male', 'female'):
        return True
    else:
        send_msg(bot, message.chat.id, const.MSG_ERROR_SEX)


def valid_location(bot, message):
    if message.location != '':
        return True
    else:
        send_msg(bot, message.chat.id, const.MSG_ERROR_LOCATION)


def valid_time(bot, message):
    if message.text in ('15', '30', '60', '90'):
        return True
    else:
        send_msg(bot, message.chat.id, const.MSG_ERROR_TIME)


def send_msg_input_age(bot, message):
    bot.send_message(message.chat.id, const.MSG_INPUT_AGE, parse_mode='Markdown')


def send_msg_input_sex(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('male', 'female')
    bot.send_message(message.chat.id, const.MSG_INPUT_SEX, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_input_location(bot, message):
    bot.send_message(message.chat.id, const.MSG_INPUT_LOCATION, parse_mode='Markdown')


def send_msg_input_time(bot, message):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('15', '30')
    markup_start.row('60', '90')
    bot.send_message(message.chat.id, const.MSG_INPUT_TIME, parse_mode='Markdown', reply_markup=markup_start)


def send_msg_find_start(bot, message):
    bot.send_message(message.chat.id, const.MSG_FIND_START, parse_mode='Markdown')


def send_msg_login_start(bot, message):
    bot.send_message(message.chat.id, const.MSG_LOGIN_START, parse_mode='Markdown')


def send_msg(bot, chat_id, msg):
    bot.send_message(chat_id, msg, parse_mode='Markdown')


def send_msg_find_result(bot, chat_id, users):
    if len(users) > 0:
        message = 'Well, good luck )'
        for i, user in enumerate(users):
            message += '\n' + str(i) + ') ' + user
    else:
        message = 'No users found =( \nTry again later...'
    bot.send_message(chat_id, message)
