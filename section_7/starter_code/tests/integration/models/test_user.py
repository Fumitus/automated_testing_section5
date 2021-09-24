from section_7.starter_code.tests.integration.integration_base_test import BaseTest
from section_7.starter_code.models.user import UserModel


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test_user', 'test_password')

            self.assertIsNone(UserModel.find_by_username('test_user'),
                              "username found in DB but it was not created yet.")
            self.assertIsNone(UserModel.find_by_id(1),
                              "user by ID found in DB but it was not created yet.")

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('test_user'),
                                 "User was not saved to DB. save_to_db() do not worked")
            self.assertIsNotNone(UserModel.find_by_id(1),
                                 "user ID in DB do not correspond.")
