from section_5.starter_code.models.item import ItemModel
from section_5.starter_code.tests.base_test import BaseTest


class TestItem(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel('Test', 18.56)

            # Make sure item is not in the database before save_to_db() is run
            self.assertIsNone(item.find_by_name('Test'))

            item.save_to_db()

            self.assertIsNotNone(item.find_by_name('Test'),
                                 "Item with specified name was not created in database.")

            item.delete_from_db()
            # Make sure item was deleted from the database after test
            self.assertIsNone(item.find_by_name('Test'),
                              "Item with specified name was not deleted from database with method detele_from_db().")
