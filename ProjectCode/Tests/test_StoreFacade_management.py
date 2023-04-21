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
    
    def test_openStore_userNotLoggedIn_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_openStore_storeAlreadyExists_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.openStore("Store1", "John")
        self.assertTrue(self.store_facade.stores.keys().__contains__("Store1"))
        self.assertEqual(len(self.store_facade.stores), 1)
    
    def test_addNewProductToStore_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_userNotLoggedIn_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_storeDoesNotExist_failure(self):
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_addNewProductToStore_userIsNotFounder_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "Jane", "Product1", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_userIsNotOwner_failure(self):
        pass

    def test_addNewProductToStore_productAlreadyExists_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
        self.assertEqual(len(self.store_facade.stores["Store1"].products), 1)

    def test_addNewProductToStore_productNameIsEmpty_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "", 10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__(""))
    
    def test_addNewProductToStore_productPriceIsNegative_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", -10, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_productPriceIsZero_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 0, 10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_addNewProductToStore_productQuantityIsNegative_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, -10)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productQuantityIsZero_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 0)
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productCategoryIsEmpty_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10, "")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_addNewProductToStore_productCategoryDoesNotExist_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10, "Category1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_userNotLoggedIn_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_storeDoesNotExist_failure(self):
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_removeProductFromStore_userIsNotOwner_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "Jane", "Product1")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))

    def test_removeProductFromStore_userIsNotFounder_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.deleteProductFromStore("Store1", "Jane", "Product1")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    def test_removeProductFromStore_productDoesNotExist_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.deleteProductFromStore("Store1", "John", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__("Product1"))
    
    # ------------------------------ Edit Product ------------------------------

    def test_editProductOfStore_price_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 20)
    
    def test_editProductOfStore_price_negativePrice_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product1", -20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_price_zeroPrice_failure(self):
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
        
    def test_editProductOfStore_name_emptyName_failure(self):
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
        
    def test_editProductOfStore_quantity_negativeQuantity_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductQuantity("Store1", "John", "Product1", -20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].quantity, 10)
    
    def test_editProductOfStore_quantity_zeroQuantity_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductQuantity("Store1", "John", "Product1", 0)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].quantity, 10)
    
    def test_editProductOfStore_category_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "Category1")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "Category1")
    
    def test_editProductOfStore_category_emptyCategory_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "None")
    
    def test_editProductOfStore_category_categoryDoesNotExist_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductCategory("Store1", "John", "Product1", "Category1")
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].category, "None")
    
    def test_editProductOfStore_usernameNotOwner_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "Jack", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)

    def test_editProductOfStore_usernameNotFounder_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "Jack", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_storeDoesNotExist_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store2", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_productDoesNotExist_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.changeProductPrice("Store1", "John", "Product2", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_editProductOfStore_storeNotOpen_failure(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.addNewProductToStore("Store1", "John", "Product1", 10, 10)
        self.store_facade.closeStore("Store1", "John")
        self.store_facade.changeProductPrice("Store1", "John", "Product1", 20)
        self.assertEqual(self.store_facade.stores["Store1"].products["Product1"].price, 10)
    
    def test_nominateStoreOwner_success(self):
        self.store_facade.openStore("Store1", "John")
        self.store_facade.nominateStoreOwner("Store1", "John", "Jack")
        self.assertTrue(self.store_facade.stores["Store1"].owners.__contains__("Jack"))
    
    def test_nominateStoreOwner_requesterNotOwner_failure(self):
        pass

    def test_nominateStoreOwner_requesterNotFounder_failure(self):
        pass

    def test_nominateStoreOwner_storeDoesNotExist_failure(self):
        pass

    def test_nominateStoreOwner_storeNotOpen_failure(self):
        pass

    def test_nominateStoreOwner_nominatedUserAlreadyOwner_failure(self):
        pass

    def test_nominateStoreOwner_nominatedUserAlreadyFounder_failure(self):
        pass

    def test_nominateStoreOwner_requesterNotLoggedIn_failure(self):
        pass

    # ------------------------------------------------------------------------

    def test_nominateStoreManager_success(self):
        pass

    def test_nominateStoreManager_requesterNotOwner_failure(self):
        pass

    def test_nominateStoreManager_requesterNotFounder_failure(self):
        pass

    def test_nominateStoreManager_storeDoesNotExist_failure(self):
        pass

    def test_nominateStoreManager_storeNotOpen_failure(self):
        pass

    def test_nominateStoreManager_nominatedUserAlreadyOwner_failure(self):
        pass

    def test_nominateStoreManager_nominatedUserAlreadyFounder_failure(self):
        pass

    def test_nominateStoreManager_nominatedUserAlreadyManager_failure(self):
        pass

    def test_nominateStoreManager_requesterNotLoggedIn_failure(self):
        pass

    def test_addPermissionsForManager_success(self):
        pass

    def test_addPermissionsForManager_requesterNotFounder_failure(self):
        pass

    def test_addPermissionsForManager_storeDoesNotExist_failure(self):
        pass

    def test_addPermissionsForManager_storeNotOpen_failure(self):
        pass

    def test_editPermissionsForManager_success(self):
        pass

    def test_closeStore_success(self):
        pass

    def test_closeStore_requesterNotFounder_failure(self):  
        pass

    def test_closeStore_storeDoesNotExist_failure(self):
        pass

    def test_closeStore_storeNotOpen_failure(self):
        pass

    def test_closeStore_requesterNotLoggedIn_failure(self):
        pass

    def test_getStaffInfo_success(self):
        pass

    def test_getStaffInfo_storeDoesNotExist_failure(self):
        pass

    def test_getStaffInfo_storeNotOpen_failure(self):
        pass

    def test_getStaffInfo_requesterNotLoggedIn_failure(self):
        pass

    def test_getStaffInfo_requesterNotOwner_failure(self):
        pass

    def test_getStaffInfo_requesterNotFounder_failure(self):
        pass

    def test_getStoreManagerPermissions_noManagers_success(self):
        pass

    def test_getStoreManagerPermissions_oneManager_success(self):
        pass

    def test_getStoreManagerPermissions_multipleManagers_success(self):
        pass

    def test_getStoreManagerPermissions_storeDoesNotExist_failure(self):
        pass

    def test_getStoreManagerPermissions_storeNotOpen_failure(self):
        pass

    def test_getStoreManagerPermissions_requesterNotLoggedIn_failure(self):
        pass

    def test_getStoreManagerPermissions_requesterNotOwner_failure(self):
        pass

    def test_getStoreManagerPermissions_requesterNotFounder_failure(self):
        pass











if __name__ == '__main__':
    unittest.main()
