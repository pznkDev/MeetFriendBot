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


states = sa.Table(
    'states', meta,

    sa.Column('id', sa.Integer),
    sa.Column('chat_id', sa.Integer, unique=True, nullable=False),
    sa.Column('state', sa.String(50)),
    sa.Column('age', sa.Integer),
    sa.Column('sex', sa.String(6)),
    sa.Column('location', sa.JSON),
    sa.Column('time', sa.Integer),

    sa.PrimaryKeyConstraint('id', name='states_id_pkey'),
)


users = sa.Table(
    'users', meta,

    sa.Column('id', sa.Integer),
    sa.Column('chat_id', sa.Integer, unique=True, nullable=False),
    sa.Column('username', sa.String(50)),
    sa.Column('age', sa.Integer),
    sa.Column('sex', sa.String(6)),
    sa.Column('location', sa.JSON),
    sa.Column('expires_at', sa.DateTime),

    sa.PrimaryKeyConstraint('id', name='users_id_pkey'),
)
