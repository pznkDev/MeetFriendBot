from views import (
    add_user,
    find_users,
    get_state,
    update_state
)


def setup_routes(app):
    app.router.add_route('POST', '/users/', add_user, name='add_user')
    app.router.add_route('GET', '/users/find', find_users, name='find_users') \
              .url(query='?age=age&sex=sex&location={}')
    app.router.add_route('GET', '/states/{chat_id}/', get_state, name='get_state')
    app.router.add_route('PUT', '/states/', update_state, name='update_state')
