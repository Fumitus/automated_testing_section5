from section_6.starter_code.models.store import StoreModel
from section_6.starter_code.tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):
    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual('test', store.name,
                         'Store name after creation does not equal constructor argument.')
