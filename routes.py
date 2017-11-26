from bot_backend.endpoints import main


def setup_routes(app):
    app.router.add_route('*', '/', main, name='main')
