import aiopg.sa
from models import user_find


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


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def create_tables(conn):
    for table_name in ['user_login', 'user_find']:
        await conn.execute('DROP TABLE IF EXISTS {}'.format(table_name))

    # TODO: sex to ENUM, location to JSON
    await conn.execute('''
            CREATE TABLE user_login (
               id serial PRIMARY KEY,
               chat_id int UNIQUE NOT NULL,
               username varchar(50) UNIQUE,
               age varchar(50),
               sex   ENUM,
               location varchar(255),
               time int 
            )
    ''')

    await conn.execute('''
            CREATE TABLE user_find (
               id serial PRIMARY KEY,
               chat_id int UNIQUE NOT NULL,
               age varchar(50),
               sex varchar(255),
               location varchar(255)
            )
    ''')


async def init_db(engine):
    async with engine:
        async with engine.acquire() as conn:
            await create_tables(conn)

        # TODO: test data
        # async with engine.acquire() as conn:
        #     await conn.execute(table.insert().values(val=''))


async def get_all_users(conn):
    rows = await conn.execute(
        user_find.select()
    )
    user_records = await rows.fetchall()
    if not user_records:
        msg = "There is no user_find records"
        raise RecordNotFound(msg)
    return user_records
