import unittest
from unittest import TestCase
from ProjectCode.Service.Service import Service

default_config = "../../default_config.json"
stores_config  = "../../config_acceptanceTests2StoresNoWorkers.json"
true_lambda = lambda self, receiver_id, notification_id, type, subject: True

class Test_Use_Cases_1(TestCase):
    default_config = "../../default_config.json"
    stores_config = "../../config_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        pass

    # TODO need to add default config for all Service(default_config) calls
    # Service(config)
    """ ---------------------- (1) system functionality tests ---------------------- """

    #  Use Case 1.1
    def test_starting_the_market_system_success(self):
        service = Service(default_config, true_lambda)
        self.assertNotEqual(service.store_facade.admins.__len__(), 0)

    # Use Case 1.2

    def test_AddSetUpdate_connection_with_supply_service_success(self):
        service = Service(default_config, true_lambda)
        self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # add new address
        service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.111webhostapp.com/","new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address("new_name") == "https://php-server-try.111webhostapp.com/")
        # set address with wrong name
        service.store_facade.supply_service.set_request_address("wrong_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
        # set address with correct name
        service.store_facade.supply_service.set_request_address("new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.111webhostapp.com/")
        # update address of new_name
        service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.222webhostapp.com/", "new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address("new_name") == "https://php-server-try.222webhostapp.com/")
        service.store_facade.supply_service.set_request_address("new_name")
        self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.222webhostapp.com/")

    def test_AddSetUpdate_connection_with_payment_service_success(self):
        service = Service(default_config, true_lambda)
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
        self.service = Service(default_config, true_lambda)
        self.service.register("Feliks", "password456", "feliks@gmail.com")
        self.service.register("Amiel", "password789", "amiel@gmail.com")
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
    default_config = "../../default_config.json"
    stores_config = "../../config_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        self.service = Service(self.stores_config, true_lambda)
    # Use Case 2.1.1
    def test_guest_visit_success(self):
        # TODO 00 - check that a guest is trackable, can know when logged out to system, etc.
        # a guest can (1) visit the system (2) have a cart
        # (3) add products to it (4) and purchase it.
        # =============================================
        self.setUp()
        # (1)
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        guest1_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.assertTrue(guest0_entrance_id == 0)
        self.assertTrue(guest1_entrance_id == 1)
        # (2)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["username"] == "2")
        self.assertTrue(self.service.getCart(guest1_entrance_id).getReturnValue()["username"] == "3")
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        self.assertTrue(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"] == [])
        # (3)
        feliks_product_1_quantity = self.service.getProduct("Feliks&Sons", 1, "Feliks").getReturnValue()["quantity"]
        robin_product_1_quantity = self.service.getProduct("Robin&daughters", 1, "Robin").getReturnValue()["quantity"]
        robin_product_2_quantity = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 3)
        self.service.addToBasket(guest0_entrance_id, "Robin&daughters", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Robin&daughters", 2, 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 8)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["store"] == "Robin&daughters")
        self.assertTrue(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        # (4)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                       "some_address", "be'er sheva", "Israel", "1234567")
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        feliks_product_1_quantity_after = self.service.getProduct("Feliks&Sons", 1, "Feliks").getReturnValue()["quantity"]
        robin_product_1_quantity_after = self.service.getProduct("Robin&daughters", 1, "Robin").getReturnValue()["quantity"]
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.assertTrue(feliks_product_1_quantity_after == feliks_product_1_quantity - 8)
        self.assertTrue(robin_product_1_quantity_after == robin_product_1_quantity - 5)
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    # Use Case 2.1.2
    def test_guest_exit_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        robin_product_2_quantity = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Robin&daughters", 2, 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 2)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    # ---------------------------------member functionality tests---------------------------------

    # Use Case 2.1.3
    def test_registration_to_the_system_success(self):
        self.setUp()
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        self.assertTrue(self.service.getMemberInfo("admin", "username22")["name"] == "username22")

    def test_registration_to_the_system_failure(self):
        self.setUp()
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        with self.assertRaises(Exception):
            self.service.register("username22", "password1", "email")


    # Use Case 2.1.4

    def test_login_to_the_system_success(self):
        self.setUp()
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        member_res = self.service.logIn("username22", "password1")
        self.assertTrue(member_res.getReturnValue()['name'] == 'username22')
        self.assertTrue(member_res.getReturnValue()['email'] == 'email')

    def test_logging_in_the_system_failure(self):
        self.setUp()
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        with self.assertRaises(Exception):
            self.service.logIn("username22", "password2")
class Test_Use_Case_2_2(TestCase):
    default_config = "../../default_config.json"
    stores_config = "../../config_acceptanceTests2StoresNoWorkers.json"
    def setUp(self):
        self.service = Service(self.stores_config, true_lambda)

    # Use Case 2.2.1
    def test_guest_information_fetching(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        store_count = self.service.getStoresBasicInfo().getReturnValue().__len__()
        self.assertTrue(store_count == 2)
        feliks_products = self.service.getStoreProductsInfo("Feliks&Sons").getReturnValue()["products"].__len__()
        self.assertTrue(feliks_products == 12)
        product1 = self.service.getProduct("Feliks&Sons", 1, guest0_entrance_id)
        self.assertTrue(product1.getReturnValue()["name"] == "Cabbage_K")
    def test_guest_information_fetching_noSuchStore_failure(self):
        self.setUp()
        res = self.service.loginAsGuest()
        store_count = self.service.getStoresBasicInfo().getReturnValue().__len__()
        self.assertTrue(store_count == 2)
        with self.assertRaises(Exception):
            self.service.getStoreProductsInfo("Ari&Bears")

    def test_guest_information_fetching_noSuchProduct_failure(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        store_count = self.service.getStoresBasicInfo().getReturnValue().__len__()
        self.assertTrue(store_count == 2)
        feliks_products = self.service.getStoreProductsInfo("Feliks&Sons").getReturnValue()["products"].__len__()
        self.assertTrue(feliks_products == 12)
        with self.assertRaises(Exception):
            self.service.getProduct("Feliks&Sons", 15, guest0_entrance_id)

    # Use Case 2.2.2

    def test_guest_product_search_by_name(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_product = self.service.productSearchByName("Ca", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Feliks&Sons"].__len__() == 3) # Cabbage, Cauliflower, Carrot
        with self.assertRaises(Exception):
            x = res_product.getReturnValue()["Robin&Daughters"] # None in Ca

    def test_guest_product_search_by_category(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_product = self.service.productSearchByCategory("Sauces", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Robin&Daughters"].__len__() == 5) # 5 Sauces
        with self.assertRaises(Exception):
            x = res_product.getReturnValue()["Feliks&Sons"] # None in Feliks's

    def test_guest_product_search_by_features_price(self):
        #TODO
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_products_below10 = self.service.productFilterByFeatures({"min price": 0, "max price": 10}, guest0_entrance_id)
        res_products_below5 = self.service.productFilterByFeatures({"min price": 0, "max price": 5}, guest0_entrance_id)
        self.assertTrue(res_products_below10.getReturnValue()["Feliks&Sons"].__len__() == 11) # All products
        self.assertTrue(res_products_below10.getReturnValue()["Robin&Daugthers"].__len__() == 3) # 6 products
        self.assertTrue(res_products_below5.getReturnValue()["Robin&Daugthers"].__len__() == 3) # 6 products
        with self.assertRaises(Exception):
            x = res_products_below5.getReturnValue()["Feliks&Sons"] # None in Feliks's
        with self.assertRaises(Exception):
            x = self.service.productFilterByFeatures({"Size": 0}, guest0_entrance_id)


    # Use Case 2.2.3

    def test_guest_add_product_to_cart_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        robin_product_2_quantity = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Robin&daughters", 2, 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 2)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

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
class Test_Use_Case_2_3_members(TestCase):
    def setUp(self):
        self.service = Service(default_config, true_lambda)
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
class Test_Use_Case_2_4_Management(TestCase):
    def setUp(self):
        self.service = Service(self.stores_config, true_lambda)
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
class Test_Use_Case_2_5_nominations(TestCase):
    def setUp(self):
        self.service = Service(self.stores_config, true_lambda)
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
class Test_Use_Case_2_6_transactions(TestCase):
    def setUp(self):
        self.service = Service(self.stores_config, true_lambda)
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
