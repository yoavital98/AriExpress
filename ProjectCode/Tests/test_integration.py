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
        pass

    # TODO need to add default config for all Service() calls
    # config = "../de fault_config.json"
    # Service(config)
    """ ---------------------- (1) system functionality tests ---------------------- """

    #  Use Case 1.1
    def test_starting_the_market_system_success(self):
        service = Service()
        self.assertNotEqual(service.store_facade.admins.__len__(), 0)

    # Use Case 1.2

    def test_AddSetUpdate_connection_with_supply_service_success(self):
        service = Service()
        self.assertTrue(
            service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # add new address
        service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.111webhostapp.com/",
                                                                      "new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address(
            "new_name") == "https://php-server-try.111webhostapp.com/")
        # set address with wrong name
        service.store_facade.supply_service.set_request_address("wrong_name")
        self.assertTrue(
            service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # set address with correct name
        service.store_facade.supply_service.set_request_address("new_name")
        self.assertTrue(
            service.store_facade.supply_service.get_request_address() == "https://php-server-try.111webhostapp.com/")
        # update address of new_name
        service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.222webhostapp.com/",
                                                                      "new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address(
            "new_name") == "https://php-server-try.222webhostapp.com/")
        service.store_facade.supply_service.set_request_address("new_name")
        self.assertTrue(
            service.store_facade.supply_service.get_request_address() == "https://php-server-try.222webhostapp.com/")

    def test_AddSetUpdate_connection_with_payment_service_success(self):
        service = Service()
        self.assertTrue(
            service.store_facade.payment_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # add new address
        service.store_facade.payment_service.addUpdate_request_address("https://php-server-try.111webhostapp.com/",
                                                                       "new_name")
        self.assertTrue(service.store_facade.payment_service.get_request_address(
            "new_name") == "https://php-server-try.111webhostapp.com/")
        # set address with wrong name
        service.store_facade.payment_service.set_request_address("wrong_name")
        self.assertTrue(
            service.store_facade.payment_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # set address with correct name
        service.store_facade.payment_service.set_request_address("new_name")
        self.assertTrue(
            service.store_facade.payment_service.get_request_address() == "https://php-server-try.111webhostapp.com/")
        # update address of new_name
        service.store_facade.payment_service.addUpdate_request_address("https://php-server-try.222webhostapp.com/",
                                                                       "new_name")
        self.assertTrue(service.store_facade.payment_service.get_request_address(
            "new_name") == "https://php-server-try.222webhostapp.com/")
        service.store_facade.payment_service.set_request_address("new_name")
        self.assertTrue(
            service.store_facade.payment_service.get_request_address() == "https://php-server-try.222webhostapp.com/")

    # Use Case 1.3 & 1.4

    def setup_purchase(self):
        self.service = Service()
        self.service.register("Feliks", "password456", "feliks@gmail.com")
        self.service.register("Amiel", "password789", "amiel@gmail.com")
        self.service.register("YuvalMelamed", "PussyDestroyer69", "fuck@gmail.com")
        self.service.logIn("Feliks", "password456")
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")

    def test_request_to_payment_supply_success(self):
        self.setup_purchase()
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("0", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())

    # Use case 1.5 & 1.6

    def test_notification_to_store_founder_and_user(self):
        self.setup_purchase()
        self.service.logIn("Amiel", "password789")
        self.service.logIn("Feliks", "password456")
        notification_amount_amiel = self.service.getAllNotifications("Amiel").__len__()
        notification_amount_feliks = self.service.getAllNotifications("Feliks").__len__()
        self.service.logOut("Feliks")
        self.assertTrue(notification_amount_amiel == 0)
        self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789", "be'er sheva",
                                  "beer sheva", "israel", "1234152")
        notification_amount_amiel = self.service.getAllNotifications("Amiel").__len__()
        self.assertTrue(notification_amount_amiel == 1)
        self.service.logIn("Feliks", "password456")
        notification_amount_founder = self.service.getAllNotifications("Feliks").__len__()
        self.assertTrue(notification_amount_founder == notification_amount_feliks + 1)

    # Use case 1.7

    def test_notify_user_at_success_and_error(self):
        self.setup_purchase()
        self.service.logIn("Amiel", "password789")
        self.service.logIn("Feliks", "password456")
        self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        res = self.service.purchaseCart("Amiel", "4580020345672134", "12/20", "Amiel Saad", "555", "123456789",
                                        "be'er sheva",
                                        "beer sheva", "israel", "1234152")
        self.assertFalse(res.getStatus())
        res = self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                        "be'er sheva",
                                        "beer sheva", "israel", "1234152")
        self.assertTrue(res.getStatus())

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

    # ---------------------------------member functionality tests---------------------------------

    # Use Case 2.1.3
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


# Use Case 2.1.4
class Test_Use_Case_2_1_4(TestCase):

    def setUp(self):
        self.service = Service()

    def test_login_to_the_system_success(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())

    def test_logging_in_the_system_failure(self):
        # there is no way to fail this
        pass

    # Use Case 2.2.1


