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

        # self.member1 = Member("John", "password123", "john.doe@example.com")
        # self.store_facade.members["John"] = self.member1
        # self.member2 = Member("Jane", "password456", "jane.doe@example.com")
        # self.store_facade.members["Jane"] = self.member2
        # self.store = Store("Store1")
        # self.store_facade.stores["Store1"] = self.store

    def test_openStore_success(self):
        self.store_facade.openStore("Store1", "John")
        self.assertTrue(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_openStore_userNotLoggedIn_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_openStore_storeAlreadyExists_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.openStore("Store1", "John")
        self.assertTrue(self.store_facade.stores.keys().__contains__("Store1"))
        self.assertEqual(len(self.store_facade.stores), 1)
    
    def test_addNewProductToStore_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_userNotLoggedIn_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_storeDoesNotExist_fail(self):
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_addNewProductToStore_userIsNotFounder_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "Jane", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_userIsNotOwner_fail(self):
        pass

    def test_addNewProductToStore_productAlreadyExists_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
        self.assertEqual(len(self.store_facade.stores["Store1"].products), 1)

    def test_addNewProductToStore_productNameIsEmpty_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__(""))
    
    def test_addNewProductToStore_productPriceIsNegative_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", -10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_productPriceIsZero_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 0, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_productQuantityIsNegative_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, -10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productQuantityIsZero_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 0)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productCategoryIsEmpty_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10, "")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productCategoryDoesNotExist_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10, "Category1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_userNotLoggedIn_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_storeDoesNotExist_fail(self):
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_removeProductFromStore_userIsNotOwner_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "Jane", "Product1")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_removeProductFromStore_userIsNotFounder_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "Jane", "Product1")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_productDoesNotExist_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    # ------------------------------ Edit Product ------------------------------

    def test_editProductOfStore_price_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 20)
    
    def test_editProductOfStore_price_negativePrice_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product1", -20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_price_zeroPrice_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product1", 0)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)

    def test_editProductOfStore_name_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductName("Store1", "John", "Product1", "Product2")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product2"))
        
    def test_editProductOfStore_name_emptyName_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductName("Store1", "John", "Product1", "")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product2"))

    def test_editProductOfStore_quantity_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductQuantity("Store1", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].quantity, 20)
        
    def test_editProductOfStore_quantity_negativeQuantity_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductQuantity("Store1", "John", "Product1", -20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].quantity, 10)
    
    def test_editProductOfStore_quantity_zeroQuantity_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductQuantity("Store1", "John", "Product1", 0)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].quantity, 10)
    
    def test_editProductOfStore_category_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "Category1")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "Category1")
    
    def test_editProductOfStore_category_emptyCategory_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "None")
    
    def test_editProductOfStore_category_categoryDoesNotExist_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "Category1")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "None")
    
    def test_editProductOfStore_usernameNotOwner_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "Jack", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)

    def test_editProductOfStore_usernameNotFounder_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "Jack", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_storeDoesNotExist_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store2", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_productDoesNotExist_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product2", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_storeNotOpen_fail(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.closeStore("Store1", "John")
        self.store_facade.changeProductPrice("Store1", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    



    









if __name__ == '__main__':
    unittest.main()
