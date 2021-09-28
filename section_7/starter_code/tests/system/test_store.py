import section_7.starter_code.models.store
from section_7.starter_code.models.store import StoreModel
from section_7.starter_code.tests.base_test import BaseTest
import json
from section_7.starter_code.models.item import ItemModel
from unittest.mock import patch
from section_7.starter_code import app


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test_store')

                self.assertEqual(201, response.status_code, 'Response code do not met specified one.')
                self.assertIsNotNone(StoreModel.find_by_name('test_store'), 'Store was not saved to DB.')
                self.assertDictEqual({'name': 'test_store', 'items': []}, json.loads(response.data))

    def test_error_occur_creating_store(self):
        with patch('section_7.starter_code.models.store.StoreModel.save_to_db') as mocked_save_to_db:
            mocked_save_to_db.side_effect = Exception
            with self.app() as client:
                with self.app_context():
                    # need code to simulate Exception and get code 500
                    response = client.post('/store/test_store')

                    self.assertEqual(500, response.status_code, 'Response code do not met specified one.')
                    self.assertDictEqual({"message": "An error occurred creating the store."},
                                         json.loads(response.data))
                    self.assertIsNone(StoreModel.find_by_name('test_store'), 'Store was saved to DB.')

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test_store'))

                client.post('/store/test_store')
                response = client.post('/store/test_store')

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': 'A store with name "test_store" already exists.'},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                store = StoreModel('test_store')

                self.assertIsNone(StoreModel.find_by_name('test_store'))

                store.save_to_db()

                self.assertIsNotNone(StoreModel.find_by_name('test_store'))

                response = client.delete('/store/test_store')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))
                self.assertIsNone(StoreModel.find_by_name('test_store'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')

                response = client.get('/store/test_store')

                self.assertEqual(200, response.status_code)
                self.assertIsNotNone(StoreModel.find_by_name('test_store'))
                self.assertDictEqual({'name': 'test_store', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test_store')

                self.assertEqual(404, response.status_code)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')

                item = ItemModel('test_item', 19.99, 1)
                item.save_to_db()

                response = client.get('/store/test_store')

                self.assertEqual(200, response.status_code)
                self.assertDictEqual({'name': 'test_store', 'items': [{'name': 'test_item', 'price': 19.99}]
                                      }, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                self.assertIsNone(StoreModel.find_by_name('test_store'))
                self.assertIsNone(StoreModel.find_by_name('test_store_2'))

                response = client.get('/stores')

                self.assertDictEqual(json.loads(response.data), {'stores': []})

                client.post('/store/test_store')
                client.post('/store/test_store_2')

                response_2 = client.get('/stores')

                self.assertIsNotNone(StoreModel.find_by_name('test_store'))
                self.assertIsNotNone(StoreModel.find_by_name('test_store_2'))
                self.assertDictEqual(json.loads(response_2.data), {'stores': [{'name': 'test_store', 'items': []},
                                                                              {'name': 'test_store_2', 'items': []}
                                                                              ]
                                                                   }
                                     )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test_store')

                item = ItemModel('test_item', 19.99, 1)
                item.save_to_db()

                response = client.get('/stores')
                self.assertDictEqual(json.loads(response.data), {'stores': [{'name': 'test_store',
                                                                             'items': [{'name': 'test_item',
                                                                                        'price': 19.99}]}]})
