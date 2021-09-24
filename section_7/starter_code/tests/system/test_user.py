
from section_7.starter_code.models.user import UserModel
import json
from section_7.starter_code.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(201, response.status_code, 'Request status code do not met expected.')
                self.assertIsNotNone(UserModel.find_by_username('test_user'), "User was not saved to DB.")
                self.assertDictEqual({'message': 'User was created successfully'},
                                 json.loads(response.data),
                                 "Request response message do not correspond to expected response message.")

    def test_register_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test_user', 'password': 'test_password'}),
                                           headers={'Content-type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicated_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(400, response.status_code, 'Request status code do not met expected.')
                self.assertDictEqual({'message': 'A user already exists'},
                                 json.loads(response.data),
                                 "Request response message do not correspond to expected response message.")
