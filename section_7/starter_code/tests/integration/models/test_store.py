from section_6.starter_code.models.item import ItemModel
from section_6.starter_code.models.store import StoreModel
from section_6.starter_code.tests.integration.integration_base_test import BaseTest


class StoreTest(BaseTest):
    def test_store_item_is_empty(self):
        store = StoreModel('test')

        self.assertEqual([], store.items.all(),
                         "List length was not equal to 0 even no items was added.")

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'name': 'test',
            'items': []
        }
        self.assertDictEqual(expected, store.json())

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected_2 = {
                'name': 'test',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }

            self.assertDictEqual(expected_2, store.json())

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Store list was not empty even no items was added.")

            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                 "Store list empty. save_to_db() not worked.")

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test'),
                              "Store list was not empty. delete_from_db() not worked.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(1, store.items.count())
            self.assertEqual('test_item', store.items.first().name)
