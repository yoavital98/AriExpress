import unittest
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects import Guest
from ProjectCode.Domain.Objects.UserObjects.Admin import Admin
from ProjectCode.Domain.Objects.UserObjects.Member import Member
from ProjectCode.Service.Service import Service


class TestStoreFacade(TestCase):

    def setUp(self):

        self.Service = Service()
        self.Service.openTheSystem("Ari")
        self.Service.register("username", "password", "email")
        self.Service.logIn("username", "password")
        self.Service.openStore("username", "storename")
        self.Service.addNewProductToStore("username", "storename", "product1", "category", 10, 10)
        self.Service.addNewProductToStore("username", "storename", "product2", "category", 10, 10)


    # ----------------------sysyem functionality tests----------------------
    #Use Case 1.1
    # An admin logging into the system using his password and username of a system manager type user
    # The system checks if the user exists in the database
    # The system checks if the user is a system_manager type of user
    # The system sends a message to payment and supliment services
    # a message is being return from those services to the system
    # The system sends a message to the the user that he had connected successfuly.
    def testing_starting_the_market_system_success(self):
        self.Service.logIn("Ari", "123")
        self.Service.openTheSystem("Ari")
        self.assertNotEqual(self.Service.store_facade, None, "The system is not open")

    def testing_starting_the_market_system_failure(self):
        try:
            self.Service.openTheSystem("Ari", "002")
        except SystemError:
            pass

    #Use Case 1.2


    # ----------------------guest functionality tests----------------------

    # The user enters the market system.
    # The system checks if the type of the current user is Guest.
    # If OK:
    #    The system assigns a Cart for the user.
    # Else:
    #    The system redirects to an error page.
    def test_guest_visit_success(self):
        guest = self.Service.loginAsGuest()
        self.assertIsInstance(guest, Guest)

    def test_guest_visit_failure(self):
        # TODO: wait for Ari's code
        pass

    # Pre - conditions: User is in the market as guest.
    # Post - conditions: User loses his basket.
    # Flow:
    #   The user exists the system.
    #   The system removes the user cart.
    def test_guest_exit_success(self):
        guest = self.Service.loginAsGuest()
        ent_id = guest.entrance_id
        self.Service.logout(guest)
        self.assertNotIn(ent_id, self.Service.store_facade.onlineGuests)

    #---------------------------------member functionality tests---------------------------------

    #Pre-conditions: User is defined as a guest.
    #Post- conditions: a new member created in the system with a new member id and the registration information
    #Flow:
    #   The user enter username, password and email and send a registration request.
    #   The system validates that the type of the user is a guest.
    #   If OK:
    #       The system validates that there is no user with the same username or email.
    #   If OK:
    #       The system creates a new user and sends a confirmation to the user.
    #   else:
    #       The system returns an appropriate error.
    def test_registration_to_the_system_success(self):
        member = self.Service.register("username22", "password", "email")
        self.assertIsInstance(member, Member)

    def test_registration_to_the_system_failure(self):
        try:
            self.Service.register("username", "password", "email")

        except SystemError:
            pass


    #Pre-conditions: User is defined as a guest and has already registered to the system.
    #Post- conditions: The User status is changed from Guest to Member.
    #Flow:
    #   The user enters the market system.
    #   The user logs-in with a username and a password.
    #   The system checks if the type of the current user is Guest.
    #   The system uses an external service for password validation.
    #   If OK:
    #       The system checks that the type of the user is Member.
    #       The system return an confirmation that the operation succeed.
    #   Else:
    #       The system sends an error message that the log-in failed.
    def test_logging_in_the_system_success(self):
        self.Service.register("username", "password", "email")
        member = self.Service.login("username", "password")
        self.assertTrue(member.get_logged(member))

    def test_logging_in_the_system_failure(self):
        try:
            self.Service.register("username", "password", "email")
            self.Service.login("username", "password")
            self.Service.login("username", "password")
        except SystemError:
            pass

    #Pre-conditions: User defined as a guest.
    #Post-conditions: User gets the information about the stores and products.
    #Flow:
    #   User enters a store in the market.
    #   The system fetches the requested store.
    #   If OK:
    #       The system returns to the user all the products information.
    #   Else:
    #       The system returns an error that no such store exists.

    #def test_guest_information_fetching(self):




if __name__ == '__main__':
    unittest.main()
