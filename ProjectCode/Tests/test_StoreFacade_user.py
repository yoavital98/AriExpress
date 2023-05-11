import unittest
from unittest import TestCase

from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Domain.StoreFacade import StoreFacade
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Cart import Cart
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        self.store_facade = StoreFacade()
        self.store_facade.register("John", "password123", "john.doe@example.com")
        self.store_facade.register("Jane", "password456", "jane.doe@example.com")
        self.member1: Member = self.store_facade.members.get("John")
        self.member2: Member = self.store_facade.members.get("Jane")


    # def test_load_data(self):
    #     self.fail()
    #
    # def test_exit_the_system(self):
    #     self.fail()

    ########################### TEST REGISTER ###############################
    def test_register_newUser(self):
        # check a new register signup
        username = "test_user"
        password = "test_password"
        email = "test_email@example.com"
        self.store_facade.register(username, password, email)
        member: Member = self.store_facade.members.get("test_user")
        self.assertEqual(member.get_username(), "test_user")

    def test_register_existingUser(self):
        # trying to register an existing user
        with self.assertRaises(Exception):
            self.store_facade.register("John", "password123", "john.doe@example.com")

    ############################### TEST LOGIN CHECK ###############################
    def test_checkIfMemberIsLoggedIn_existingUserLoggedIn(self):
        self.store_facade.logInAsMember("John", "password123")
        member: Member = self.store_facade.online_members.get("John")
        self.assertTrue(member.get_username(), self.member1.get_username())

    def test_checkIfMemberIsLoggedIn_existingUserLoggedOut(self):
        self.member1.logOut()
        self.assertFalse(self.store_facade.online_members.__contains__(self.member1.get_username()))

    def test_checkIfMemberIsLoggedIn_UserNotExists(self):
        self.assertFalse(self.store_facade.checkIfUserIsLoggedIn("Amiel"))

    ############################### TEST Guests LOGIN-OUT ###############################

    def test_logInAsGuest_checkIDAndOnlineGuests(self):
        previous_last_entrance_id = self.store_facade.nextEntranceID
        self.store_facade.loginAsGuest()
        guest: Guest = self.store_facade.onlineGuests.get(str(previous_last_entrance_id))
        self.assertEqual(guest.get_entrance_id(), previous_last_entrance_id)

    def test_leaveAsGuest_success(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = Guest(entrance_id)
        self.store_facade.onlineGuests[str(entrance_id)] = guest
        self.store_facade.leaveAsGuest(entrance_id)
        self.assertNotIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_leaveAsGuest_failure_notTheSameEntranceID(self):
        entrance_id = self.store_facade.nextEntranceID
        with self.assertRaises(Exception):
            self.store_facade.leaveAsGuest(entrance_id + 1)

    ############################### TEST MEMBERS LOGIN-OUT ###############################

    def test_logInAsMember_success(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.assertTrue(self.store_facade.online_members.__contains__(self.member1.get_username()))

    def test_logInAsMember_failure_unExistingUser(self):
        with self.assertRaises(Exception):
            self.store_facade.logInAsMember("UnRealUser", "1234")

    def test_logInAsMember_failure_userNotRegistered_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.logInAsMember("UnRealUser", "1234")

    def test_logInAsMember_failure_wrongPassword(self):
        with self.assertRaises(Exception):
            self.store_facade.logInAsMember(self.member1.get_username(), "wrong_password")

    def test_logOut(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.assertTrue(self.store_facade.online_members.__contains__(self.member1.get_username()))
        self.store_facade.logOut(self.member1.get_username())
        self.assertFalse(self.store_facade.online_members.__contains__(self.member1.get_username()))

    ############################### TEST MEMBERS PURCHASE HISTORY & CARTS & BASKETS ###############################
    # getPurchaseHistory
    def test_getMemberPurchaseHistory_success(self):
        self.member1.logInAsMember()
        self.assertEqual(self.store_facade.getMemberPurchaseHistory(self.member1.get_username().get_username()).user,
                         self.member1)
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory(self.member1.get_username())

    def test_getMemberPurchaseHistory_invalid_username(self):
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory("UN_REAL_USER")

    # getCart
    def test_getCart_success(self):
        self.member1.logInAsMember()
        cart1 = self.store_facade.getCart(self.member1.get_username())
        self.assertEqual(cart1.get_username, self.member1)
        self.assertIsInstance(cart1, Cart)

    def test_getCart_userNotLoggedIn_failure(self):
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.getCart(self.member1.get_username())

    def test_getCart_userNotRegistered_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.getCart("Unreal_User")

    # getBasket
    def test_getBasket_success(self):
        self.member1.logInAsMember()
        basket1 = self.store_facade.getBasket(self.member1.get_username(), "Office Depot")
        self.assertEqual(basket1.user, self.member1)
        self.assertIsInstance(basket1, Basket)

    def test_getBasket_userNotLoggedIn_failure(self):
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.getBasket(self.member1.get_username(), "Office Depot")

    def test_getBasket_userNotRegistered_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.getBasket("Unreal_User", "Office Depot")

    def test_getBasket_storeDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.getBasket(self.member1.get_username(), "UNREAL_STORE")

    ############################### TEST Managing Baskets ###############################
    # add to basket
    def test_addToBasket_success(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.get_store_name())
        self.assertEqual(len(basket1.get_Products()), 1)
        self.assertEqual(basket1.get_Products().get(self.item_paper.get_product_id())[1], 5)
        self.assertIn(self.item_paper.get_product_id(), basket1.get_Products().keys())

    def test_addToBasket_negativeQuantity_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), -5)

    def test_addToBasket_zeroQuantity_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 0)

    def test_addToBasket_productDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), "UNREAL_PRODUCT", 5)

    def test_addToBasket_storeDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), "UNREAL_STORE", self.item_paper.get_product_id(), 5)

    def test_addToBasket_usernameDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("UNREAL_USER", self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    def test_addToBasket_userNotLoggedIn_failure(self):
        self.member1.logOut()
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    # remove from basket
    def test_removeFromBasket_success(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.store_name)
        self.assertEqual(len(basket1.get_Products[0]), 5)
        self.assertNotIn(self.item_paper, basket1.get_Products())

    def test_removeFromBasket_productDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.store_name, "UNREAL_PRODUCT")

    def test_removeFromBasket_storeDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), "UNREAL_STORE", self.item_paper.name)

    def test_removeFromBasket_usernameDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket("UNREAL_USER", self.store1.store_name, self.item_paper.name)

    def test_removeFromBasket_userNotLoggedIn_failure(self):
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.store_name,
                                               self.item_paper.name)

    def test_removeFromBasket_basketIsEmpty_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.store_name,
                                               self.item_paper.name)

    # edit product quantity
    def test_editBasketQuantity_success(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name, self.item_paper.name,
                                             3)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.store_name)
        self.assertEqual(len(basket1.get_Products[0]), 3)
        self.assertIn(self.item_paper, basket1.get_Products())

    def test_editBasketQuantity_negativeQuantity_failure(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), -5)

    def test_editBasketQuantity_zeroQuantity_failure(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 0)

    def test_editBasketQuantity_userNotLoggedIn_failure(self):
        self.member1.logOut()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_basketIsEmpty_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_productDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(), "UNREAL_PRODUCT",
                                                 5)

    def test_editBasketQuantity_storeDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), "UNREAL_STORE", self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_usernameDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("UNREAL_USER", self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    # edit purchase quantity
    def test_purchaseCart_success(self):
        self.member1.logInAsMember()
        user_transaction_number = self.store_facade.transaction_history.get_User_Transactions(
            self.member1.get_username()).sizeof()
        store_transaction_number = self.store_facade.transaction_history.get_Store_Transactions(
            self.store1.get_store_name()).sizeof()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.get_store_name())
        self.assertEqual(len(basket1.get_Products[0]), 5)
        self.assertEqual(self.store1.get_product(self.item_paper.get_product_id()).get_quantity(), 10)
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")
        self.assertEqual(len(basket1.get_Products[0]), 0)
        self.assertEqual(self.store1.get_product(self.item_paper.get_product_id()).get_quantity(), 5)
        self.assertEqual(
            self.store_facade.transaction_history.get_User_Transactions(self.member1.get_username()).sizeof(),
            user_transaction_number + 1)
        self.assertEqual(self.store_facade.transaction_history.get_Store_Transactions(self.store1.get_store_name()).sizeof(),
                         store_transaction_number + 1)

    # here we need to check deeper about the paying processes and things that can get wrong:
    # 1. the user is not logged in
    # 2. the user does not exist
    # 3. the user does not have enough money
    # 4. the store does not have enough products
    # 5. the basket is empty
    # 6. someone else bought already the products before and after the adding to basket

    def test_purchaseCart_userNotLoggedIn_failure(self):
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")

    def test_purchaseCart_usernameDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("UNREAL_USER", "4580", "John Doe", "007", "12/26", "555")

    def test_purchaseCart_notEnoughMoney_failure(self):
        self.assertFalse(True)
        # TODO here we need to check deeper about the paying processes and things that can get wrong:
        # maybe a mock that accept one card and doesn't accept the other one

    def test_purchaseCart_basketIsEmpty_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")

    def test_purchaseCart_someoneElseBought_failure(self):
        self.member1.logInAsMember()
        self.member2.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 9)
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 9)
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555")


if __name__ == '__main__':
    unittest.main()
