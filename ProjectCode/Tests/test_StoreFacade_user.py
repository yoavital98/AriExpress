import unittest
from unittest import TestCase

from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Basket import Basket
from ProjectCode.Domain.Objects.UserObjects.Guest import Guest


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        self.store_facade = StoreFacade()
        self.store_facade.openSystem('Ari')
        self.member1 = self.store_facade.register("John", "password123", "john.doe@example.com")
        self.member2 = self.store_facade.register("Jane", "password456", "jane.doe@example.com")
        self.store1 = self.store_facade.openStore(self.member1.get_username(), "Dunder Mifflin")
        self.item_paper = self.store_facade.addNewProductToStore(self.member1.get_username(), self.store1.store_name,
                                                                 "Paper", 10, 10, ["Office"])

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
        member = self.store_facade.register(username, password, email)
        self.assertEqual(self.store_facade.members[username], member)
        self.assertIn(member, self.store_facade.members)

    def test_register_existingUser(self):
        # trying to register an existing user
        with self.assertRaises(Exception):
            self.store_facade.register("John", "password123", "john.doe@example.com")

    ############################### TEST LOGIN CHECK ###############################
    def test_checkIfMemberIsLoggedIn_existingUserLoggedIn(self):
        self.member1.logInAsMember()
        self.assertTrue(self.store_facade.checkIfUserIsLoggedIn("John"))

    def test_checkIfMemberIsLoggedIn_existingUserLoggedOut(self):
        self.member1.logOff()
        self.assertFalse(self.store_facade.checkIfUserIsLoggedIn("John"))

    def test_checkIfMemberIsLoggedIn_UserNotExists(self):
        with self.assertRaises(Exception):
            self.store_facade.checkIfUserIsLoggedIn("Amiel")

    ############################### TEST Guests LOGIN-OUT ###############################

    def test_logInAsGuest_checkIDAndOnlineGuests(self):
        previous_last_entrance_id = self.store_facade.nextEntranceID
        guest = self.store_facade.logInAsGuest()
        new_last_entrance_id = self.store_facade.nextEntranceID
        self.assertEqual(guest.entrance_id, previous_last_entrance_id)
        self.assertNotEqual(guest.entrance_id, new_last_entrance_id)
        self.assertIn(str(previous_last_entrance_id), self.store_facade.onlineGuests)

    def test_leaveAsGuest_success(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = Guest(entrance_id)
        self.store_facade.onlineGuests[str(entrance_id)] = guest
        self.store_facade.leaveAsGuest(entrance_id)
        self.assertNotIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_leaveAsGuest_failure(self):
        entrance_id = self.store_facade.nextEntranceID
        with self.assertRaises(Exception):
            self.store_facade.leaveAsGuest(entrance_id + 1)

    ############################### TEST MEMBERS LOGIN-OUT ###############################

    def test_logInAsMember_success(self):
        self.assertEqual(self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password()),
                         self.member1)
        self.assertTrue(self.member1.get_logged())

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
        self.assertTrue(self.member1.get_logged())
        self.member1.logOff()
        self.assertFalse(self.member1.get_logged())

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
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.product_id, 5)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.store_name)
        self.assertEqual(len(basket1.get_Products), 5)
        self.assertIn(self.item_paper, basket1.get_Products())

    def test_addToBasket_negativeQuantity_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, -5)

    def test_addToBasket_zeroQuantity_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 0)

    def test_addToBasket_productDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, "UNREAL_PRODUCT", 5)

    def test_addToBasket_storeDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), "UNREAL_STORE", self.item_paper.name, 5)

    def test_addToBasket_usernameDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("UNREAL_USER", self.store1.store_name, self.item_paper.name, 5)

    def test_addToBasket_userNotLoggedIn_failure(self):
        self.member1.logOff()
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)

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
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name, self.item_paper.name,
                                             3)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.store_name)
        self.assertEqual(len(basket1.get_Products[0]), 3)
        self.assertIn(self.item_paper, basket1.get_Products())

    def test_editBasketQuantity_negativeQuantity_failure(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name,
                                                 self.item_paper.name, -5)

    def test_editBasketQuantity_zeroQuantity_failure(self):
        self.member1.logInAsMember()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name,
                                                 self.item_paper.name, 0)

    def test_editBasketQuantity_userNotLoggedIn_failure(self):
        self.member1.logOff()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name,
                                                 self.item_paper.name, 5)

    def test_editBasketQuantity_basketIsEmpty_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name,
                                                 self.item_paper.name, 5)

    def test_editBasketQuantity_productDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.store_name, "UNREAL_PRODUCT",
                                                 5)

    def test_editBasketQuantity_storeDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), "UNREAL_STORE", self.item_paper.name, 5)

    def test_editBasketQuantity_usernameDoesNotExist_failure(self):
        self.member1.logInAsMember()
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("UNREAL_USER", self.store1.store_name, self.item_paper.name, 5)

    # edit purchase quantity
    def test_purchaseCart_success(self):
        self.member1.logInAsMember()
        user_transaction_number = self.store_facade.transaction_history.get_User_Transactions(
            self.member1.get_username()).sizeof()
        store_transaction_number = self.store_facade.transaction_history.get_Store_Transactions(
            self.store1.name).sizeof()
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 5)
        basket1 = self.store_facade.getBasket(self.member1.get_username(), self.store1.store_name)
        self.assertEqual(len(basket1.get_Products[0]), 5)
        self.assertEqual(self.store1.get_product(self.item_paper.name).get_quantity(), 10)
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")
        self.assertEqual(len(basket1.get_Products[0]), 0)
        self.assertEqual(self.store1.get_product(self.item_paper.name).get_quantity(), 5)
        self.assertEqual(
            self.store_facade.transaction_history.get_User_Transactions(self.member1.get_username()).sizeof(),
            user_transaction_number + 1)
        self.assertEqual(self.store_facade.transaction_history.get_Store_Transactions(self.store1.name).sizeof(),
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
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.store_name, self.item_paper.name, 9)
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.store_name, self.item_paper.name, 9)
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555")


if __name__ == '__main__':
    unittest.main()
