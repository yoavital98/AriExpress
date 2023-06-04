import unittest
from unittest import TestCase
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.DataObjects.DataGuest import DataGuest
from ProjectCode.Domain.DataObjects.DataMember import DataMember
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Service.Service import Service
from ProjectCode.Service.Response import Response


class Test_Use_Cases_1(TestCase):
    def setUp(self):

        self.Service = Service()

    # ----------------------sysyem functionality tests----------------------
    #Use Case 1.1
    def testing_starting_the_market_system_success(self):

        self.Service.login("Ari", "123")
        res = self.Service.openTheSystem("Ari")
        self.assertEqual(res, None, "The system is not open")

    def testing_starting_the_market_system_failure(self):

        res = self.Service.openTheSystem("Rubin")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't open")

    #Use Case 1.2

    def tearDown(self):
        #self.Service.closeTheSystem()
        pass

    # ----------------------guest functionality tests----------------------

class Test_Use_Cases_2_1(TestCase):
    def setUp(self):

        self.Service = Service()

    # Use Case 2.1.1
    def test_guest_visit_success(self):
            
        res = self.Service.loginAsGuest()
        self.assertIsInstance(res.getReturnValue(), DataGuest, "the return value is not a guest - an error occured")

    def test_guest_visit_failure(self):

        # TODO: wait for Ari's code
        pass

    # Use Case 2.1.2
    def test_guest_exit_success(self):

        dataGuest = self.Service.loginAsGuest()
        res =self.Service.leaveAsGuest(dataGuest)
        self.assertEquals(res.getReturnValue(), None, "the return value is not None - an error occured")

        #---------------------------------member functionality tests---------------------------------

    #Use Case 2.1.3
    def test_registration_to_the_system_success(self):

        res = self.Service.register("username22", "password", "email")
        self.assertIsInstance(res.getReturnValue(), DataMember, "the return value is not a member - an error occured")

    def test_registration_to_the_system_failure(self):

        self.Service.register("username", "password", "email")
        res = self.Service.register("username", "password", "email")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't register")



 #Use Case 2.1.4
class Test_Use_Case_2_1_4(TestCase):

    def setUp(self):
        self.Service = Service()
        self.Service.register("username", "password", "email")


    def test_login_to_the_system_success(self):

        res = self.Service.login("username", "password")
        self.assertTrue(res.getReturnValue().get_login_status(), "The user is not logged in")

    def test_logging_in_the_system_failure(self):
        self.Service.login("username", "password")
        res = self.Service.login("username", "password")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't log in")


    #Use Case 2.2.1
class Test_Use_Case_2_2(TestCase):
    def setUp(self):

        self.Service = Service()
        self.Service.register("username", "password", "email")
        self.Service.register("rubin_krief", "h9reynWq", "roobink@post.bgu.ac.il")
        self.Service.logIn("username", "password")
        res = self.Service.createStore("username", "roobs_store")
        print(res.getReturnValue())
        self.Service.addNewProductToStore("username", "roobs_store", "product1", "category", 10, 10)
        self.Service.addNewProductToStore("username", "roobs_store", "product2", "category", 10, 10)
        self.Service.logIn("rubin_krief", "h9reynWq")

        

    def test_guest_information_fetching(self):
        res_guest = self.Service.loginAsGuest()
        stores = self.Service.getStores().getReturnValue()
        store_name = stores[0].get_store_name()  #TODO: check why doest this line doesn't work (something about way we access an object in list)
        products = self.Service.getProductsByStore(store_name).getReturnValue()
        self.assertTrue(len(products) > 0)

    def test_guest_information_fetching_failure(self):
        guest = self.Service.loginAsGuest()
        try:
            self.Service.getProductsByStore("storename_that_doesn't_exist")
        except Exception:
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

    def test_guest_add_product_to_cart_success(self): #TODO: check the todo in storeFacade under the productSearchByName function
        guest = self.Service.loginAsGuest()
        products = self.Service.productSearchByName("product1")
        product_id = products[0].get_product_id()
        self.Service.addToBasket(guest.get_username(), "storename", product_id, 1)


    def test_guest_add_product_to_cart_failure(self):
        guest = self.Service.loginAsGuest()
        try:
            self.Service.addToBasket(guest.get_username(), "storename", "product_id", 100)
        except Exception:
            pass

    def test_user_add_product_to_cart_success(self):
        res = self.Service.addToBasket("rubin_krief", "roobs_store", 1, 1)
        print(res.getReturnValue())
        self.assertTrue(res.getStatus())


if __name__ == '__main__':
    unittest.main()
