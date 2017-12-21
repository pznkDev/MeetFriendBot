import json
import random
import string
import unittest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from db import close_pg
from run import init


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TestViews(AioHTTPTestCase):
    async def get_application(self):
        app = init()
        app.on_cleanup.append(close_pg)
        return app

    @unittest_run_loop
    async def test_get_state(self):
        route = '/states/{chat_id}/'
        chat_id = 1
        res = await self.client.request('GET', route.format(chat_id=chat_id))
        data = await res.json()
        assert res.status == 200
        assert 'state' in data
        for key in ['location', 'state', 'age', 'chat_id', 'time', 'sex']:
            assert key in data['state']
        state = json.loads(data['state'].replace("'", '"').replace('None', 'null'))
        assert chat_id == state['chat_id']
        assert 'male' in state['sex']

    @unittest_run_loop
    async def test_update_state(self):
        route = '/states/'
        chat_id = 1
        data = {
            "chat_id": chat_id,
            "state": "state_find_input_age",
            "age": None,
            "location": None,
            "time": None
        }
        res = await self.client.request('PUT', route, data=json.dumps(data))
        assert res.status == 200

        route_check = '/states/{chat_id}/'
        res_check = await self.client.request('GET', route_check.format(chat_id=chat_id))
        res_data = await res_check.json()
        state = json.loads(res_data['state'].replace("'", '"').replace('None', 'null'))
        del state['id']
        del state['sex']
        assert state == data

    @unittest_run_loop
    async def test_add_user(self):
        route = '/users/'
        data = {
            "chat_id": random.randint(0, 100000),
            "username": "@{}".format(random_string_generator()),
            "age": 18,
            "sex": "male",
            "location": {"latitude": 50.5, "longitude": 30.4},
            "expires_at": 30
        }
        res = await self.client.request('POST', route, data=json.dumps(data))
        assert res.status == 200

    @unittest_run_loop
    async def test_find_users(self):
        route = '/users/find?age={age}&sex={sex}&location={location}'
        res = await self.client.request('GET', route.format(
            sex='male',
            location={"latitude": 50.5, "longitude": 30.4},
            age=18
        ))
        assert res.status == 200
        data = await res.json()
        assert 'users' in data
        assert '@' in data['users']


if __name__ == '__main__':
    unittest.main()
