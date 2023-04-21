import unittest
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects.Member import Member


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        self.store_facade = StoreFacade()
        self.member1 = Member("John", "password123", "john.doe@example.com")
        self.store_facade.members["John"] = self.member1
        self.member2 = Member("Jane", "password456", "jane.doe@example.com")
        self.store_facade.members["Jane"] = self.member2
        # self.username = "test_user"
        # self.password = "test_password"
        # self.member = Member(self.username, self.password, "testing111@gmail.com")
        # self.member = Member("JohnDoe", "password", "testing222@gmail.com")
        # self.store_facade.members["JohnDoe"] = self.member
        # self.store = Store("Store1")
        # self.store_facade.stores["Store1"] = self.store

    # def test_load_data(self):
    #     self.fail()
    #
    # def test_exit_the_system(self):
    #     self.fail()


    def test_register_success(self):

    def test_register_new_member_success(self):
        # check a new register signup

        username = "test_user"
        password = "test_password"
        email = "test_email@example.com"
        member = self.store_facade.register(username, password, email)
        self.assertEqual(self.store_facade.members[username], member)


    def test_register_new_member_failure(self):
        # trying to register an existing user
        self.assertRaises(self.store_facade.register("John", "password123", "john.doe@example.com"), SystemError)


    def test_checkIfUserIsLoggedIn_existingUserLoggedIn_success(self):
        self.member1.logInAsMember()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, True)


    def test_checkIfUserIsLoggedIn_existingUserNotLoggedIn_success(self):  #success but returns false

    def test_checkIfUserIsLoggedIn_existingUserLoggedIn_failure(self):
        self.member1.logInAsMember()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, True)

    def test_checkIfUserIsLoggedIn_existingUserNotLoggedIn_success(self):
        self.member1.logOff()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, False)
    def test_checkIfUserIsLoggedIn_existingUserNotLoggedIn_failure(self):
        self.member1.logOff()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, False)


    def test_checkIfUserIsLoggedIn_nonExistingUser_success(self):
        with self.assertRaises(SystemError):
            self.store_facade.checkIfUserIsLoggedIn("NonExistingUser")

    def test_checkIfUserIsLoggedIn_nonExistingUser_failure(self):
        with self.assertRaises(SystemError):
            self.store_facade.checkIfUserIsLoggedIn("NonExistingUser")

    def test_logInAsGuest_success(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = self.store_facade.logInAsGuest()
        self.assertEqual(guest.id, entrance_id)
        self.assertIn(str(entrance_id), self.store_facade.onlineGuests)
        
    def test_logInAsGuest_failure(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = self.store_facade.logInAsGuest()
        self.assertEqual(guest.id, entrance_id)
        self.assertIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_leaveAsGuest_success(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = Mock()
        guest.id = entrance_id
        self.store_facade.onlineGuests[str(entrance_id)] = guest
        self.store_facade.leaveAsGuest(entrance_id)
        self.assertNotIn(str(entrance_id), self.store_facade.onlineGuests)
        
    def test_leaveAsGuest_failure(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = Mock()
        guest.id = entrance_id
        self.store_facade.onlineGuests[str(entrance_id)] = guest
        self.store_facade.leaveAsGuest(entrance_id)
        self.assertNotIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_logInAsMember_existing_user_success(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member
        # call login function
        logged_in_member = self.store_facade.logInAsMember(self.username, self.password)
       
    def test_logInAsMember_existing_user_failure(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member
        # call login function
        logged_in_member = self.store_facade.logInAsMember(self.username, self.password)


    def test_logInAsMember_userNotLoggedIn_success(self):
        pass
        # check that the member is logged in
        self.assertTrue(logged_in_member.get_logged())
   
   def test_logInAsMember_existing_user_failure(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member

    def test_logInAsMember_userLoggedIn_success(self):
        pass
    
    def test_logInAsMember_userLoggedIn_failure(self):
        pass
        
    def test_logInAsMember_userNotRegistered_success(self):
        pass
    def test_logInAsMember_userNotRegistered_failure(self):
        pass

    def test_logInAsMember_wrongPassword_success(self):
        pass

    def test_logInAsMember_wrongPassword_failure(self):
        pass

    def test_logOut_success(self):
        pass
        # username = "test_user111"
        # password = "password123"
        # member = Member(username, password, "testingEmail@gmail.com")
        # self.store_facade.members[username] = member
        # member.logInAsMember()
        # self.store_facade.logOut(username)
        # self.assertFalse(member.get_logged())

    def test_logOut_userNotLoggedIn_failure(self):
        pass

    def test_logOut_userNotRegistered_failure(self):

    def test_logInAsMember_non_existing_user_success(self):
        # call login function for non-existing user
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember("non_existing_user", self.password)
    def test_logInAsMember_non_existing_user_failure(self):
        # call login function for non-existing user
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember("non_existing_user", self.password)

    def test_logInAsMember_wrong_password_success(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member

        # call login function with wrong password
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember(self.username, "wrong_password")

    def test_logInAsMember_wrong_password_failure(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member

        # call login function with wrong password
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember(self.username, "wrong_password")

    def test_logOut_member_exists_success(self):
        username = "test_user111"
        password = "password123"
        member = Member(username, password, "testingEmail@gmail.com")
        self.store_facade.members[username] = member
        member.logInAsMember()
        self.store_facade.logOut(username)
        self.assertFalse(member.get_logged())
    def test_logOut_member_exists_failure(self):
        username = "test_user111"
        password = "password123"
        member = Member(username, password, "testingEmail@gmail.com")
        self.store_facade.members[username] = member
        member.logInAsMember()
        self.store_facade.logOut(username)
        self.assertFalse(member.get_logged())

    def test_logOut_member_does_not_exist_success(self):
        # Try to log out a member that does not exist
        username = "nonexistent_user"
        self.store_facade.logOut(username)
        self.assertTrue(True)
    def test_logOut_member_does_not_exist_failure(self):
        # Try to log out a member that does not exist
        username = "nonexistent_user"
        self.store_facade.logOut(username)
        self.assertTrue(True)


    def test_getMemberPurchaseHistory_guestLoggedIn_failure(self):

    def test_getMemberPurchaseHistory_returns_transaction_history_for_valid_username_success(self):
        # Arrange
        test_username = "test_user"
        # TODO: create a mock TransactionHistory and add some transactions for the test user

        # Act
        result = self.store_facade.getMemberPurchaseHistory(test_username)

        # Assert
        # TODO: add assertions to verify that the correct TransactionHistory is returned
    def test_getMemberPurchaseHistory_returns_transaction_history_for_valid_username_failure(self):

        # Arrange
        test_username = "test_user"
        # TODO: check if something needs to return (from guestID or something)


    def test_getMemberPurchaseHistory_usernameDoesNotExist_failure(self):
        pass

    def test_getMemberPurchaseHistory_userNotLoggedIn_failure(self):
        pass

    def test_getMemberPurchaseHistory_success(self):
        pass

        # Assert
        # TODO: add assertions to verify that the correct TransactionHistory is returned

    def test_getMemberPurchaseHistory_returns_none_for_invalid_username_success(self):
        # Arrange
        test_username = "invalid_user"

        # Act
        result = self.store_facade.getMemberPurchaseHistory(test_username)

        # Assert
        self.assertIsNone(result)
    def test_getMemberPurchaseHistory_returns_none_for_invalid_username_failure(self):
        # Arrange
        test_username = "invalid_user"

        # Act
        result = self.store_facade.getMemberPurchaseHistory(test_username)

        # Assert
        self.assertIsNone(result)

    def test_getMemberPurchaseHistory_raises_error_if_user_is_not_logged_in_success(self):
        # Arrange
        test_username = "test_user"
        # TODO: log the test user out

        # Act & Assert
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory(test_username)
    def test_getMemberPurchaseHistory_raises_error_if_user_is_not_logged_in_failure(self):
        # Arrange
        test_username = "test_user"
        # TODO: log the test user out

        # Act & Assert
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory(test_username)

    def test_get_basket_success(self):
        # test with invalid username, should return None
        self.assertIsNone(self.store_facade.getBasket("invalid_username", "Store1"))

        # test with valid username and storename, should return a Cart object
        basket = self.store_facade.getBasket("JohnDoe", "Store1")
        self.assertIsInstance(basket, Cart)
    def test_get_basket_failure(self):
        # test with invalid username, should return None
        self.assertIsNone(self.store_facade.getBasket("invalid_username", "Store1"))


    def test_getBasket_success(self):
        pass


    def test_getBasket_userNotLoggedIn_failure(self):
        pass

    def test_getBasket_userNotRegistered_failure(self):
        pass

    def test_getBasket_storeDoesNotExist_failure(self):
        pass

    def test_addToBasket_success(self):
        pass

    def test_addToBasket_negativeQuantity_failure(self):
        pass

    def test_addToBasket_zeroQuantity_failure(self):
        pass

    def test_addToBasket_productDoesNotExist_failure(self):
        pass

    def test_addToBasket_storeDoesNotExist_failure(self):
        pass

    def test_addToBasket_usernameDoesNotExist_failure(self):
        pass

    def test_addToBasket_loggedUserNotFounder_failure(self):
        pass

    def test_addToBasket_loggedUserNotOwner_failure(self):
        pass

    def test_addToBasket_userNotLoggedIn_failure(self):
        pass

    def test_removeFromBasket_success(self):
        pass

    def test_removeFromBasket_productDoesNotExist_failure(self):
        pass

    def test_removeFromBasket_usernameDoesNotExist_failure(self):
        pass

    def test_removeFromBasket_userNotLoggedIn_failure(self):
        pass

    def test_removeFromBasket_basketIsEmpty_failure(self):
        pass

    def test_editBasketQuantity_success(self):
        pass

    def test_editBasketQuantity_negativeQuantity_failure(self):
        pass

    def test_editBasketQuantity_zeroQuantity_failure(self):
        pass

    def test_editBasketQuantity_userNotLoggedIn_failure(self):
        pass

    def test_editBasketQuantity_basketIsEmpty_failure(self):
        pass
    
    def test_purchaseCart_success(self):
        pass

    def test_purchaseCart_userNotLoggedIn_failure(self):
        pass

    def test_purchaseCart_basketIsEmpty_failure(self):

    def test_get_basket_with_invalid_storename_success(self):
        # test with invalid storename, should raise an error
        with self.assertRaises(SystemError):
            self.store_facade.getBasket("JohnDoe", "invalid_storename")
    def test_get_basket_with_invalid_storename_failure(self):
        # test with invalid storename, should raise an error
        with self.assertRaises(SystemError):
            self.store_facade.getBasket("JohnDoe", "invalid_storename")

    # (self,username):
    def test_get_cart_success(self):
        # test with invalid username, should return None
        self.assertIsNone(self.store_facade.getCart("invalid_username"))

        # test with valid username, should return a Cart object
        cart = self.store_facade.getCart("JohnDoe")
        self.assertIsInstance(cart, Cart)
    def test_get_cart_failure(self):
        # test with invalid username, should return None
        self.assertIsNone(self.store_facade.getCart("invalid_username"))

        # test with valid username, should return a Cart object
        cart = self.store_facade.getCart("JohnDoe")
        self.assertIsInstance(cart, Cart)


    def test_addToBasket_valid_input_success(self):
        pass
    def test_addToBasket_valid_input_failure(self):
        pass
    def test_addToBasket_invalid_quantity_success(self):
        pass
    def test_addToBasket_invalid_quantity_failure(self):
        pass
    def test_addToBasket_invalid_product_success(self):
        pass
    def test_addToBasket_invalid_product_failure(self):
        pass
    def test_addToBasket_invalid_store_success(self):
        pass
    def test_addToBasket_invalid_store_failure(self):
        pass
    def test_addToBasket_invalid_username_success(self):
        pass
    def test_addToBasket_invalid_username_failure(self):
        pass
    def test_removeFromBasket_valid_input_success(self):
        pass
    def test_removeFromBasket_valid_input_failure(self):
        pass
    def test_removeFromBasket_invalid_quantity_success(self):
        pass
    def test_removeFromBasket_invalid_quantity_failure(self):
        pass
    def test_removeFromBasket_invalid_product_success(self):
        pass
    def test_removeFromBasket_invalid_product_failure(self):
        pass
    def test_removeFromBasket_invalid_store_success(self):
        pass
    def test_removeFromBasket_invalid_store_failure(self):
        pass
    def test_removeFromBasket_invalid_username_success(self):
        pass
    def test_removeFromBasket_invalid_username_failure(self):
        pass
    def test_removeFromBasket_empty_cart_success(self):
        pass
    def test_removeFromBasket_empty_cart_failure(self):
        pass
    def test_removeFromBasket_empty_basket_success(self):
        pass
    def test_removeFromBasket_empty_basket_failure(self):
        pass
    def test_editBasketQuantity_valid_input_success(self):
        pass
    def test_editBasketQuantity_valid_input_failure(self):
        pass
    def test_editBasketQuantity_invalid_quantity_success(self):
        pass
    def test_editBasketQuantity_invalid_quantity_failure(self):
        pass
    def test_editBasketQuantity_invalid_product_success(self):
        pass
    def test_editBasketQuantity_invalid_product_failure(self):
        pass
    def test_editBasketQuantity_invalid_store_success(self):
        pass
    def test_editBasketQuantity_invalid_store_failure(self):
        pass
    def test_editBasketQuantity_invalid_username_success(self):
        pass
    def test_editBasketQuantity_invalid_username_failure(self):
        pass
    def test_editBasketQuantity_empty_cart_success(self):
        pass
    def test_editBasketQuantity_empty_cart_failure(self):
        pass
    def test_editBasketQuantity_empty_basket_success(self):
        pass
    def test_editBasketQuantity_empty_basket_failure(self):
        pass
    def test_purchaseCart_valid_input_success(self):
        pass
    def test_purchaseCart_valid_input_failure(self):
        pass

if __name__ == '__main__':
    unittest.main()
