import json

from aiohttp import web
from geopy.distance import vincenty

import db
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
    params = {
        'age': request.query.get('age'),
        'sex': request.query.get('sex'),
        'loc': json.loads(request.query.get('location'))
    }

    users, users_result = [], []
    async with request.app['db'].acquire() as conn:
        try:
            users = await db.get_users_with_params(conn, params)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        users = [dict(u) for u in users]

    # find 3 users with minimum distance to request location
    if len(users) > 3:
        cur_loc = (float(params['loc']['latitude']), float(params['loc']['longitude']))
        min_distance_index_dict = {}
        cur_max = float('inf')

        for user in users:
            user_loc = (float(user['location']['latitude']), float(user['location']['longitude']))
            cur_dist = vincenty(cur_loc, user_loc).km

            if len(min_distance_index_dict.keys()) < 3:
                min_distance_index_dict[cur_dist] = user['id']
                if cur_max < cur_dist or cur_max == float('inf'):
                    cur_max = cur_dist
            else:
                if cur_max > cur_dist:
                    min_distance_index_dict.pop(cur_max, None)
                    min_distance_index_dict[cur_dist] = user['id']
                    cur_max = max([key for key in min_distance_index_dict])

        users_result = [user for user in users if user['id'] in min_distance_index_dict.values()]
        return web.json_response({'users': str(users_result)})

    else:
        return web.json_response({'users': str(users)})


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
