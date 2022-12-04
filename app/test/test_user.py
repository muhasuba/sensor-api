import unittest

from app.main import db
# from app.main.model.blacklist import BlacklistToken
import json
from app.test.base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='joe@gmail.com',
            username='username',
            password='123456'
        )),
        content_type='application/json'
    )


def get_all_users(self):
    return self.client.get('/user/')


class TestUser(BaseTestCase):
    def test_get_all_users_initial(self):
        """ Test get all users initial"""
        with self.client:
            response = get_all_users(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 0)
            self.assertEqual(response.status_code, 200)

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['Authorization'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_get_all_users_after_register(self):
        """ Test get all users after register"""
        register_user(self)
        with self.client:
            response = get_all_users(self)
            data = json.loads(response.data.decode())
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'][0]['email'], "joe@gmail.com")
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
