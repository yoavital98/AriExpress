import unittest
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects.Member import Member


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        # TODO: check implementations of tests
        self.store_facade = StoreFacade()
        self.member1 = Member("John", "password123", "john.doe@example.com")
        self.store_facade.members["John"] = self.member1
        self.member2 = Member("Jane", "password456", "jane.doe@example.com")
        self.store_facade.members["Jane"] = self.member2
        # self.store = Store("Store1")
        # self.store_facade.stores["Store1"] = self.store

    def test_getStores_returnsStores_empty(self):
        self.assertEqual(self.store_facade.getStores(), [])

    def test_getStores_returnsStores_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.getStores(), [self.store])
    
    def test_getStores_returnsStores_single1(self):  # duplicate test, might need to delete
        stores = self.store_facade.getStores()
        self.assertIsInstance(stores, list)
        self.assertGreater(len(stores), 0)
        for store in stores:
            self.assertIsInstance(store, Store)

    def test_getStores_returnsStores_multiple(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.store2 = Store("Store2")
        self.store_facade.stores["Store2"] = self.store2
        self.assertEqual(self.store_facade.getStores(), [self.store, self.store2])

    def test_getProductsByStore_returnsProducts_empty(self):
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), [])

    def test_getProductsByStore_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), [self.product])
    
    def test_getProductsByStore_returnsProducts_multiple(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.product2 = self.store.addProduct("Product2", 10, 10)
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), [self.product, self.product2])

    def test_getProduct_returnsProduct_found(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.getProduct("Store1", "Product1"), self.product)
    
    def test_getProduct_returnsProduct_notFound(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.getProduct("Store1", "Product2"), None)

    def test_productSearchByName_returnsProducts_empty(self):
        self.assertEqual(self.store_facade.productSearchByName("Product1"), [])
    
    def test_productSearchByName_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.productSearchByName("Product1"), [self.product])
    
    def test_productSearchByName_returnsProducts_multiple(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.product2 = self.store.addProduct("Product2", 10, 10)
        self.assertEqual(self.store_facade.productSearchByName("Product1"), [self.product])

    def test_productSearchByCategory_returnsProducts_empty(self):
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), [])
    
    def test_productSearchByCategory_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), [self.product])
    
    def test_productSearchByCategory_returnsProducts_multipleProducts(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1")
        self.product2 = self.store.addProduct("Product2", 10, 10, "Category1")
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), [self.product, self.product2])
    
    def test_productSearchByCategory_returnsProducts_multipleCategories(self):
        # TODO: should be only 1 category with the same name so assert fail
        # self.store = Store("Store1")
        # self.store_facade.stores["Store1"] = self.store
        # self.product = self.store.addProduct("Product1", 10, 10, "Category1")
        # self.product2 = self.store.addProduct("Product2", 10, 10, "Category2")
        # self.assertEqual(self.store_facade.productSearchByCategory("Category1"), [self.product])
        pass


    # ------------------------- Keyword: like name but can be in desc -------------------------

    def test_productSearchByKeyword_returnsProducts_empty(self):
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [])
    
    def test_productSearchByKeyword_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1", "Keyword1")
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [self.product])
    
    def test_productSearchByKeyword_returnsProducts_multipleProducts(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1", "Keyword1")
        self.product2 = self.store.addProduct("Product2", 10, 10, "Category1", "Keyword1")
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [self.product, self.product2])
    
    # ----------------------------------------------------------------------------------------

    def test_productFilterByFeatures_returnsProducts_empty(self):
        self.assertEqual(self.store_facade.productFilterByFeatures("Category1", "Keyword1"), [])
    
    def test_productFilterByFeatures_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1", "Keyword1")
        self.assertEqual(self.store_facade.productFilterByFeatures("Category1", "Keyword1"), [self.product])
    
    def test_productFilterByFeatures_returnsProducts_multipleProducts(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10, "Category1", "Keyword1")
        self.product2 = self.store.addProduct("Product2", 10, 10, "Category1", "Keyword1")
        self.assertEqual(self.store_facade.productFilterByFeatures("Category1", "Keyword1"), [self.product, self.product2])
    
    def test_placeBid_returnsTrue(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.placeBid("Store1", "Product1", 10), True)
    
    def test_placeBid_badStore_returnsFalse(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.placeBid("Store2", "Product1", 10), False)
    
    def test_placeBid_badProduct_returnsFalse(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.placeBid("Store1", "Product2", 10), False)
    
    def test_placeBid_badPrice_returnsFalse(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.assertEqual(self.store_facade.placeBid("Store1", "Product1", 9), False)
    
    def test_placeBid_badProductPurchasePolicy_returnsFalse(self):
        pass

    def test_getStorePurchaseHistory_returnsHistory_empty(self):
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [])
    
    def test_getStorePurchaseHistory_returnsHistory_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.store_facade.placeBid("Store1", "Product1", 10)
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [self.product])

    def test_getStorePurchaseHistory_returnsHistory_multiple(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.product = self.store.addProduct("Product1", 10, 10)
        self.product2 = self.store.addProduct("Product2", 10, 10)
        self.store_facade.placeBid("Store1", "Product1", 10)
        self.store_facade.placeBid("Store1", "Product2", 10)
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [self.product, self.product2])
    
    def test_getStorePurchaseHistory_badStore_returnsEmpty(self):
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store2"), [])
    


if __name__ == '__main__':
    unittest.main()
