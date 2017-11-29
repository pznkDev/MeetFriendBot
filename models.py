import enum

import sqlalchemy as sa


meta = sa.MetaData()


class State(enum.Enum):
    STATE_INIT = 1

    STATE_LOGIN_START = 2
    STATE_LOGIN_INPUT_AGE = 3
    STATE_LOGIN_INPUT_SEX = 4
    STATE_LOGIN_INPUT_LOCATION = 5
    STATE_LOGIN_INPUT_TIME = 6

    STATE_FIND_INPUT_AGE = 7
    STATE_FIND_INPUT_SEX = 8
    STATE_FIND_INPUT_LOCATION = 9

    def __str__(self):
        return self.name


class Sex(enum.Enum):
    male = 1
    female = 2


user_login = sa.Table(
    'user_login', meta,

    sa.Column('id', sa.Integer),
    sa.Column('chat_id', sa.Integer, unique=True, nullable=False),
    sa.Column('username', sa.String(50), unique=True),
    sa.Column('age', sa.String(50)),
    sa.Column('sex', sa.Enum(Sex)),
    sa.Column('location', sa.JSON),
    sa.Column('time', sa.Integer),

    sa.PrimaryKeyConstraint('id', name='user_login_id_pkey'),
)


user_find = sa.Table(
    'user_find', meta,

    sa.Column('id', sa.Integer),
    sa.Column('chat_id', sa.Integer, unique=True, nullable=False),
    sa.Column('age', sa.String(50)),
    sa.Column('sex', sa.Enum(Sex)),
    sa.Column('location', sa.JSON),

    sa.PrimaryKeyConstraint('id', name='user_find_id_pkey'),
)

