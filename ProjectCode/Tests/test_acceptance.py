import unittest
from unittest import TestCase

from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Service.Service import Service

default_config = "../../default_config.json"
stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"
true_lambda = lambda self, receiver_id, notification_id, type, subject: True


class Test_Use_Cases_1(TestCase):
    default_config = "../../default_config.json"
    stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"

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

    # def test_AddSetUpdate_connection_with_supply_service_success(self):
    #     service = Service(default_config, true_lambda)
    #     self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
    #     # add new address
    #     service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.111webhostapp.com/","new_name")
    #     self.assertTrue(service.store_facade.supply_service.get_request_address("new_name") == "https://php-server-try.111webhostapp.com/")
    #     # set address with wrong name
    #     service.store_facade.supply_service.set_request_address("wrong_name")
    #     self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
    #     # set address with correct name
    #     service.store_facade.supply_service.set_request_address("new_name")
    #     self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.111webhostapp.com/")
    #     # update address of new_name
    #     service.store_facade.supply_service.addUpdate_request_address("https://php-server-try.222webhostapp.com/", "new_name")
    #     self.assertTrue(service.store_facade.supply_service.get_request_address("new_name") == "https://php-server-try.222webhostapp.com/")
    #     service.store_facade.supply_service.set_request_address("new_name")
    #     self.assertTrue(service.store_facade.supply_service.get_request_address() == "https://php-server-try.222webhostapp.com/")
    #
    # def test_AddSetUpdate_connection_with_payment_service_success(self):
    #     service = Service(default_config, true_lambda)
    #     self.assertTrue(
    #         service.store_facade.payment_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
    #     # add new address
    #     service.store_facade.payment_service.addUpdate_request_address("https://php-server-try.111webhostapp.com/",
    #                                                                    "new_name")
    #     self.assertTrue(service.store_facade.payment_service.get_request_address(
    #         "new_name") == "https://php-server-try.111webhostapp.com/")
    #     # set address with wrong name
    #     service.store_facade.payment_service.set_request_address("wrong_name")
    #     self.assertTrue(
    #         service.store_facade.payment_service.get_request_address() == "https://php-server-try.000webhostapp.com/")
    #     # set address with correct name
    #     service.store_facade.payment_service.set_request_address("new_name")
    #     self.assertTrue(
    #         service.store_facade.payment_service.get_request_address() == "https://php-server-try.111webhostapp.com/")
    #     # update address of new_name
    #     service.store_facade.payment_service.addUpdate_request_address("https://php-server-try.222webhostapp.com/",
    #                                                                    "new_name")
    #     self.assertTrue(service.store_facade.payment_service.get_request_address(
    #         "new_name") == "https://php-server-try.222webhostapp.com/")
    #     service.store_facade.payment_service.set_request_address("new_name")
    #     self.assertTrue(
    #         service.store_facade.payment_service.get_request_address() == "https://php-server-try.222webhostapp.com/")

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
    stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

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
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 8)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["store"] == "Robin&daughters")
        self.assertTrue(
            self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        # (4)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        feliks_product_1_quantity_after = self.service.getProduct("Feliks&Sons", 1, "Feliks").getReturnValue()[
            "quantity"]
        robin_product_1_quantity_after = self.service.getProduct("Robin&daughters", 1, "Robin").getReturnValue()[
            "quantity"]
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()[
            "quantity"]
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
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 2)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()[
            "quantity"]
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
    stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

    # Use Case 2.2.1
    def test_guest_information_fetching_success(self):
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

    # Use Case 2.2.2.a

    def test_guest_product_search_by_name_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_product = self.service.productSearchByName("Ca", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Feliks&Sons"].__len__() == 3)  # Cabbage, Cauliflower, Carrot
        with self.assertRaises(Exception):
            x = res_product.getReturnValue()["Robin&Daughters"]  # None in Ca

    # Use Case 2.2.2.b
    def test_guest_product_search_by_category_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_product = self.service.productSearchByCategory("Sauces", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Robin&Daughters"].__len__() == 5)  # 5 Sauces
        with self.assertRaises(Exception):
            x = res_product.getReturnValue()["Feliks&Sons"]  # None in Feliks's

    # Use Case 2.2.2.c
    def test_guest_product_search_by_features_price_success(self):
        # TODO
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        res_products_below10 = self.service.productFilterByFeatures({"min price": 0, "max price": 10},
                                                                    guest0_entrance_id)
        res_products_below5 = self.service.productFilterByFeatures({"min price": 0, "max price": 5}, guest0_entrance_id)
        self.assertTrue(res_products_below10.getReturnValue()["Feliks&Sons"].__len__() == 11)  # All products
        self.assertTrue(res_products_below10.getReturnValue()["Robin&Daugthers"].__len__() == 3)  # 6 products
        self.assertTrue(res_products_below5.getReturnValue()["Robin&Daugthers"].__len__() == 3)  # 6 products
        with self.assertRaises(Exception):
            x = res_products_below5.getReturnValue()["Feliks&Sons"]  # None in Feliks's
        with self.assertRaises(Exception):
            x = self.service.productFilterByFeatures({"Size": 0}, guest0_entrance_id)

    # Use Case 2.2.3

    def test_guest_add_product_to_cart_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        robin_product_2_quantity = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Robin&daughters", 2, 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 2)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        robin_product_2_quantity_after = self.service.getProduct("Robin&daughters", 2, "Robin").getReturnValue()[
            "quantity"]
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    def test_guest_add_product_to_cart_productDoesntExists_failure(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        with self.assertRaises(Exception):
            self.service.addToBasket(guest0_entrance_id, "Robin&daughters", 80, 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])

    def test_guest_add_product_to_cart_StoreDoesntExists_failure(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        with self.assertRaises(Exception):
            self.service.addToBasket(guest0_entrance_id, "Robin&Sons", 1, 5)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])

    # Use Case 2.2.4.a

    def test_guest_getBasket_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 1)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["store"] == "Feliks&Sons")
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["products"][0]["quantity"] == 5)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["products"][0]["id"] == 1)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["store"] == "Robin&Daughters")

    # Use Case 2.2.4.b
    def test_guest_editBasket_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        self.service.editBasketQuantity(guest0_entrance_id, "Feliks&Sons", 1, 7)
        self.service.editBasketQuantity(guest0_entrance_id, "Robin&Daughters", 1, 8)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["quantity"] == 7)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["products"][0]["id"] == 1)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][0]["store"] == "Feliks&Sons")
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["products"][0]["quantity"] == 8)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["products"][0]["id"] == 1)
        self.assertTrue(
            self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"][1]["store"] == "Robin&Daughters")

    def test_guest_editBasket_itemDoesntExists_fail(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        with self.assertRaises(Exception):
            self.service.editBasketQuantity(guest0_entrance_id, "Feliks&Sons", 2, 7)

    def test_guest_editBasket_BasketDoesntExists_fail(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        with self.assertRaises(Exception):
            self.service.editBasketQuantity(guest0_entrance_id, "Robin&Daughters", 1, 7)

    # Use Case 2.2.5.a

    def test_guest_purchaseCart_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"].__len__() == 2)
        feliks_notification_count = self.service.getNotifications("Feliks").getReturnValue().__len__()
        robin_notification_count = self.service.getNotifications("Robin").getReturnValue().__len__()
        feliks_item1_count = self.service.getStoreInfo("Feliks&Sons").getReturnValue()["items"][0]["quantity"]
        robin_item1_count = self.service.getStoreInfo("Robin&Daughters").getReturnValue()["items"][0]["quantity"]
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        feliks_notification_count_after = self.service.getNotifications("Feliks").getReturnValue().__len__()
        robin_notification_count_after = self.service.getNotifications("Robin").getReturnValue().__len__()
        feliks_item1_count_after = self.service.getStoreInfo("Feliks&Sons").getReturnValue()["items"][0]["quantity"]
        robin_item1_count_after = self.service.getStoreInfo("Robin&Daughters").getReturnValue()["items"][0]["quantity"]
        self.assertTrue(feliks_notification_count_after == feliks_notification_count + 1)
        self.assertTrue(robin_notification_count_after == robin_notification_count + 1)
        self.assertTrue(feliks_item1_count_after == feliks_item1_count - 5)
        self.assertTrue(robin_item1_count_after == robin_item1_count - 5)
        # check amount of the products
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(0).get_quantity() == 25)
        self.assertTrue(
            self.service.store_facade.getStores()["Robin&Daughters"].getProducts().get(0).get_quantity() == 25)

    def test_guest_purchaseCart_withAddedDiscount_success(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 5,
                                 5)  # "Tomato_K", "30", "8", "vegetables" simple discount 25
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9,
                                 5)  # "Mango_K", "30", "20", "fruits" all fruits 25 simple discount
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"].__len__() == 1)
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 * 0.75 + 5 * 20 * 0.75)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        with self.assertRaises(Exception):
            self.service.store_facade.getCart(guest0_entrance_id).get_Basket("Feliks&Sons")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(4).get_quantity() == 25)

    def test_guest_purchaseCart_CardDateFail_fail(self):
        self.setUp()
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        with self.assertRaises(Exception):
            self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/20", "Amiel Saad", "555", "123456789",
                                      "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(0).get_quantity() == 30)

    # Use Case 2.2.5.b,c (guests cant participate in bids)
    def test_member_BidPurchaseRegular_success(self):
        self.service.logIn("Amiel", "password111")
        feliks_notifications_count = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "vegetables"  , 4K = 32 ins
        # ////////////
        feliks_notifications_count_afterplace = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getNotifications("Amiel").getReturnValue().__len__()
        basket = self.service.getBasket("Amiel", "Feliks&Sons")
        feliks_store = self.service.store_facade.getStores().get("Feliks&Sons")
        bid1: Bid = basket.get_bids().get(0)
        bid2: Bid = basket.get_bids().get(1)
        self.assertTrue(len(list(basket.get_bids().values())) == 2)
        self.assertTrue(len(list(feliks_store.get_bids().values())) == 2)
        self.assertTrue(bid1.get_product_id() == 0)
        self.assertTrue(bid2.get_product_id() == 1)
        self.assertTrue(bid1.get_quantity() == 4)
        self.assertTrue(bid2.get_quantity() == 4)
        self.assertTrue(bid1.get_storename() == "Feliks&Sons")
        self.assertTrue(bid2.get_storename() == "Feliks&Sons")
        self.assertTrue(bid1.get_offer() == 25)
        self.assertTrue(bid2.get_offer() == 25)
        self.assertTrue(feliks_notifications_count_afterplace == feliks_notifications_count + 2)
        self.assertTrue(sona_notifications_count_afterplace == sona_notifications_count + 2)
        self.assertTrue(sonb_notifications_count_afterplace == sonb_notifications_count + 2)
        self.assertTrue(sonc_notifications_count_afterplace == sonc_notifications_count + 2)
        self.assertTrue(sond_notifications_count_afterplace == sond_notifications_count + 2)
        self.assertTrue(amiel_notifications_count_afterplace == amiel_notifications_count + 2)
        # ========= approve all =========
        self.service.approveBid("Feliks", "Feliks&Sons", 3)
        self.service.approveBid("SonA", "Feliks&Sons", 3)
        self.service.approveBid("SonB", "Feliks&Sons", 3)
        self.service.approveBid("SonC", "Feliks&Sons", 3)
        self.service.approveBid("SonD", "Feliks&Sons", 3)
        self.service.approveBid("Feliks", "Feliks&Sons", 4)
        self.service.approveBid("SonA", "Feliks&Sons", 4)
        feliks_notifications_count_afterapprove = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterapprove = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterapprove = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterapprove = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterapprove = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterapprove = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(feliks_notifications_count_afterapprove == feliks_notifications_count_afterplace + 1)
        self.assertTrue(sona_notifications_count_afterapprove == sona_notifications_count_afterplace + 1)
        self.assertTrue(sonb_notifications_count_afterapprove == sonb_notifications_count_afterplace + 1)
        self.assertTrue(sonc_notifications_count_afterapprove == sonc_notifications_count_afterplace + 1)
        self.assertTrue(sond_notifications_count_afterapprove == sond_notifications_count_afterplace + 1)
        self.assertTrue(amiel_notifications_count_afterapprove == amiel_notifications_count_afterplace + 1)
        self.assertTrue(bid1.get_status() == 1)
        self.assertTrue(bid2.get_status() == 0)
        self.service.purchaseConfirmedBid(0, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad", "555",
                                          "123456789",
                                          "be'er sheva", "beer sheva", "israel", "1234152")
        feliks_notifications_count_afterpurchase = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterpurchase = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterpurchase = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterpurchase = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterpurchase = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterpurchase = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(feliks_notifications_count_afterpurchase == feliks_notifications_count_afterapprove + 1)
        self.assertTrue(sona_notifications_count_afterpurchase == sona_notifications_count_afterapprove + 1)
        self.assertTrue(sonb_notifications_count_afterpurchase == sonb_notifications_count_afterapprove + 1)
        self.assertTrue(sonc_notifications_count_afterpurchase == sonc_notifications_count_afterapprove + 1)
        self.assertTrue(sond_notifications_count_afterpurchase == sond_notifications_count_afterapprove + 1)
        self.assertTrue(amiel_notifications_count_afterpurchase == amiel_notifications_count_afterapprove + 1)
        self.assertTrue(self.service.getAllBidsFromStore("Feliks&Sons").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.getAllBidsFromUser("Amiel").getReturnValue().__len__() == 1)
        with self.assertRaises(Exception):  # bid id 1 wasn't confirmed
            self.service.purchaseConfirmedBid(1, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad",
                                              "555", "123456789",
                                              "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(2).get_quantity() == 26)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(3).get_quantity() == 30)

    def test_member_BidPurchaseRejected_success(self):
        self.service.logIn("Amiel", "password111")
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "vegetables"  , 4K = 32 ins
        # ////////////
        basket = self.service.getBasket("Amiel", "Feliks&Sons")
        bid1: Bid = basket.get_bids().get(0)
        bid2: Bid = basket.get_bids().get(1)
        # ========= one rejects all =========
        feliks_notifications_count_afterplace = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.service.approveBid("Feliks", "Feliks&Sons", 3)
        self.service.approveBid("SonA", "Feliks&Sons", 3)
        self.service.approveBid("SonB", "Feliks&Sons", 3)
        self.service.approveBid("SonC", "Feliks&Sons", 3)
        self.service.rejectBid("SonD", "Feliks&Sons", 3)
        self.service.approveBid("Feliks", "Feliks&Sons", 4)
        self.service.approveBid("SonA", "Feliks&Sons", 4)
        feliks_notifications_count_afterreject = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterreject = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterreject = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterreject = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterreject = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterreject = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(feliks_notifications_count_afterreject == feliks_notifications_count_afterplace + 1)
        self.assertTrue(sona_notifications_count_afterreject == sona_notifications_count_afterplace + 1)
        self.assertTrue(sonb_notifications_count_afterreject == sonb_notifications_count_afterplace + 1)
        self.assertTrue(sonc_notifications_count_afterreject == sonc_notifications_count_afterplace + 1)
        self.assertTrue(sond_notifications_count_afterreject == sond_notifications_count_afterplace + 1)
        self.assertTrue(amiel_notifications_count_afterreject == amiel_notifications_count_afterplace + 1)
        self.assertTrue(bid1.get_status() == 2)
        self.assertTrue(bid2.get_status() == 0)
        with self.assertRaises(Exception):  # bid id 0 was rejected
            self.service.purchaseConfirmedBid(0, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad",
                                              "555", "123456789",
                                              "be'er sheva", "beer sheva", "israel", "1234152")
        with self.assertRaises(Exception):  # bid id 1 wasn't confirmed
            self.service.purchaseConfirmedBid(1, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad",
                                              "555", "123456789",
                                              "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.getAllBidsFromStore("Feliks&Sons").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.getAllBidsFromUser("Amiel").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(2).get_quantity() == 30)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(3).get_quantity() == 30)

    def test_member_BidPurchaseAlternate_success(self):
        self.service.logIn("Amiel", "password111")
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "vegetables"  , 4K = 32 ins
        # ////////////
        basket = self.service.getBasket("Amiel", "Feliks&Sons")
        bid1: Bid = basket.get_bids().get(0)
        bid2: Bid = basket.get_bids().get(1)
        # ========= one rejects all =========
        feliks_notifications_count_afterplace = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.service.approveBid("Feliks", "Feliks&Sons", 3)
        self.service.sendAlternativeOffer("SonD", "Feliks&Sons", 3, 30)
        self.service.approveBid("Feliks", "Feliks&Sons", 4)
        self.service.approveBid("SonA", "Feliks&Sons", 4)
        feliks_notifications_count_afteralternate = self.service.getNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afteralternate = self.service.getNotifications("Sona").getReturnValue().__len__()
        sonb_notifications_count_afteralternate = self.service.getNotifications("Sonb").getReturnValue().__len__()
        sonc_notifications_count_afteralternate = self.service.getNotifications("Sonc").getReturnValue().__len__()
        sond_notifications_count_afteralternate = self.service.getNotifications("Sond").getReturnValue().__len__()
        amiel_notifications_count_afteralternate = self.service.getNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(feliks_notifications_count_afteralternate == feliks_notifications_count_afterplace + 1)
        self.assertTrue(sona_notifications_count_afteralternate == sona_notifications_count_afterplace + 1)
        self.assertTrue(sonb_notifications_count_afteralternate == sonb_notifications_count_afterplace + 1)
        self.assertTrue(sonc_notifications_count_afteralternate == sonc_notifications_count_afterplace + 1)
        self.assertTrue(sond_notifications_count_afteralternate == sond_notifications_count_afterplace + 1)
        self.assertTrue(amiel_notifications_count_afteralternate == amiel_notifications_count_afterplace + 1)
        self.assertTrue(bid1.get_status() == 3)
        self.assertTrue(bid2.get_status() == 0)
        self.assertTrue(bid1.get_offer() == 30)
        self.service.purchaseConfirmedBid(0, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad",
                                          "555", "123456789",
                                          "be'er sheva", "beer sheva", "israel", "1234152")
        with self.assertRaises(Exception):  # bid id 1 wasn't confirmed
            self.service.purchaseConfirmedBid(1, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad",
                                              "555", "123456789",
                                              "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.getAllBidsFromStore("Feliks&Sons").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.getAllBidsFromUser("Amiel").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(2).get_quantity() == 26)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(3).get_quantity() == 30)


class Test_Use_Case_2_3_members(TestCase):
    default_config = "../../default_config.json"
    stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

    # Use Case 2.3.1
    def test_log_out_from_the_system_success(self):
        self.setUp()
        self.service.loginAsGuest()
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(res.getReturnValue()["entrance_id"])
        self.service.logInFromGuestToMember(1, "Amiel", "password111")
        data = self.service.logOut("Amiel")
        self.assertTrue(data.getReturnValue()["entrance_id"] == guest1_entrance_id)

    def test_member_logout_same_cart(self):
        # a meber adds stuff to his cart, the log out and log in and we need to check that the cart is the same
        self.setUp()
        self.service.logIn("Amiel", "password111")
        self.service.addToBasket("Amiel", "Feliks&Sons", 3, 5)  # 5k brocolli
        self.service.addToBasket("Amiel", "Feliks&Sons", 4, 5)  # 5k carrots
        self.service.logOut("Amiel")
        self.service.logIn("Amiel", "password111")
        basket: Basket = self.service.store_facade.getBasket("Amiel", "Feliks&Sons")
        self.assertTrue(basket.getBasketSize() == 2)
        self.assertTrue(basket.calculateBasketPrice() == 10 * 8)

    # Use Case 2.3.2
    def test_createShop_Success(self):
        # a member creates a shop and we need to check that it was created and he is its founder
        self.setUp()
        self.service.logIn("Amiel", "password111")
        self.service.createStore("Amiel", "Amiel&sons")
        amiels_store: Store = self.service.store_facade.getStores()["Amiel&sons"]
        self.assertTrue(self.service.store_facade.getStores().__len__() == 3)
        self.assertTrue(amiels_store.getFounder().get_username() == "Amiel")
        self.assertTrue(amiels_store.getAllStaffMembersNames().__len__() == 1)

    def test_createShop_exists_failure(self):
        # a member creates a shop but the name is already taken
        self.setUp()
        self.service.logIn("Amiel", "password111")
        with self.assertRaises(Exception):
            self.service.createStore("Amiel", "Feliks&Sons")

    # Use Case 2.3.7
    def test_getPurchaseHistory_forMember_success(self):
        # a member buys stuff, and we need to check that it is in his purchase history
        self.setUp()
        self.service.addToBasket("Amiel", "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket("Amiel", "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        self.assertTrue(self.service.getCart("Amiel").getReturnValue()["baskets"].__len__() == 2)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.getPurchaseHistory("Amiel").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.getPurchaseHistory("Amiel").getReturnValue()[0].get_basket().getBasketSize() == 2)


class Test_Use_Case_2_4_Management(TestCase):
    default_config = "../../default_config.json"
    stores_load = "../../load_acceptanceTests2StoresNoWorkers.json"

    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

    # Use Case 4.1.a
    def test_addProductToStore_Success(self):
        pass

    # Use Case 4.1.b
    def test_deleteProductFromStore_Success(self):
        pass

    # Use Case 4.1.c
    def test_changeProductInStore_Success(self):
        pass

    # Use Case 4.2.a
    def test_newDiscountToStore_StoreLevel_Success(self):
        # res = self.service.logIn("Feliks", "password456")
        # self.assertTrue(res.getStatus())
        # res_new_discount = self.service.addDiscount("AriExpress", "Feliks", "Simple", percent=10, level="Store",
        #                                             level_name=1)
        # self.assertTrue(res_new_discount.getStatus())
        pass

    # Use Case 4.2.b

    def test_newDiscountToStore_ProductLevel_Success(self):
        pass

    # Use Case 4.2.c
    def test_newDiscountToStore_Category_Success(self):
        pass

    # Use Case 4.2.d
    def test_newDiscountToStore_Conditional_Success(self):
        pass

    # Use Case 4.2.e
    def test_newDiscountToStore_Max_Success(self):
        pass

    # Use Case 4.2.f
    def test_newDiscountToStore_Add_Success(self):
        pass

    # Use Case 4.2.g
    def test_newPolicyToStore_StoreLevel_Success(self):
        pass

    # Use Case 4.2.h
    def test_newPolicyToStore_ProductLevel_Success(self):
        pass

    # Use Case 4.2.i
    def test_newPolicyToStore_Category_Success(self):
        pass

    # Use Case 4.4.a
    def test_nominateShopOwnerByOwner_Success(self):
        pass

    # Use Case 4.4.b
    def test_nominateShopOwnerByFounder_Success(self):
        pass

    # Use Case 4.5.a
    def test_removeShopOwnerByHisNomineeOwner_Success(self):
        pass

    # Use Case 4.5.b
    def test_removeShopOwnerByFounder_Success(self):
        pass

    # Use Case 4.6.a
    def test_nominateShopManagerByOwner_Success(self):
        pass

    # Use Case 4.6.b
    def test_nominateShopManagerByFounder_Success(self):
        pass

    # Use Case 4.7.a
    def test_addPermissionToShopManager_Success(self):
        pass

    # Use Case 4.7.b
    def test_removePermissionToShopManager_success(self):
        pass

    # Use Case 4.8.a
    def test_removeShopManagerByHisNomineeOwner_Success(self):
        pass

    # Use Case 4.8.b
    def test_removeShopManagerByFounder_Success(self):
        pass

    # Use Case 4.9
    def test_closeStore_success(self):
        # also to check users can't see items from there after close
        # and that notifications were sent to all staff
        pass

    # Use Case 4.10
    def test_reopenStore_success(self):
        pass

    # Use Case 4.11
    def test_requestStoreStaffInfo_success(self):
        pass

    # Use Case 4.13
    def test_requestStorePurchaseHistory_success(self):
        pass


class Test_Use_Case_2_5_nominations(TestCase):
    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

    # Use Case 5
    def test_nominatedPreformingGivenAction_Success(self):
        pass

    # Use Case 5.1
    def test_nominatedPreformingUnGivenAction_Fail(self):
        pass


class Test_Use_Case_2_6_transactions(TestCase):
    def setUp(self):
        self.service = Service(self.default_config, true_lambda)

    # Use Case 2.6.2
    def test_AdminBanMember_success(self):
        pass

    # Use Case 2.6.4
    def test_StorePurchaseHistoryAdmin_success(self):
        pass

    def test_UserPurchaseHistoryAdmin_success(self):
        pass

    # Use Case 2.6.6
    def test_AdminGetInfoMembersOnOff_success(self):
        pass

    def test_AdminGetInfoMember_success(self):
        pass


if __name__ == '__main__':
    unittest.main()
