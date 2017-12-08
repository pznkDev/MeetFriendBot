import datetime

import aiopg.sa as sa
from sqlalchemy import and_

from models import users, states, Sex, State


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']
    engine = await sa.create_engine(
        database=conf['DB_NAME'],
        user=conf['DB_USER'],
        password=conf['DB_PASSWORD'],
        host=conf['DB_HOST'],
        port=conf['DB_PORT'],
        minsize=1,
        maxsize=5,
        loop=app.loop
    )
    app['db'] = engine
    # await init_db(engine, conf)


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def create_tables(conn, config):
    for table_name in ['states', 'users']:
        await conn.execute('DROP TABLE IF EXISTS {}'.format(table_name))

    await conn.execute('DROP TYPE IF EXISTS sex;')

    await conn.execute('''
            CREATE TYPE sex AS ENUM (
                'male',
                'female'
            );
            ALTER TYPE sex OWNER TO {};
    '''.format(config['DB_USER']))

    await conn.execute('''
            CREATE TABLE states (
               id serial PRIMARY KEY,
               chat_id int UNIQUE NOT NULL,
               state varchar(50),
               age int,
               sex sex DEFAULT 'male'::sex,
               location json,
               time int
            );
            ALTER TABLE states OWNER TO {};
    '''.format(config['DB_USER']))

    await conn.execute('''
            CREATE TABLE users (
               id serial PRIMARY KEY,
               chat_id int UNIQUE NOT NULL,
               username varchar(50) UNIQUE NOT NULL,
               age varchar(50) NOT NULL,
               sex sex DEFAULT 'male'::sex,
               location json,
               expires_at TIMESTAMP DEFAULT now()
            );
            ALTER TABLE users OWNER TO {};
    '''.format(config['DB_USER']))


async def init_db(engine, config):
    async with engine:
        async with engine.acquire() as conn:
            await create_tables(conn, config)

        async with engine.acquire() as conn:
            await conn.execute(users.insert().values(
                chat_id=1,
                username='@lol',
                age=18,
                sex=Sex.male,
                location={'lat': 50.5, 'lng': 30.4}
            ))


async def get_all_users(conn):
    rows = await conn.execute(
        users.select()
    )
    user_records = await rows.fetchall()
    if not user_records:
        msg = "There is no user_find records"
        raise RecordNotFound(msg)
    return user_records


async def get_users_with_params(conn, params):
    rows = await conn.execute(
        users.select()
             .where(
                and_(
                    users.c.age == params['age'],
                    users.c.sex == params['sex']
                )
        )
    )
    return await rows.fetchall()


async def insert_user(conn, user):
    user["expires_at"] = datetime.datetime.now() + datetime.timedelta(minutes=int(user["expires_at"]))
    await conn.execute(
        users.insert().values(user)
    )


async def get_state_by_chat_id(conn, chat_id):
    row = await conn.execute(
        states.select().where(states.c.chat_id == int(chat_id))
    )
    return await row.fetchone()


async def insert_state(conn, chat_id):
    await conn.execute(
        states.insert().values(chat_id=chat_id, state=State.STATE_INIT.value)
    )


def update_state_by_chat_id(conn, chat_id, params):
    # TODO: update state with params by chat_id
    return None
