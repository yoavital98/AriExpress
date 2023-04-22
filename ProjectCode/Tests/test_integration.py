import unittest
from unittest import TestCase
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects import Guest
from ProjectCode.Domain.Objects.UserObjects.Guest import Guest
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
            self.Service.openTheSystem("Ari")
        except SystemError:
            pass

    #Use Case 1.2



    # ----------------------guest functionality tests----------------------


    # Use Case 2.1.1
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

    # Use Case 2.1.2
    # Pre - conditions: User is in the market as guest.
    # Post - conditions: User loses his basket.
    # Flow:
    #   The user exists the system.
    #   The system removes the user cart.
    def test_guest_exit_success(self):
        guest = self.Service.loginAsGuest()
        self.Service.leasveAsGuest(guest)
        self.assertNotIn(guest, self.Service.store_facade.onlineGuests)

    #---------------------------------member functionality tests---------------------------------

    #Use Case 2.1.3
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


    #Use Case 2.1.4
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
        member = self.Service.logIn("username", "password")
        self.assertTrue(member.get_logged())

    def test_logging_in_the_system_failure(self):
        try:
            self.Service.register("username", "password", "email")
            self.Service.login("username", "password")
            self.Service.login("username", "password")
        except SystemError:
            pass

    #Use Case 2.2.1
    #Pre-conditions: User defined as a guest.
    #Post-conditions: User gets the information about the stores and products.
    #Flow:
    #   User enters a store in the market.
    #   The system fetches the requested store.
    #   If OK:
    #       The system returns to the user all the products information.
    #   Else:
    #       The system returns an error that no such store exists.

    def test_guest_information_fetching(self):
        guest = self.Service.loginAsGuest()
        stores = self.Service.getStores()
        store_name = stores[0].get_store_name()  #TODO: check why doest this line doesn't work (something about way we access an object in list)
        products = self.Service.getProductsByStore(store_name)
        self.assertTrue(len(products) > 0)

    def test_guest_information_fetching_failure(self):
        guest = self.Service.loginAsGuest()
        try:
            self.Service.getProductsByStore("storename_that_doesn't_exist")
        except SystemError:
            pass

    #Use Case 2.2.2
    #Pre-conditions: User defined as guest is connected to the system
    #Post-conditions: None.
    #Flow:
    #   User types a certain product name/category/keyword on the search bar.
    #   The system iterates over the stores and looks for a product that fits the description.
    #   If OK:
    #       The system returns the results of all the products that fits the description.
    #   Else:
    #       The system returns a message that there is no products for that description.

    def test_guest_product_search_by_name(self): #TODO: check the todo in storeFacade under the productSearchByName function
        guest = self.Service.loginAsGuest()
        products = self.Service.productSearchByName("product1")
        self.assertTrue(len(products) > 0)

    def test_guest_product_search_by_category(self):
        guest = self.Service.loginAsGuest()
        products = self.Service.productSearchByCategory("category1")
        self.assertTrue(len(products) > 0)

    def test_guest_product_search_by_keyword(self):
        guest = self.Service.loginAsGuest()
        products = self.Service.productFilterByFeatures("keyword1")
        self.assertTrue(len(products) > 0)

    #Use Case 2.2.3
    #Pre-conditions: User defined as a guest is connected to the system.
    #Post-conditions: User basket filled with the products he added.
    #Flow:
    #   User adds a specific product to the basket.
    #   The system looks for the product id that corresponds to the store id.
    #   The system checks if there is an existing basket for the specific store.
    #   If OK:
    #       The system adds the product to the basket.
    #   Else:
    #       The system creates a new basket for the user.
    #       The system adds the product to the basket.
    def test_guest_add_product_to_cart_success(self): #TODO: check the todo in storeFacade under the productSearchByName function
        guest = self.Service.loginAsGuest()
        products = self.Service.productSearchByName("product1")
        product_id = products[0].get_product_id()
        self.Service.addToBasket(guest.get_username(), "storename", product_id, 1)

    def test_guest_add_product_to_cart_failure(self):
        guest = self.Service.loginAsGuest()
        try:
            self.Service.addToBasket(guest.get_username(), "storename", "product_id", 100)
        except SystemError:
            pass


if __name__ == '__main__':
    unittest.main()