class Test_Use_Case_2_guests(TestCase):
    def setUp(self):
        self.service = Service()
        self.service.register("Feliks", "password456", "feliks@gmail.com")
        self.service.register("Amiel", "password789", "amiel@gmail.com")
        self.service.register("YuvalMelamed", "PussyDestroyer69", "fuck@gmail.com")
        self.service.logIn("Feliks", "password456")
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")
        self.service.logOut("Feliks")

    def test_guest_information_fetching(self):
        res_guest = self.service.loginAsGuest()
        self.assertTrue(res_guest.getStatus())
        res_product = self.service.getProductsByStore("Feliks&Sons", "0")
        self.assertTrue(res_product.getStatus())

    def test_guest_information_fetching_noSuchStore_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.getProductsByStore("some_store", "0")
        self.assertFalse(res_product.getStatus())

    def test_guest_information_fetching_noSuchProduct_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.getProduct("some_store", 5, 1)
        self.assertFalse(res_product.getStatus())

    # Use Case 2.2.2
    # Pre-conditions: User defined as guest is connected to the system
    # Post-conditions: None.
    # Flow:
    #   User types a certain product name/category/keyword on the search bar.
    #   The system iterates over the stores and looks for a product that fits the description.
    #   If OK:
    #       The system returns the results of all the products that fits the description.
    #   Else:
    #       The system returns a message that there is no products for that description.

    def test_guest_product_search_by_name(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.productSearchByName("paper", "0")
        self.assertTrue(res.getStatus())

    def test_guest_product_search_by_category(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        products = self.service.productSearchByCategory("paper", "0")

        self.assertTrue(products.getStatus())

    def test_guest_product_search_by_name_fail(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_product = self.service.productSearchByName("some_name", "0")
        self.assertTrue(res.getStatus())

    def test_guest_product_search_by_category_fail(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        products = self.service.productSearchByCategory("some_category", "0")

        self.assertTrue(products.getStatus())

    # def test_guest_product_search_by_keyword(self):
    #     guest = self.Service.loginAsGuest()
    #     products = self.Service.productFilterByFeatures("keyword1")
    #     self.assertTrue(len(products) > 0)

    # Use Case 2.2.3

    def test_guest_add_product_to_cart_success(
            self):  # TODO: check the todo in storeFacade under the productSearchByName function
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())

    def test_guest_add_product_to_cart_productDoesntExists_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 2, 5)
        self.assertFalse(res_added_product.getStatus())

    def test_guest_add_product_to_cart_StoreDoesntExists_failure(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "some_store", 1, 5)
        self.assertFalse(res_added_product.getStatus())

    def test_member_add_product_to_cart_success(self):
        res = self.service.logIn("Amiel", "password789")
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())

    # Use Case 2.2.4.a

    def test_guest_getBasket_success(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_basket = self.service.getBasket('0', "Feliks&Sons")
        self.assertTrue(res_basket.getStatus())

    # Use Case 2.2.4.b
    def test_guest_editBasket_success(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_basket = self.service.editBasketQuantity('0', "Feliks&Sons", 1, 7)
        self.assertTrue(res_basket.getStatus())

    def test_guest_editBasket_itemDoesntExists_fail(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_basket = self.service.editBasketQuantity('0', "Feliks&Sons", 2, 7)
        self.assertFalse(res_basket.getStatus())

    def test_guest_editBasket_BasketDoesntExists_fail(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_basket = self.service.editBasketQuantity('0', "some", 1, 7)
        self.assertFalse(res_basket.getStatus())

    # Use Case 2.2.5.a

    def test_guest_purchaseCart_success(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("0", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())

    def test_guest_purchaseCart_UserDoesntExists_fail(self):
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("5", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                                 "be'er sheva")
        self.assertFail(res_purchase.getStatus())

    # Use Case 2.2.5.b,c guests cant participate in bids
    def test_guest_purchaseConfirmedBid_success(self):
        pass
        # todo: ver 3


class Test_Use_Case_3_members(TestCase):
    def setUp(self):
        self.service = Service()
        self.service.register("username", "password", "email")

    # Use Case 3.1.1
    def test_login_to_the_system_success(self):
        res = self.service.logIn("username", "password")
        self.assertTrue(res.getStatus())
        return_value = res.getReturnValue()
        self.assertTrue(return_value.get('email') == 'email')
        self.assertTrue(return_value.get('entrance_id') == '0')
        self.assertTrue(return_value.get('username') == 'username')

    def test_logging_in_the_system_wrongPassword_failure(self):
        res = self.service.logIn("username", "passwo")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't log in")

    def test_logging_in_the_system_wrongUserName_failure(self):
        res = self.service.logIn("userna", "password")
        self.assertIsInstance(res.getReturnValue(), Exception, "The system shouldn't log in")

    # Use Case 3.1.2
    def test_log_out_from_the_system_success(self):
        res = self.service.logIn("username", "password")
        self.assertTrue(res.getStatus())
        res_logout = self.service.logOut("username")
        self.assertTrue(res_logout.getStatus())

    def test_log_out_from_the_system_userDoesntExists_fail(self):
        res = self.service.logIn("username", "password")
        self.assertTrue(res.getStatus())
        res_logout = self.service.logOut("userna")
        self.assertFalse(res_logout.getStatus())

    # Use Case 3.2
    def test_createShop_Success(self):
        res = self.service.logIn("username", "password")
        self.assertTrue(res.getStatus())
        res_create_store = self.service.createStore("username", "Feliks&Sons")
        self.assertTrue(res_create_store.getStatus())

    def test_createShop_notLoggedIn_fail(self):
        res_create_store = self.service.createStore("username", "Feliks&Sons")
        self.assertFalse(res_create_store.getStatus())


class Test_Use_Case_4_Management(TestCase):
    def setUp(self):
        self.service = Service()
        self.service.register("Feliks", "password456", "feliks@gmail.com")
        self.service.register("Amiel", "password789", "amiel@gmail.com")
        res = self.service.logIn("Feliks", "password456")
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.logOut("Feliks")

    # Use Case 4.1.a
    def test_addProductToStore_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_new_product = self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")
        self.assertTrue(res_new_product.getStatus())

    # Use Case 4.1.b

    def test_deleteProductFromStore_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_new_product = self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")
        self.assertTrue(res_new_product.getStatus())
        res_delete = self.service.removeProductFromStore("Feliks", "Feliks&Sons", 1)
        self.assertTrue(res_delete.getStatus())

    # Use Case 4.1.c
    def test_changeProductinStore_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_new_product = self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")
        self.assertTrue(res_new_product.getStatus())
        res_edit = self.service.editProductOfStore("Feliks", "Feliks&Sons", 1, quantity=50)
        self.assertTrue(res_edit.getStatus())

    # Use Case 4.4
    def test_nominateShopOwner_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreOwner("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())

    # Use Case 4.6
    def test_nominateShopManager_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreManager("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())

    # Use Case 4.7
    def test_addPermissionToShopManager_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreManager("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())
        res_permission = self.service.addPermission("Feliks&Sons", "Feliks", "Amiel", "ModifyPermissions")
        self.assertTrue(res_permission.getStatus())

    # Use Case 4.8
    def test_removePermissionToShopManager_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreManager("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())
        res_permission = self.service.removePermissions("Feliks&Sons", "Feliks", "Amiel", "Bid")
        self.assertTrue(res_permission.getStatus())

    def test_removePermissionToShopManager_Fail(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreManager("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())
        res_permission = self.service.removePermissions("Feliks&Sons", "Feliks", "Amiel", "StaffInfo")
        self.assertFalse(res_permission.getStatus())

    # Use Case 4.9
    def test_closeStore_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_close = self.service.closeStore("Feliks", "Feliks&Sons")
        self.assertTrue(res_close.getStatus())

    # Use Case 4.11.a

    def test_requestStoreStaffInfo_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res_info = self.service.getStaffInfo("Feliks", "Feliks&Sons")
        self.assertTrue(res_info.getStatus())

    # Use Case 4.13

    def test_requestStorePurchaseHistory_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", 50, 100, "paper")
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("0", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())
        res_purchase_history = self.service.getStorePurchaseHistory("Feliks", "Feliks&Sons")
        self.assertTrue(res_purchase_history.getStatus())

    # Use Case 5
    def test_nominatedPreformingAction_Success(self):
        res = self.service.logIn("Feliks", "password456")
        self.assertTrue(res.getStatus())
        res = self.service.logIn("Amiel", "password789")
        self.assertTrue(res.getStatus())
        res_nominate = self.service.nominateStoreManager("Feliks", "Amiel", "Feliks&Sons")
        self.assertTrue(res_nominate.getStatus())
        res_request = self.service.addNewProductToStore("Amiel", "Feliks&Sons", "paper", 50, 100, "paper")
        self.assertTrue(res_request.getStatus())
        res_request = self.service.removeProductFromStore("Amiel", "Feliks&Sons", 1)
        self.assertTrue(res_request.getStatus())

    # Use Case 6.4

    def test_StorePurchaseHistoryAdmin_success(self):
        res = self.service.logIn("Feliks", "password456")
        self.service.loginAsGuest()
        res_admin = self.service.logIn("admin", "12341234")
        self.assertTrue(res.getStatus())
        self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", "paper", 50, 100)
        res_added_product = self.service.addToBasket('0', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("0", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())
        res_purchase_history = self.service.getStorePurchaseHistory("admin", "Feliks&Sons")
        self.assertTrue(res_purchase_history.getStatus())

    # Use Case 6.4

    def test_UserPurchaseHistoryAdmin_success(self):
        res = self.service.logIn("Feliks", "password456")
        res_admin = self.service.logIn("admin", "12341234")
        res_amiel = self.service.logIn("Amiel", "password789")
        self.assertTrue(res.getStatus())
        self.assertTrue(res_admin.getStatus())
        self.service.createStore("Feliks", "Feliks&Sons")
        self.service.addNewProductToStore("Feliks", "Feliks&Sons", "paper", "paper", 50, 100)
        res_added_product = self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())
        res_purchase_history = self.service.getMemberPurchaseHistory("admin", "Amiel")
        self.assertTrue(res_purchase_history.getStatus())


if __name__ == '__main__':
    unittest.main()
