import db

from aiohttp import web


async def get_all_users(request):
    async with request.app['db'].acquire() as conn:
        try:
            user_records = await db.get_all_users(conn)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        users = [dict(u) for u in user_records]
        return web.json_response({'users': users})