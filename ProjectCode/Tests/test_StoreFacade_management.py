import unittest
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects.Member import Member


class TestStoreFacade(TestCase):

    def setUp(self):
        self.store_facade = StoreFacade()
        self.store_facade = StoreFacade()
        self.member1 = Member("Ari", "password123", "ari@gmail.com")
        self.store_facade.members["Ari"] = self.member1
        self.member2 = Member("Feliks", "password456", "feliks@gmail.com")
        self.store_facade.members["Feliks"] = self.member2
        self.member3 = Member("Amiel", "password789", "amiel@gmail.com")
        self.store_facade.members["Amiel"] = self.member3

    def test_openStore_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertTrue(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_openStore_userNotLoggedIn_failure(self):
        self.member1.logged_In = False
        self.store_facade.openStore("Ari", "Store1")
        self.assertFalse(self.store_facade.stores.keys().__contains__("Store1"))
    
    def test_openStore_storeAlreadyExists_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertTrue(self.store_facade.stores.keys().__contains__("Store1"))
        self.store_facade.openStore("Ari", "Store1")
        self.assertEqual(len(self.store_facade.stores), 1)
    
    def test_addNewProductToStore_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertTrue(self.store_facade.stores["Store1"].products.keys().__contains__(self.product.product_id))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id], self.product)

    def test_addNewProductToStore_userNotLoggedIn_failure(self):
        self.member1.logged_In = False
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1"))

    def test_addNewProductToStore_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Store2", "Ari", "Product1", 10, 10, "category1"))
    
    def test_addNewProductToStore_userIsNotFounder_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Store1", "Feliks", "Product1", 10, 10, "category1"))

    def test_addNewProductToStore_userIsNotOwner_failure(self):
        # TODO: add owner to store
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Store1", "Feliks", "Product1", 10, 10, "category1"))

    def test_addNewProductToStore_productAlreadyExists_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1"))

    def test_addNewProductToStore_productNameIsEmpty_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "", 10, 10, "category1"))
    
    def test_addNewProductToStore_productPriceIsNegative_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, -10, "category1"))

    def test_addNewProductToStore_productPriceIsZero_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 0, "category1"))


    def test_addNewProductToStore_productQuantityIsNegative_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", -10, 10, "category1"))

    def test_addNewProductToStore_productQuantityIsZero_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 0, 10, "category1"))

    def test_addNewProductToStore_productCategoryIsEmpty_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, ""))
    
    def test_addNewProductToStore_productCategoryDoesNotExist_failure(self):
        # TODO: make sure category doesn't exist
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1"))
    
    def test_removeProductFromStore_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.store_facade.removeProductFromStore("Ari", "Store1", "Product1")
        self.assertFalse(self.store_facade.stores["Store1"].products.keys().__contains__(self.product.product_id))

    def test_removeProductFromStore_userNotLoggedIn_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.member1.logged_In = False
        self.assertRaises(Exception, self.store_facade.removeProductFromStore("Ari", "Store1", self.product.product_id))
    
    def test_removeProductFromStore_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.assertRaises(Exception, self.store_facade.removeProductFromStore("Store2", "Ari", self.product.product_id))
    
    def test_removeProductFromStore_userIsNotOwner_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.member2.logged_In = True
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.assertRaises(Exception, self.store_facade.removeProductFromStore("Store1", "Feliks", self.product.product_id))

    def test_removeProductFromStore_userIsNotFounder_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.member3.logged_In = True
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10)
        self.assertRaises(Exception, self.store_facade.removeProductFromStore("Store1", "Amiel", self.product.product_id))
    
    def test_removeProductFromStore_productDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.removeProductFromStore("Ari", "Store1", "Product1"))

    # ------------------------------ Edit Product ------------------------------

    def test_editProductOfStore_price_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, price=20)
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 20)
    
    def test_editProductOfStore_price_negativePrice_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, price = -20))
    
    def test_editProductOfStore_price_zeroPrice_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, price = 0))

    def test_editProductOfStore_name_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, name="Product2")
        self.assertNotEqual(self.store_facade.stores["Store1"].products[self.product.product_id].name, "Product1")
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].name, "Product2")
        
    def test_editProductOfStore_name_emptyName_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, name=""))

    def test_editProductOfStore_quantity_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, quantity=20)
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].quantity, 20)
        
    def test_editProductOfStore_quantity_negativeQuantity_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, quantity = -20))
    
    def test_editProductOfStore_quantity_zeroQuantity_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.product = self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", self.product.product_id, quantity = 0))
    
    def test_editProductOfStore_category_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.store_facade.editProductOfStore("Ari", "Store1", "Product1", category="Category2")
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].category, "Category2")
    
    def test_editProductOfStore_category_emptyCategory_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", "Product1", category=""))
    
    def test_editProductOfStore_category_categoryDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        # TODO: make sure category does not exist
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", "Product1", category="Category2"))
    
    def test_editProductOfStore_usernameNotOwner_failure(self):
        self.member1.logged_In = True
        self.member2.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Store1", "Feliks", "Product1", price=20))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 10)

    def test_editProductOfStore_usernameNotFounder_failure(self):
        self.member1.logged_In = True
        self.member3.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Store1", "Amiel", "Product1", price=20))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 10)
    
    def test_editProductOfStore_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store2", "Product1", price=20))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 10)

    def test_editProductOfStore_productDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", "Product2", price=20))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 10)
    
    def test_editProductOfStore_storeNotOpen_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.addNewProductToStore("Ari", "Store1", "Product1", 10, 10, "Category1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.editProductOfStore("Ari", "Store1", "Product1", 20))
        self.assertEqual(self.store_facade.stores["Store1"].products[self.product.product_id].price, 10)
    
    def test_nominateStoreOwner_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreOwner("Ari", "Feliks","Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isOwner)
    
    def test_nominateStoreOwner_requesterNotOwner_failure(self):
        self.member1.logged_In = True
        self.member2.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Feliks", "Amiel", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Amiel")) #TODO: check if works

    def test_nominateStoreOwner_requesterNotFounder_failure(self):
        self.member1.logged_In = True
        self.member3.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Amiel", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreOwner_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store2"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreOwner_storeNotOpen_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreOwner_nominatedUserAlreadyOwner_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isOwner)
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1"))
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isOwner)

    def test_nominateStoreOwner_nominatedUserAlreadyFounder_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Ari"].isFounder)
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Ari", "Ari", "Store1"))

    def test_nominateStoreOwner_requesterNotLoggedIn_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.member1.logged_In = False
        self.assertRaises(Exception, self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    # ------------------------------------------------------------------------

    def test_nominateStoreManager_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreManager("Ari", "Feliks","Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isManager)

    def test_nominateStoreManager_requesterNotOwner_failure(self):  # not sure we need this test
        self.member1.logged_In = True
        self.member2.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Feliks", "Amiel", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Amiel"))

    def test_nominateStoreManager_requesterNotFounder_failure(self):
        self.member1.logged_In = True
        self.member3.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Amiel", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreManager_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Feliks", "Store2"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreManager_storeNotOpen_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    def test_nominateStoreManager_nominatedUserAlreadyOwner_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isOwner)
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses["Feliks"].isManager)

    def test_nominateStoreManager_nominatedUserAlreadyFounder_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Ari"].isFounder)
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Ari", "Store1"))

    def test_nominateStoreManager_nominatedUserAlreadyManager_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1")
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isManager)
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1"))
        self.assertTrue(self.store_facade.stores["Store1"].accesses["Feliks"].isManager)

    def test_nominateStoreManager_requesterNotLoggedIn_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.member1.logged_In = False
        self.assertRaises(Exception, self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].accesses.keys().__contains__("Feliks"))

    # ----------------------------- Not implemented yet --------------------------------
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
    # ----------------------------------------------------------------------------------

    def test_closeStore_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertFalse(self.store_facade.stores["Store1"].active)

    def test_closeStore_requesterNotFounder_failure(self):  
        self.member1.logged_In = True
        self.member3.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.closeStore("Amiel", "Store1"))
        self.assertTrue(self.store_facade.stores["Store1"].active)

    def test_closeStore_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.assertRaises(Exception, self.store_facade.closeStore("Ari", "Store1"))

    def test_closeStore_storeNotOpen_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.closeStore("Ari", "Store1"))
        self.assertFalse(self.store_facade.stores["Store1"].active)

    def test_closeStore_requesterNotLoggedIn_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.member1.logged_In = False
        self.assertRaises(Exception, self.store_facade.closeStore("Ari", "Store1"))
        self.assertTrue(self.store_facade.stores["Store1"].active)

    def test_getStaffInfo_success(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.nominateStoreManager("Ari", "Feliks", "Store1")
        self.access = self.member2.accesses["Store1"]
        self.assertEqual(self.store_facade.getStaffInfo("Ari", "Store1"), self.access)

    def test_getStaffInfo_storeDoesNotExist_failure(self):
        self.member1.logged_In = True
        self.assertRaises(Exception, self.store_facade.getStaffInfo("Ari", "Store2"))

    def test_getStaffInfo_storeNotOpen_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.store_facade.closeStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.getStaffInfo("Ari", "Store1"))

    def test_getStaffInfo_requesterNotLoggedIn_failure(self):
        self.member1.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.member1.logged_In = False
        self.assertRaises(Exception, self.store_facade.getStaffInfo("Ari", "Store1"))

    def test_getStaffInfo_requesterNotOwner_failure(self):
        self.member1.logged_In = True
        self.member2.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.getStaffInfo("Feliks", "Store1"))

    def test_getStaffInfo_requesterNotFounder_failure(self):
        self.member1.logged_In = True
        self.member3.logged_In = True
        self.store_facade.openStore("Ari", "Store1")
        self.assertRaises(Exception, self.store_facade.getStaffInfo("Amiel", "Store1"))

    # ----------------------------- Not implemented yet --------------------------------
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
