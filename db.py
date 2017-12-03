import aiopg.sa
from models import users, Sex


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']
    engine = await aiopg.sa.create_engine(
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
    # await init_db(engine)


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
            ALTER TYPE sex OWNER TO meet_user;
    ''')

    await conn.execute('''
            CREATE TABLE states (
               id serial PRIMARY KEY,
               chat_id int UNIQUE NOT NULL,
               state varchar(50),
               age int NOT NULL,
               sex sex DEFAULT 'male'::sex,
               location json,
               time int NOT NULL
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
