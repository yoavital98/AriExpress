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
        self.username = "test_user"
        self.password = "test_password"
        self.member = Member(self.username, self.password, "testing111@gmail.com")
        self.member = Member("JohnDoe", "password", "testing222@gmail.com")
        self.store_facade.members["JohnDoe"] = self.member
        self.store = Store("Store1")
        self.store_facade.stores["Store1"] = self.store

    def test_load_data(self):
        self.fail()

    def test_exit_the_system(self):
        self.fail()

    def test_register_new_member(self):
        username = "test_user"
        password = "test_password"
        email = "test_email@example.com"
        self.store_facade.passwordValidator.ValidatePassword = MagicMock(return_value=True)
        member = self.store_facade.register(username, password, email)
        self.assertEqual(self.store_facade.members[username], member)

    def test_checkIfUserIsLoggedIn_existingUserLoggedIn(self):
        self.member1.logInAsMember()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, True)

    def test_checkIfUserIsLoggedIn_existingUserNotLoggedIn(self):
        self.member1.logOff()
        result = self.store_facade.checkIfUserIsLoggedIn("John")
        self.assertEqual(result, False)

    def test_checkIfUserIsLoggedIn_nonExistingUser(self):
        with self.assertRaises(SystemError):
            self.store_facade.checkIfUserIsLoggedIn("NonExistingUser")

    def test_logInAsGuest(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = self.store_facade.logInAsGuest()
        self.assertEqual(guest.id, entrance_id)
        self.assertIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_leaveAsGuest(self):
        entrance_id = self.store_facade.nextEntranceID
        guest = Mock()
        guest.id = entrance_id
        self.store_facade.onlineGuests[str(entrance_id)] = guest
        self.store_facade.leaveAsGuest(entrance_id)
        self.assertNotIn(str(entrance_id), self.store_facade.onlineGuests)

    def test_logInAsMember_existing_user(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member

        # call login function
        logged_in_member = self.store_facade.logInAsMember(self.username, self.password)

        # check that the member is logged in
        self.assertTrue(logged_in_member.get_logged())

    def test_logInAsMember_non_existing_user(self):
        # call login function for non-existing user
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember("non_existing_user", self.password)

    def test_logInAsMember_wrong_password(self):
        # add member to members dictionary
        self.store_facade.members[self.username] = self.member

        # call login function with wrong password
        with self.assertRaises(SystemError):
            self.store_facade.logInAsMember(self.username, "wrong_password")

    def test_logOut_member_exists(self):
        username = "test_user111"
        password = "password123"
        member = Member(username, password, "testingEmail@gmail.com")
        self.store_facade.members[username] = member
        member.logInAsMember()
        self.store_facade.logOut(username)
        self.assertFalse(member.get_logged())

    def test_logOut_member_does_not_exist(self):
        # Try to log out a member that does not exist
        username = "nonexistent_user"
        self.store_facade.logOut(username)
        self.assertTrue(True)

    def test_getMemberPurchaseHistory_returns_transaction_history_for_valid_username(self):
        # Arrange
        test_username = "test_user"
        # TODO: create a mock TransactionHistory and add some transactions for the test user

        # Act
        result = self.store_facade.getMemberPurchaseHistory(test_username)

        # Assert
        # TODO: add assertions to verify that the correct TransactionHistory is returned

    def test_getMemberPurchaseHistory_returns_none_for_invalid_username(self):
        # Arrange
        test_username = "invalid_user"

        # Act
        result = self.store_facade.getMemberPurchaseHistory(test_username)

        # Assert
        self.assertIsNone(result)

    def test_getMemberPurchaseHistory_raises_error_if_user_is_not_logged_in(self):
        # Arrange
        test_username = "test_user"
        # TODO: log the test user out

        # Act & Assert
        with self.assertRaises(Exception):
            self.store_facade.getMemberPurchaseHistory(test_username)

    def test_get_basket(self):
        # test with invalid username, should return None
        self.assertIsNone(self.store_facade.getBasket("invalid_username", "Store1"))

        # test with valid username and storename, should return a Cart object
        basket = self.store_facade.getBasket("JohnDoe", "Store1")
        self.assertIsInstance(basket, Cart)


if __name__ == '__main__':
    unittest.main()
