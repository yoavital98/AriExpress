import unittest
from typing import List
from unittest import TestCase

from ProjectCode.Domain.StoreFacade import StoreFacade
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        # TODO: check implementations of tests
        self.store_facade = StoreFacade()
        self.member1 = Member("Ari", "password123", "ari@gmail.com")
        self.store_facade.members["Ari"] = self.member1


    def test_getStores_returnsStores_empty(self):
        self.stores = TypedDict(str, Store)
        self.assertEqual(self.store_facade.getStores(), self.stores)

    def test_getStores_returnsStores_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.stores = TypedDict(str, Store)
        self.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.getStores(), self.stores)
    
    # def test_getStores_returnsStores_single1(self):  # duplicate test, might need to delete
    #     stores = self.store_facade.getStores()
    #     self.assertIsInstance(stores, list)
    #     self.assertGreater(len(stores), 0)
    #     for store in stores:
    #         self.assertIsInstance(store, Store)

    def test_getStores_returnsStores_multiple(self):
        self.stores = TypedDict(str, Store)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.store2 = Store("Store2")
        self.store_facade.stores["Store2"] = self.store2
        self.stores["Store1"] = self.store
        self.stores["Store2"] = self.store2
        self.assertEqual(self.store_facade.getStores(), self.stores)

    def test_getProductsByStore_returnsProducts_empty(self):
        self.products = TypedDict(int, Product)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), self.products)

    def test_getProductsByStore_returnsProducts_single(self):
        self.products = TypedDict(int, Product)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "category1")
        self.products[self.product.product_id] = self.product
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), self.products)
    
    def test_getProductsByStore_returnsProducts_multiple(self):
        self.products = TypedDict(int, Product)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product1", 10, 10, "category1")
        self.product2 = self.store.addProduct(self.access, "Product2", 10, 10, "category1")
        self.products[self.product1.product_id] = self.product1
        self.products[self.product2.product_id] = self.product2
        self.assertEqual(self.store_facade.getProductsByStore("Store1"), self.products)

    def test_getProductsByStore_storeNotFound(self):
        with self.assertRaises(Exception) as context:
            self.store_facade.getProductsByStore("Store1")
        self.assertTrue("No such store exists" in str(context.exception))

    def test_getProduct_returnsProduct_notFound(self):
        self.products = TypedDict(int, Product)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "category1")
        self.assertEqual(self.store_facade.getProduct("Store1", "Product2"), self.products)

    def test_getProduct_returnsProduct_found(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "category1")
        self.assertEqual(self.store_facade.getProduct("Store1", "Product1"), self.product)

    def test_productSearchByName_returnsProducts_empty(self):
        self.products = TypedDict(int, Product)
        self.assertEqual(self.store_facade.productSearchByName("Product1"), self.products)

    def test_productSearchByName_returnsProducts_single(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "category1")
        self.returnedList = self.store_facade.productSearchByName("Product1")
        newlist: List[Product] = list()
        newlist.append(self.product)
        self.products[self.store] = newlist
        self.assertEqual(self.returnedList, self.products)
    
    def test_productSearchByName_returnsProducts_multiple(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product123", 10, 10, "category1")
        self.product2 = self.store.addProduct(self.access, "Product145", 10, 10, "category1")
        newlist: List[Product] = list()
        newlist.append(self.product1)
        newlist.append(self.product2)
        self.products[self.store] = newlist
        self.assertEqual(self.store_facade.productSearchByName("Product1"), self.products)

    def test_productSearchByCategory_returnsProducts_empty(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), self.products)
    
    def test_productSearchByCategory_returnsProducts_single(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        newlist: List[Product] = list()
        newlist.append(self.product)
        self.products[self.store] = newlist
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), self.products)
    
    def test_productSearchByCategory_returnsProducts_multipleProducts(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product123", 10, 10, "Category1")
        self.product2 = self.store.addProduct(self.access, "Product145", 10, 10, "Category1")
        newlist: List[Product] = list()
        newlist.append(self.product1)
        newlist.append(self.product2)
        self.products[self.store] = newlist
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), self.products)
    
    def test_productSearchByCategory_returnsProducts_multipleCategories(self):
        self.products = TypedDict(Store, list)
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product123", 10, 10, "Category1")
        self.product2 = self.store.addProduct(self.access, "Product145", 10, 10, "Category2")
        newlist: List[Product] = list()
        newlist.append(self.product1)
        self.products[self.store] = newlist
        self.assertEqual(self.store_facade.productSearchByCategory("Category1"), self.products)


    # ------------------------- Keyword: like name but can be in desc -------------------------
    # TODO: turn off those tests, there is no product description and features for now

    def test_productSearchByKeyword_returnsProducts_empty(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [])
    
    def test_productSearchByKeyword_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        # add description to product
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [self.product])
    
    def test_productSearchByKeyword_returnsProducts_multipleProducts(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product123", 10, 10, "Category1")
        self.product2 = self.store.addProduct(self.access, "Product145", 10, 10, "Category2")
        # add description to products
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), [self.product, self.product2])
    
    def test_productFilterByFeatures_returnsProducts_empty(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.productFilterByFeatures({"Category1": "Keyword1"}), [])
    
    def test_productFilterByFeatures_returnsProducts_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        # add feature to product
        self.assertEqual(self.store_facade.productFilterByFeatures({"Category1": "Keyword1"}), [self.product])
    
    def test_productFilterByFeatures_returnsProducts_multipleProducts(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product123", 10, 10, "Category1")
        self.product2 = self.store.addProduct(self.access, "Product145", 10, 10, "Category2")
        # add features to products
        self.assertEqual(self.store_facade.productFilterByFeatures({"Category1": "Keyword1"}), [self.product, self.product2])
    
    # ----------------------------------------------------------------------------------------

    def test_placeBid_success(self):
        self.member1.logInAsMember()
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.placeBid("Ari", "Store1", 20, self.product.product_id, 5), True)
        #username, storename, offer, productID, quantity
    
    def test_placeBid_badStore_failure(self):
        self.member1.logInAsMember()
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.placeBid("Ari", "Store2", 20, self.product.product_id, 5), False)
    
    def test_placeBid_badProduct_failure(self):
        self.member1.logInAsMember()
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.placeBid("Ari", "Store1", 20, self.product.product_id+1, 5), False)
    
    def test_placeBid_badPrice_failure(self):
        self.member1.logInAsMember()
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.placeBid("Ari", "Store1", 5, self.product.product_id+1, 5), False)

    # ---------------------- Not implemented yet ----------------------
    def test_placeBid_badProductPurchasePolicy_failure(self):
        pass

    def test_getStorePurchaseHistory_returnsHistory_empty(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [])
    
    def test_getStorePurchaseHistory_returnsHistory_single(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.store_facade.placeBid("Store1", "Product1", 10)
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [self.product])

    def test_getStorePurchaseHistory_returnsHistory_multiple(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product1 = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.product2 = self.store.addProduct(self.access, "Product2", 10, 10, "Category1")
        self.store_facade.placeBid("Store1", "Product1", 10)
        self.store_facade.placeBid("Store1", "Product2", 10)
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store1"), [self.product1, self.product2])
    
    def test_getStorePurchaseHistory_badStore_returnsEmpty(self):
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.assertEqual(self.store_facade.getStorePurchaseHistory("Store2"), [])
    


if __name__ == '__main__':
    unittest.main()
