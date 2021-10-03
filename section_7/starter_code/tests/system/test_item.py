from section_7.starter_code.models.item import ItemModel
from section_7.starter_code.models.store import StoreModel
from section_7.starter_code.models.user import UserModel
from section_7.starter_code.tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(401, resp.status_code,
                                 'Expected response code do not met specified.')
                self.assertDictEqual({'message': "Did you include a valid Authorization header?"},
                                     json.loads(resp.data), 'Response message do not met specified one.')

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(404, resp.status_code, 'Expected response code do not met specified.')
                self.assertDictEqual({'message': 'Item not found'}, json.loads(resp.data),
                                     'Response message do not met specified one.')

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})
                self.assertEqual(200, resp.status_code, 'Expected response code do not met specified.')
                self.assertDictEqual({'name': 'test_item', 'price': 17.99}, json.loads(resp.data),
                                     'Response message do not met specified one.')

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})
                self.assertEqual(200, resp.status_code, 'Item was not added to DB before delete_item() will run.')
                self.assertDictEqual({'name': 'test_item', 'price': 17.99}, json.loads(resp.data),
                                     'Item was not added to DB before delete_item() will run.')
                resp = client.delete('/item/test_item')

                self.assertEqual(200, resp.status_code)
                self.assertIsNone(ItemModel.find_by_name('test_item'), 'Item was not deleted from DB.')
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(201, resp.status_code)
                self.assertDictEqual({'name': 'test_item', 'price': 17.99}, json.loads(resp.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(400, resp.status_code)
                self.assertDictEqual({'message': "An item with name 'test_item' already exists."},
                                     json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.put('/item/test_item', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(200, resp.status_code,
                                 'Response code do not met specified one.')
                self.assertDictEqual({'name': 'test_item', 'price': 17.99}, json.loads(resp.data),
                                     'Response message do not met specified one.')

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99,
                                 'test_item was not added to DB before test.')

                resp = client.put('/item/test_item', data={'price': 20.00, 'store_id': 1})

                self.assertEqual(200, resp.status_code,
                                 'Response code do not met specified one.')
                self.assertDictEqual({'name': 'test_item', 'price': 20.00}, json.loads(resp.data),
                                     'Response message do not met specified one.')

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertEqual(200, resp.status_code)
                self.assertDictEqual({'items': [{'name': 'test_item', 'price': 17.99}]}, json.loads(resp.data))
