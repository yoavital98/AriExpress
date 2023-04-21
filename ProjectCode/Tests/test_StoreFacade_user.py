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
        # self.member1 = Member("John", "password123", "john.doe@example.com")
        # self.store_facade.members["John"] = self.member1
        # self.member2 = Member("Jane", "password456", "jane.doe@example.com")
        # self.store_facade.members["Jane"] = self.member2
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
        username = "test_user"
        password = "test_password"
        email = "test_email@example.com"
        # self.store_facade.passwordValidator.ValidatePassword = MagicMock(return_value=True)
        member = self.store_facade.register(username, password, email)
        self.assertEqual(self.store_facade.members[username], member)

    def test_register_usernameTaken_failure(self):
        pass
        # username = "test_user"
        # password = "test_password"
        # email = "test_email@example.com"
        # # self.store_facade.passwordValidator.ValidatePassword = MagicMock(return_value=True)
        # member = self.store_facade.register(username, password, email)
        # self.assertRaises(self.store_facade.register(username, password, email), SystemError)

    def test_register_passwordInvalid_failure(self):
        pass

    def test_checkIfUserIsLoggedIn_existingUserLoggedIn_success(self):
        self.member1.logInAsMember()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, True)

    def test_checkIfUserIsLoggedIn_existingUserNotLoggedIn_success(self):  #success but returns false
        self.member1.logOff()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, False)

    def test_checkIfUserIsLoggedIn_nonExistingUser_failure(self):
        with self.assertRaises(SystemError):
            self.store_facade.checkIfUserIsLoggedIn("NonExistingUser")

    def test_logInAsGuest_success(self):
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
        # TODO: create a member (not guest) and try to log him out
        pass

    def test_logInAsMember_userNotLoggedIn_success(self):
        pass

    def test_logInAsMember_userLoggedIn_failure(self):
        pass

    def test_logInAsMember_userNotRegistered_failure(self):
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
        # Try to log out a member that does not exist
        username = "nonexistent_user"
        self.store_facade.logOut(username)
        self.assertTrue(True)

    def test_getMemberPurchaseHistory_guestLoggedIn_failure(self):
        # Arrange
        test_username = "test_user"
        # TODO: check if something needs to return (from guestID or something)

    def test_getMemberPurchaseHistory_usernameDoesNotExist_failure(self):
        pass

    def test_getMemberPurchaseHistory_userNotLoggedIn_failure(self):
        pass

    def test_getMemberPurchaseHistory_success(self):
        pass

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
        pass


if __name__ == '__main__':
    unittest.main()
