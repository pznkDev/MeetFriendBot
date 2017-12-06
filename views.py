import db

from aiohttp import web

from models import State


async def get_users(request):
    async with request.app['db'].acquire() as conn:
        try:
            user_records = await db.get_all_users(conn)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        users = [dict(u) for u in user_records]
        return web.json_response({'users': str(users)})


async def add_user(request):
    user = await request.json()
    async with request.app['db'].acquire() as conn:
        await db.insert_user(conn, user)
    return web.json_response({'message': 'success'})


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
    chat_id = request.match_info['chat_id']

    async with request.app['db'].acquire() as conn:
        user_record = None
        try:
            user_record = await db.get_state_by_chat_id(conn, chat_id)
        except db.RecordNotFound:
            print('get_state not found')
        if not user_record:
            await db.insert_state(conn, chat_id)
            return web.json_response({'state': State.STATE_INIT.value})

        user = dict(user_record)
        if user:
            state = user.get('state')
            return web.json_response({'state': state})
        else:
            return web.json_response({'error': 'unique chat_id error'})


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
