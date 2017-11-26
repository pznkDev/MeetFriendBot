from envparse import env
from os.path import isfile


def get_config(file_name='.env'):
    if isfile(file_name):
        env.read_envfile(file_name)
    config = {'DEBUG': env.bool('DEBUG', default=False),
              'HOST': env.str('HOST'),
              'PORT': env.int('PORT'),
              'DB_NAME': env.str('DB_NAME'),
              'DB_USER': env.str('DB_USER'),
              'DB_PASSWORD': env.str('DB_PASSWORD'),
              'DB_HOST': env.str('DB_HOST'),
              'DB_PORT': env.str('DB_PORT'),
              }
    return config
