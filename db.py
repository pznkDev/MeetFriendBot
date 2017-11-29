import aiopg.sa
from models import user_find, meta


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
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def get_all_users(conn):
    rows = await conn.execute(
        user_find.select()
    )
    user_records = await rows.fetchall()
    if not user_records:
        msg = "There is no user_find records"
        raise RecordNotFound(msg)
    return user_records
