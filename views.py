import db

from aiohttp import web


async def get_users(request):
    async with request.app['db'].acquire() as conn:
        try:
            user_records = await db.get_all_users(conn)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        users = [dict(u) for u in user_records]
        return web.json_response({'users': str(users)})


async def add_user(request):
    # TODO: add validation
    user = None
    async with request.app['db'].acquire() as conn:
        await db.add_user(conn, user)

    return web.json_response()


async def find_users(request):
    # TODO: add validation
    params = {
        'age': 12,
        'sex': 1,
        'location': ''
    }

    async with request.app['db'].acquire() as conn:
        try:
            user_records = await db.get_users_with_params(conn, params)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        users = [dict(u) for u in user_records]

    # TODO: add realization of distance-min
    return web.json_response({'users': []})


async def get_state(request):
    # TODO: add validation
    chat_id = '12561236'

    async with request.app['db'].acquire() as conn:
        try:
            user_records = await db.get_state_by_chat_id(conn, chat_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        user = [dict(u) for u in user_records]
        return web.json_response({'users': str(user)})


async def update_state(request):
    # TODO: add validation
    chat_id = '12561236'
    params = {
        'age': 12,
        'sex': 1,
        'location': ''
    }

    async with request.app['db'].acquire() as conn:
        try:
            await db.update_state_by_chat_id(conn, chat_id, params)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
