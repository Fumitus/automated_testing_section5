from section_7.starter_code.tests.unit.unit_base_test import UnitBaseTest
from section_7.starter_code.models.user import UserModel


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test', 'password')

        self.assertEqual('Test', user.username,
                         "Username after creation do not correspond constructor elements.")
        self.assertEqual('password', user.password,
                         "User password after creation do not correspond constructor elements.")
