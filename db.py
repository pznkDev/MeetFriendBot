import aiopg.sa


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
