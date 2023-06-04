import unittest
from unittest import TestCase

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.MarketObjects.StoreObjects import Product
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import *
from ProjectCode.Domain.MarketObjects import Store
from ProjectCode.Domain.MarketObjects.Store import *
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
        self.store_facade.logInAsMember("John", "password123")
        self.store_facade.createStore("John", "AriExpress")
        self.store1: Store = self.store_facade.stores.get("AriExpress")
        self.store_facade.addNewProductToStore("John", "AriExpress", "paper", 10, 500, "paper")
        self.item_paper: Product = self.store1.getProductById(1, "John")
        self.store_facade.logOut("John")


    ########################### TEST ORM ###############################

    def test_addNewUser(self):
        db = SqliteDatabase('database.db')
        db.connect()
        db.drop_tables([MemberModel, CartModel, BasketModel])
        db.create_tables([MemberModel, CartModel, BasketModel])
        self.store_facade.add_member(Member(-1, "John", "password123", "john.doe@example.com"))
        member: Member = self.store_facade.get_member("John")
        self.assertEqual(member.get_username(), "John")
        self.assertEqual(member.get_password(), "password123")
        self.assertEqual(member.get_email(), "john.doe@example.com")
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

    def test_logOutAndBecomeGuest(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.assertTrue(self.store_facade.online_members.__contains__(self.member1.get_username()))
        entrance_num = str(self.member1.get_entrance_id())
        self.store_facade.logOut(self.member1.get_username())
        self.assertIn(entrance_num, self.store_facade.onlineGuests.keys())

    def test_logOut_fail(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.assertTrue(self.store_facade.online_members.__contains__(self.member1.get_username()))
        with self.assertRaises(Exception):
            self.store_facade.logOut("made_up_user_name")

    ############################### TEST MEMBERS PURCHASE HISTORY & CARTS & BASKETS ###############################
    # getPurchaseHistory
    def test_getMemberPurchaseHistory_fail_notLogged_in(self):
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory(self.member1.get_username())

    def test_getMemberPurchaseHistory_invalid_username(self):
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory("UN_REAL_USER")

    # getCart
    def test_getCart_success(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        cart: Cart = self.store_facade.members.get("John").get_cart()
        self.assertEqual(cart.get_username(), self.member1.get_username())

    def test_getCart_userNotLoggedIn_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.getCart(self.member1.get_username())

    def test_getCart_userNotRegistered_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.getCart("Unreal_User")

    # getBasket
    def test_getBasket_success(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 5)
        basket: Basket = self.member1.get_Basket(self.store1.get_store_name())
        self.assertTrue(basket.get_Store().get_store_name() == self.store1.get_store_name())

    def test_getBasket_userNotLoggedIn_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
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
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        basket: Basket = self.member1.get_cart().get_Basket(self.store1.get_store_name())
        self.assertEqual(len(basket.get_Products()), 1)
        self.assertEqual(basket.get_Products().get(self.item_paper.get_product_id())[1], 5)
        self.assertIn(self.item_paper.get_product_id(), basket.get_Products().keys())

    def test_addToBasket_negativeQuantity_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), -5)

    def test_addToBasket_zeroQuantity_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 0)

    def test_addToBasket_productDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), "UNREAL_PRODUCT", 5)

    def test_addToBasket_storeDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), "UNREAL_STORE", self.item_paper.get_product_id(), 5)

    def test_addToBasket_usernameDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("UNREAL_USER", self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    def test_addToBasket_userNotLoggedIn_failure(self):
        self.member1.logOut()
        with self.assertRaises(Exception):
            self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    # remove from basket
    def test_removeFromBasket_success(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 5)
        answer: bool = self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id())
        self.assertTrue(answer)

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
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.get_store_name(),
                                               self.item_paper.name)

    def test_removeFromBasket_basketIsEmpty_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.removeFromBasket(self.member1.get_username(), self.store1.get_store_name(),
                                               self.item_paper.name)

    # edit product quantity
    def test_editBasketQuantity_success(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        basket: Basket = self.member1.get_cart().get_Basket(self.store1.get_store_name())
        self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                             self.item_paper.get_product_id(), 3)
        self.assertTrue(basket.get_Products().get(self.item_paper.get_product_id())[1], 3)
        self.assertIn(self.item_paper.get_product_id(), basket.get_Products().keys())

    def test_editBasketQuantity_negativeQuantity_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), -5)

    def test_editBasketQuantity_zeroQuantity_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 0)

    def test_editBasketQuantity_userNotLoggedIn_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 5)
        self.store_facade.logOut(self.member1.get_username())
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_basketIsEmpty_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(),
                                                 self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_productDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), self.store1.get_store_name(), "UNREAL_PRODUCT",
                                                 5)

    def test_editBasketQuantity_storeDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity(self.member1.get_username(), "UNREAL_STORE", self.item_paper.get_product_id(), 5)

    def test_editBasketQuantity_usernameDoesNotExist_failure(self):
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("UNREAL_USER", self.store1.get_store_name(), self.item_paper.get_product_id(), 5)

    # edit purchase quantity
    def test_purchaseCart_success(self):
        transaction_history = TransactionHistory()
        self.store_facade.logInAsMember(self.member1.get_username(),self.member1.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(),
                                      self.item_paper.get_product_id(), 5)
        basket: Basket = self.member1.get_Basket(self.store1.get_store_name())
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555","wherever")
        self.assertTrue(len(transaction_history.get_User_Transactions("John")) == 1)
        self.assertTrue(len(transaction_history.get_Store_Transactions("AriExpress")) == 1)
        transaction_history.clearAllHistory()

    # here we need to check deeper about the paying processes and things that can get wrong:
    # 1. the user is not logged in
    # 2. the user does not exist
    # 3. the user does not have enough money
    # 4. the store does not have enough products
    # 5. the basket is empty
    # 6. someone else bought already the products before and after the adding to basket

    def test_purchaseCart_userNotLoggedIn_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")

    def test_purchaseCart_usernameDoesNotExist_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("UNREAL_USER", "4580", "John Doe", "007", "12/26", "555")

    #def test_purchaseCart_notEnoughMoney_failure(self):
       # self.assertFalse(False)
        # TODO here we need to check deeper about the paying processes and things that can get wrong:
        # maybe a mock that accept one card and doesn't accept the other one

    def test_purchaseCart_basketIsEmpty_failure(self):
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555")

    def test_purchaseCart_someoneElseBought_failure(self):
        transaction_history = TransactionHistory()
        self.store_facade.logInAsMember(self.member1.get_username(), self.member1.get_password())
        self.store_facade.logInAsMember(self.member2.get_username(), self.member2.get_password())
        self.store_facade.addToBasket(self.member1.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 9)
        self.store_facade.addToBasket(self.member2.get_username(), self.store1.get_store_name(), self.item_paper.get_product_id(), 9)
        self.store_facade.purchaseCart(self.member1.get_username(), "4580", "John Doe", "007", "12/26", "555", "some_address")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart(self.member2.get_username(), "4580", "Jane Doe", "008", "12/26", "555", "some_address")
        transaction_history.clearAllHistory()

if __name__ == '__main__':
    unittest.main()
