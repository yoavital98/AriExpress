import unittest
from unittest import TestCase
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.DataObjects.DataGuest import DataGuest
from ProjectCode.Domain.DataObjects.DataMember import DataMember
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Service.Service import Service
from ProjectCode.Service.Response import Response


class Test_Use_Cases_1(TestCase):
    def setUp(self):
        self.Service = Service()

    # ----------------------sysyem functionality tests----------------------
    #Use Case 1.1
    # def testing_starting_the_market_system_success(self):
    #
    #     self.Service.login("Ari", "123")
    #     res = self.Service.openTheSystem("Ari")
    #     self.assertEqual(res, None, "The system is not open")
    #
    # def testing_starting_the_market_system_failure(self):
    #
    #     res = self.Service.openTheSystem("Rubin")
    #     self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't open")

    #Use Case 1.2

#    def tearDown(self):
        #self.Service.closeTheSystem()
 #       pass
    #Use Case 1.3

    # ----------------------guest functionality tests----------------------

class Test_Use_Cases_2_1(TestCase):
    def setUp(self):

        self.Service = Service()

    # Use Case 2.1.1
    def test_guest_visit_success(self):
            
        res = self.Service.loginAsGuest()
        self.assertTrue(res.getStatus())
        return_value = res.getReturnValue()
        self.assertTrue(return_value == '{"entrance_id": "0"}')


    def test_guest_visit_failure(self):
        # cannot fail!
        pass

    # Use Case 2.1.2
    def test_guest_exit_success(self):
        pass

    #---------------------------------member functionality tests---------------------------------

    #Use Case 2.1.3
    def test_registration_to_the_system_success(self):

        res = self.Service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        return_value: dict = res.getReturnValue()
        self.assertTrue(return_value.get('email') == 'email')
        self.assertTrue(return_value.get('entrance_id') == '0')
        self.assertTrue(return_value.get('username') == 'username22')

    def test_registration_to_the_system_failure(self):

        res = self.Service.register("username", "password", "email")
        self.assertTrue(res.getStatus())
        res = self.Service.register("username", "password", "email")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't register")



 #Use Case 2.1.4
class Test_Use_Case_2_1_4(TestCase):

    def setUp(self):
        self.Service = Service()
        self.Service.register("username", "password", "email")


    def test_login_to_the_system_success(self):

        res = self.Service.logIn("username", "password")
        self.assertTrue(res.getStatus())
        return_value = res.getReturnValue()
        self.assertTrue(return_value.get('email') == 'email')
        self.assertTrue(return_value.get('entrance_id') == '0')
        self.assertTrue(return_value.get('username') == 'username')

    def test_logging_in_the_system_failure(self):
        res = self.Service.logIn("username", "passwo")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't log in")


    #Use Case 2.2.1
class Test_Use_Case_2_2(TestCase):
    def setUp(self):
        self.service = Service()
        self.service.register("Feliks", "password456", "feliks@gmail.com")
        self.service.register("Amiel", "password789", "amiel@gmail.com")
        self.service.register("YuvalMelamed", "PussyDestroyer69", "fuck@gmail.com")
        self.service.logIn("Feliks", "password456")
        self.service.createStore("Feliks", "AriExpress")
        self.service.addNewProductToStore("Feliks","AriExpress", "paper", "paper", 50, 100)
        self.service.logOut("Feliks")

        

    def test_guest_information_fetching(self):
        res_guest = self.service.loginAsGuest()
        self.assertTrue(res_guest.getStatus())
        res_product = self.service.getProductsByStore("AriExpress", "0")
        self.assertTrue(res_product.getStatus())


    def test_guest_information_fetching_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.getProductsByStore("some_store", "0")
        self.assertFalse(res_product.getStatus())


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
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.productSearchByName("paper", "0")
        self.assertTrue(res.getStatus())

    def test_guest_product_search_by_category(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        products = self.service.productSearchByName("paper", "0")
        self.assertTrue(products.getStatus())

    # def test_guest_product_search_by_keyword(self):
    #     guest = self.Service.loginAsGuest()
    #     products = self.Service.productFilterByFeatures("keyword1")
    #     self.assertTrue(len(products) > 0)

    #Use Case 2.2.3

    def test_guest_add_product_to_cart_success(self): #TODO: check the todo in storeFacade under the productSearchByName function
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "AriExpress", 1, 5)
        self.assertTrue(res_added_product.getStatus())


    def test_guest_add_product_to_cart_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "AriExpress", 0, 5)
        self.assertFalse(res_added_product.getStatus())

    def test_member_add_product_to_cart_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('Feliks', "AriExpress", 0, 5)
        self.assertFalse(res_added_product.getStatus())







if __name__ == '__main__':
    unittest.main()
