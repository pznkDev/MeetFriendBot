from asyncio import sleep

TWO_MINUTES = 120


async def init_task(app):
    app['task'] = app.loop.create_task(cleaner(app))


async def close_task(app):
    app['task'].close()


async def cleaner(app):
    while True:
        # TODO get all users, cleaning function
        await sleep(TWO_MINUTES)
