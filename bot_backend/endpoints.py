from aiohttp import web


async def main(request):
    return web.Response(text='Lol')
