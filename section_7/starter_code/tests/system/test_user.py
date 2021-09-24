
from section_7.starter_code.models.user import UserModel
import json
from section_7.starter_code.tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(201, request.status_code, 'Request status code do not met expected.')
                self.assertIsNotNone(UserModel.find_by_username('test_user'), "User was not saved to DB.")
                self.assertEqual({'message': 'User was created successfully'},
                                 json.loads(request.data),
                                 "Request response message do not correspond to expected response message.")

                request2 = client.post('/register', data={'username': 'test_user', 'password': 'test_password'})

                self.assertEqual(400, request2.status_code, 'Request status code do not met expected.')
                self.assertEqual({'message': 'A user already exists'},
                                 json.loads(request2.data),
                                 "Request response message do not correspond to expected response message.")

    def test_register_login(self):
        pass

    def test_register_duplicated_user(self):
        pass
