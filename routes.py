from views import get_all_users


def setup_routes(app):
    app.router.add_route('*', '/', get_all_users, name='get_all_users')
