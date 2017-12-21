import asyncio
import logging

from aiohttp import web

from db import init_pg, close_pg
from periodic_tasks.user_cleaner import init_task, close_task
from routes import setup_routes
from settings import get_config


async def init_app(app):
    app.on_startup.append(init_pg)
    # app.on_startup.append(init_task)


async def destroy_app(app):
    await app.on_cleanup.append(close_pg)
    # await app.on_cleanup.append(close_task)


def init(loop=None):
    config = get_config()
    app = web.Application(loop=loop)
    app['config'] = config

    app.on_startup.append(init_app)
    if loop:
        app.on_cleanup.append(destroy_app)

    setup_routes(app)

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    app = init(loop)
    web.run_app(app,
                host=app['config']['HOST'],
                port=app['config']['PORT'])


if __name__ == '__main__':
    main()
