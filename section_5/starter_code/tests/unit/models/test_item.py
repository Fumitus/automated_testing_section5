from unittest import TestCase

from section_5.starter_code.models.item import ItemModel


class ItemTest(TestCase):
    def test_create_item(self):
        i = ItemModel('Test', 19.56)

        self.assertEqual('Test', i.name,
                         'The item name after creation do not represent constructor argument.')
        self.assertEqual(19.56, i.price,
                         'The item price after creation do not represent constructor argument.')

    def test_item_json(self):
        i = ItemModel('Test', 19.56)
        expected = {'name': 'Test', 'price': 19.56}

        self.assertEqual(expected, i.json(),
                         'The json after creation do not represent constructor argument.')
