import asyncio
import logging

from aiohttp import web

from db import init_pg, close_pg
from routes import setup_routes
from settings import get_config


def init(loop):
    config = get_config()
    app = web.Application(loop=loop)
    app['config'] = config

    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

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
