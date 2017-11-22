MSG_START = 'Hello, i\'ll help you to _find new friends_) Choose */login* to create account or */find* to look for ' \
            'some new friends '
MSG_FIND_START = 'Okay, let me see... \n_(it can take a few seconds)_'

MSG_FIND_INPUT_START = 'Let\'s find somebody. But first, input *age*'
MSG_FIND_INPUT_SEX = '*male* or *female* ?'
MSG_FIND_INPUT_LOCATION = 'Enter country(english)'

MSG_ERROR_AGE = 'Sorry, but age is incorrect'
MSG_ERROR_SEX = 'Sorry, but sex is incorrect'
MSG_ERROR_LOCATION = 'Sorry, but location is incorrect'


# states for Finite-state machine
STATE_INIT = 'state_init'

STATE_LOGIN_START = 'state_login_start'
STATE_LOGIN_INPUT_NAME = 'state_login_input_name'
STATE_LOGIN_INPUT_ID = 'state_login_input_id'
STATE_LOGIN_INPUT_AGE = 'state_login_input_age'
STATE_LOGIN_INPUT_SEX = 'state_login_input_sex'
STATE_LOGIN_INPUT_LOCATION = 'state_login_input_location'

STATE_FIND_INPUT_AGE = 'state_find_input_age'
STATE_FIND_INPUT_SEX = 'state_find_input_sex'
STATE_FIND_INPUT_LOCATION = 'state_find_input_location'
