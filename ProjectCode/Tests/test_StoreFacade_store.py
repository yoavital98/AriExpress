import unittest
from typing import List
from unittest import TestCase

from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
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
        self.store_facade.register("Ari", "password123", "ari@gmail.com")
        self.store_facade.register("Jane", "password456", "jane.doe@example.com")
        self.member1: Member = self.store_facade.members.get("Ari")
        self.member2: Member = self.store_facade.members.get("Jane")
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store1")
        self.store1: Store = self.store_facade.stores.get("Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "paper", 10, 500, "paper")
        self.item_paper: Product = self.store1.getProductById(1, "Ari")
        self.store_facade.logOut("Ari")


    def test_getStores_returnsStores_single(self):
        self.assertTrue(len(self.store_facade.getStores().values()) == 1)
        list_of_stores: list = list(self.store_facade.getStores().values())
        self.assertTrue(list_of_stores[0] == self.store1)

    # def test_getStores_returnsStores_single1(self):  # duplicate test, might need to delete
    #     stores = self.store_facade.getStores()
    #     self.assertIsInstance(stores, list)
    #     self.assertGreater(len(stores), 0)
    #     for store in stores:
    #         self.assertIsInstance(store, Store)


    def test_Orm_to_delete(self):
        self.store1.testing_orm()
    def test_getStores_returnsStores_multiple(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store2")
        store2: Store = self.store_facade.stores.get("Store2")
        self.assertTrue(len(self.store_facade.getStores().values()) == 2)
        list_of_stores: list = list(self.store_facade.getStores().values())
        self.assertTrue(list_of_stores[0] == self.store1)
        self.assertTrue(list_of_stores[1] == store2)

    def test_getProductsByStore_removeProductFromStore_empty(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.removeProductFromStore("Ari", "Store1", 1)
        self.assertEqual(self.store_facade.getProductsByStore("Store1", "Ari"), {})

    def test_getProductsByStore_returnsProducts_single(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.assertTrue(len(self.store_facade.getProductsByStore("Store1", "Ari")) == 1)


    def test_getProductsByStore_returnsProducts_multiple(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.addNewProductToStore("Ari", "Store1", "paper2", 10, 500, "paper")
        self.assertTrue(len(self.store_facade.getProductsByStore("Store1", "Ari")) == 2)


    def test_getProductsByStore_storeNotFoundOrNotAvailable(self):
        self.store_facade.logInAsMember("Ari", "password123")
        with self.assertRaises(Exception) as context:
            self.store_facade.getProductsByStore("Store2", "Ari")

    def test_getProduct_returnsProduct_notFound(self):
        with self.assertRaises(Exception):
            self.store_facade.getProduct("Store1", 4, "Ari")

    def test_getProduct_returnsProduct_found(self):
        self.store_facade.logInAsMember("Ari", "password123")
        product: Product = self.store_facade.getProduct("Store1", 1, "Ari")
        self.assertTrue(product.get_product_id() == 1)

    def test_productSearchByName_returnsProducts_empty(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.assertEqual(list(self.store_facade.productSearchByName("some_product").values()), [])

    def test_productSearchByName_returnsProducts_single(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.assertEqual(self.store_facade.productSearchByName("paper").get("Store1"), [self.item_paper])
    
    def test_productSearchByName_returnsProducts_multiple(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store2")
        store2: Store = self.store_facade.stores.get("Store2")
        self.store_facade.addNewProductToStore("Ari", "Store2", "paper", 10, 500, "paper")
        item_paper2: Product = store2.getProductById(1, "Ari")
        dict_products: TypedDict = self.store_facade.productSearchByName("paper")
        self.assertEqual(dict_products.get(self.store1.get_store_name()), [self.item_paper])
        self.assertEqual(dict_products.get(store2.get_store_name()), [item_paper2])

    def test_productSearchByCategory_returnsProducts_single(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.assertTrue(len(list(self.store_facade.productSearchByCategory("paper").values())) == 1)

    
    def test_productSearchByCategory_returnsProducts_empty(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.removeProductFromStore(self.member1.get_username(), self.store1.get_store_name(), 1)
        self.assertTrue(len(list(self.store_facade.productSearchByCategory("paper").values())) == 0)
    def test_productSearchByCategory_returnsProducts_multipleProducts(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store2")
        store2: Store = self.store_facade.stores.get("Store2")
        self.store_facade.addNewProductToStore("Ari", "Store2", "paper", 10, 500, "paper")
        item_paper2: Product = store2.getProductById(1, "Ari")
        dict_products: TypedDict = self.store_facade.productSearchByCategory("paper")
        self.assertEqual(dict_products.get(self.store1.get_store_name()), [self.item_paper])
        self.assertEqual(dict_products.get(store2.get_store_name()), [item_paper2])
    
    def test_productSearchByCategory_returnsProducts_multipleCategories(self):
        self.products = TypedDict(Store, list)
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store2")
        store2: Store = self.store_facade.stores.get("Store2")
        self.store_facade.addNewProductToStore("Ari", "Store2", "paper", 10, 500, "paper1")
        item_paper2: Product = store2.getProductById(1, "Ari")
        dict_products: TypedDict = self.store_facade.productSearchByCategory("paper")
        self.assertEqual(dict_products.get(self.store1.get_store_name()), [self.item_paper])
        self.assertEqual(dict_products.get(store2.get_store_name()), [item_paper2])
        dict_products2: TypedDict = self.store_facade.productSearchByCategory("paper1")
        self.assertEqual(dict_products2.get(store2.get_store_name()), [item_paper2])

    # ------------------------- Keyword: like name but can be in desc -------------------------
    # TODO: turn off those tests, there is no product description and features for now

    def test_productSearchByKeyword_returnsProducts_empty(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.assertEqual(self.store_facade.productSearchByName("Keyword1"), {})
    

    

    
    def test_productFilterByFeatures_returnsProducts_empty(self):
        pass
        # TODO: amiel, features


    def test_productFilterByFeatures_returnsProducts_single(self):
        pass
        # TODO: amiel, features
    
    def test_productFilterByFeatures_returnsProducts_multipleProducts(self):
        pass
        # TODO: amiel, features

    
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
        self.store_facade.logInAsMember("Ari", "password123")
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store
        self.access = Access(self.store, self.member1)
        self.access.setFounder(True)
        self.store.get_accesses()[self.member1.get_username()] = self.access
        self.product = self.store.addProduct(self.access, "Product1", 10, 10, "Category1")
        self.assertEqual(self.store_facade.placeBid("Ari", "Store1", 5, self.product.product_id+1, 5), False)


    def test_addDiscount_success(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore(self.member1.get_username(), "Store1")
        self.store = self.store_facade.stores["Store1"]
        self.access = self.store.get_accesses()[self.member1.get_username()]
        self.product = self.store.addProduct(self.access, "Oreo", 10, 10, "Milk")
        self.discount = self.store.addDiscount("Simple", percent=10, level="Product", level_name=self.product.get_product_id())
        self.added_discount = self.store.getDiscount(1)
        self.assertEqual(self.discount, self.added_discount)


    def test_calculateSimpleDiscount_success(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore(self.member1.get_username(), "Store1")
        self.store = self.store_facade.stores["Store1"]
        self.access = self.store.get_accesses()[self.member1.get_username()]
        self.product = self.store.addProduct(self.access, "Oreo", 10, 10, "Milk")
        self.discount = self.store.addDiscount("Simple", percent=10, level="Product",
                                               level_name=self.product.get_product_id())
        self.product_dict = {self.product.get_product_id(): 1}
        self.price_after_discount = self.store.getProductPriceAfterDiscount(self.product, self.product_dict, 0)
        self.assertEqual(self.price_after_discount, 9)

    def test_calculateConditionedDiscount_success(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore(self.member1.get_username(), "Store1")
        self.store = self.store_facade.stores["Store1"]
        self.access = self.store.get_accesses()[self.member1.get_username()]
        self.product = self.store.addProduct(self.access, "Oreo", 10, 10, "Milk")
        self.product2 = self.store.addProduct(self.access, "Cariot", 10, 10, "Milk")
        self.sub_rule = {"rule_type": "amount_of_product", "product_id":self.product.get_product_id(),
                        "operator":">=", "quantity":1,"category":"", "child": {}}
        self.rule = {"rule_type": "amount_of_product", "product_id":self.product2.get_product_id(),
                     "operator":">=", "quantity":1,"category":"", "child": {"logic_type":"OR", "rule":self.sub_rule} }
        self.discount = self.store.addDiscount("Conditioned", percent=10, level="Product",
                                               level_name=self.product.get_product_id(), rule=self.rule)
        self.product_dict = {self.product.get_product_id(): 2, self.product2.get_product_id(): 2}
        self.price_after_discount_1 = self.store.getProductPriceAfterDiscount(self.product, self.product_dict, 0)
        self.assertEqual(9,self.price_after_discount_1)
    # ---------------------- Not implemented yet ----------------------
    def test_placeBid_badProductPurchasePolicy_failure(self):
        pass

    def test_getStorePurchaseHistory_returnsHistory_empty(self):
        transaction_history = TransactionHistory()
        self.assertTrue(self.store1.get_store_name() not in transaction_history.store_transactions.keys())



    
    def test_getStorePurchaseHistory_returnsHistory_single(self):
        transaction_history = TransactionHistory()
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.logInAsMember("Jane", "password456")
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 9)
        self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555",
                                       "some_address")
        transaction_list: list = self.store_facade.getStorePurchaseHistory(self.member1.get_username(), self.store1.get_store_name())
        self.assertTrue(len(transaction_list) == 1)
        transaction_history.clearAllHistory()




    def test_getStorePurchaseHistory_returnsHistory_multiple(self):
        transaction_history = TransactionHistory()
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.logInAsMember("Jane", "password456")
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 3)
        self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555",
                                       "some_address")
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 3)
        self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555",
                                       "some_address")
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 3)
        self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555",
                                       "some_address")
        transaction_list: list = transaction_history.get_Store_Transactions(self.store1.get_store_name())
        self.assertTrue(len(transaction_list) == 3)
        transaction_history.clearAllHistory()
    
    def test_getStorePurchaseHistory_badStore_returnsEmpty(self):
        self.store_facade.logInAsMember("Ari", "password123")
        transaction_history = TransactionHistory()
        with self.assertRaises(Exception):
           self.store_facade.getStorePurchaseHistory("Ari", "made_up_store")
    


if __name__ == '__main__':
    unittest.main()
