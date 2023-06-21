import ast
import json
import unittest
from unittest import TestCase

from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects import Discount
from ProjectCode.Domain.MarketObjects.StoreObjects.PurchasePolicy import PurchasePolicy
from ProjectCode.Service.Service import Service

default_config = "../../../default_config.json"
stores_load = "../../../load_acceptanceTests2StoresSonsWorkers.json"
empty_load = "../../../empty_load.json"
true_lambda = lambda self, receiver_id, notification_id, type, subject: True

""" ---------------------- (1) System Functionality tests ---------------------- """
class Test_Use_Cases_1(TestCase):

    #  Use Case 1.1
    def test_starting_the_market_system_success(self):
        service = Service(config_file=default_config, load_file=empty_load, send_notification_call=true_lambda)
        self.assertTrue(service.store_facade.getAdmin("admin"))

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

    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    def test_request_to_payment_supply_success(self):
        res = self.service.loginAsGuest()
        guest_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(res.getStatus())
        res_added_product = self.service.addToBasket(guest_id, "Feliks&Sons", 1, 5)
        self.assertTrue(res_added_product.getStatus())
        res_purchase = self.service.purchaseCart(guest_id, "4580020345672134", "12/26", "Amiel Saad", "555",
                                                 "123456789",
                                                 "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(res_purchase.getStatus())

    # Use case 1.5 & 1.6

    def test_notification_to_store_founder_and_user(self):
        self.service.logIn("Amiel", "password111")
        self.service.logIn("Feliks", "password333")
        notification_amount_amiel = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        notification_amount_feliks = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.logOut("Feliks")
        self.assertTrue(notification_amount_amiel == 0)
        self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789", "be'er sheva",
                                  "beer sheva", "israel", "1234152")
        notification_amount_amiel = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(notification_amount_amiel == 1)
        self.service.logIn("Feliks", "password333")
        notification_amount_founder = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertTrue(notification_amount_founder == notification_amount_feliks + 1)
        self.assertTrue(self.service.getAllNotifications("Feliks").getReturnValue()[-1]["status"] == "pending")

    # Use case 1.7

    def test_notify_user_at_success_and_error(self):
        self.service.logIn("Amiel", "password111")
        self.service.logIn("Feliks", "password333")
        self.service.addToBasket('Amiel', "Feliks&Sons", 1, 5)
        res = self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "986", "123456789",
                                        "be'er sheva",
                                        "beer sheva", "israel", "1234152")
        self.assertFalse(res.getStatus())
        res = self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                        "be'er sheva",
                                        "beer sheva", "israel", "1234152")
        self.assertTrue(res.getStatus())


""" ---------------------- (2.1) User system Functionality tests ---------------------- """
class Test_Use_Cases_2_1(TestCase):

    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    # Use Case 2.1.1
    def test_guest_visit_success(self):  # TODO fix
        # a guest can (1) visit the system (2) have a cart
        # (3) add products to it (4) and purchase it.
        # =============================================
        # (1)
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(guest0_entrance_id == 2)
        self.assertTrue(guest1_entrance_id == 3)
        # (2)
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["username"] == "2")
        self.assertTrue(self.service.getCart(guest1_entrance_id).getReturnValue()["username"] == "3")
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest1_cart = ast.literal_eval(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart == {})
        self.assertTrue(guest1_cart == {})
        # (3)
        feliks_product_1_quantity = self.service.getProduct("Feliks&Sons", 1, "Feliks").getReturnValue()["quantity"]
        print(self.service.getProduct("Robin&Daughters", 1, "Robin").getReturnValue()["name"])
        robin_product_1_quantity = self.service.getProduct("Robin&Daughters", 1, "Robin").getReturnValue()["quantity"]
        robin_product_2_quantity = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 2, 5)
        self.service.editBasketQuantity(guest0_entrance_id, "Feliks&Sons", 1, 8)
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Robin&Daughters", 2, 5)
        basket = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        basket1 = ast.literal_eval(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"])
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest0_products_Robin = ast.literal_eval(guest0_cart["Robin&Daughters"]["products"])
        guest0_products_Feliks = ast.literal_eval(guest0_cart["Feliks&Sons"]["products"])
        guest1_cart = ast.literal_eval(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"])
        guest1_products_Robin = ast.literal_eval(guest1_cart["Robin&Daughters"]["products"])
        self.assertTrue(ast.literal_eval(
            ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])["Feliks&Sons"][
                "products"])["1"]["quantity"] == 8)
        self.assertTrue(
            ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"]).keys().__contains__(
                "Robin&Daughters"))
        self.assertTrue(ast.literal_eval(
            ast.literal_eval(self.service.getCart(guest1_entrance_id).getReturnValue()["baskets"])["Robin&Daughters"][
                "products"])["2"]["quantity"] == 5)
        # (4)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        self.assertTrue(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"] == [])
        feliks_product_1_quantity_after = self.service.getProduct("Feliks&Sons", 1, "Feliks").getReturnValue()[
            "quantity"]
        robin_product_1_quantity_after = self.service.getProduct("Robin&Daughters", 1, "Robin").getReturnValue()[
            "quantity"]
        robin_product_2_quantity_after = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()[
            "quantity"]
        self.assertTrue(feliks_product_1_quantity_after == feliks_product_1_quantity - 8)
        self.assertTrue(robin_product_1_quantity_after == robin_product_1_quantity - 5)
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    # Use Case 2.1.2
    def test_guest_exit_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        robin_product_2_quantity = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 2, 5)
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest0_products_Robin = ast.literal_eval(guest0_cart["Robin&Daughters"]["products"])
        self.assertTrue(guest0_products_Robin["2"]["product"]['name'] == "Ketchup")
        self.assertTrue(guest0_products_Robin["2"]["quantity"] == 5)
        self.assertTrue(guest0_products_Robin["2"]["price"] == 15)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertFalse(self.service.getCart(guest0_entrance_id).getStatus())
        robin_product_2_quantity_after = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()["quantity"]
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    # Use Case 2.1.3
    def test_registration_to_the_system_success(self):
        self.assertFalse(self.service.logIn("username22", "password1").getStatus())
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        member_info = ast.literal_eval(ast.literal_eval(self.service.getMemberInfo("admin", "username22").getReturnValue())["member"])
        self.assertTrue(member_info["username"] == "username22")
        self.assertTrue(member_info["email"] == "email")
        self.assertTrue(member_info["cart"]["baskets"] == '{}')
        res = self.service.logIn("username22", "password1")
        self.assertTrue(res.getStatus())

    def test_registration_to_the_system_failure(self):
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        self.assertFalse(self.service.register("username22", "password1", "email").getStatus())

    # Use Case 2.1.4

    def test_login_to_the_system_success(self):
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        member_res = self.service.logIn("username22", "password1").getReturnValue()
        self.assertTrue(member_res['username'] == 'username22')
        self.assertTrue(member_res['email'] == 'email')

    def test_logging_in_the_system_failure(self):
        res = self.service.register("username22", "password1", "email")
        self.assertTrue(res.getStatus())
        self.assertFalse(self.service.logIn("username22", "password2").getStatus())


""" ---------------------- (2.2) User Purchase tests ---------------------- """
class Test_Use_Case_2_2(TestCase):
    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    # Use Case 2.2.1
    def test_guest_information_fetching_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        stores_info = ast.literal_eval(self.service.getStoresBasicInfo().getReturnValue())
        store_count = stores_info.__len__()
        self.assertTrue(store_count == 2)
        feliks_products = ast.literal_eval(self.service.getStoreProductsInfo("Feliks&Sons").getReturnValue()["products"])
        self.assertTrue(feliks_products.__len__() == 12)
        product1 = self.service.getProduct("Feliks&Sons", 1, guest0_entrance_id).getReturnValue()
        self.assertTrue(product1["name"] == "Cauliflower_K")
        self.assertTrue(product1["quantity"] == 30)
        self.assertTrue(product1["price"] == 8)
        self.assertTrue(product1["categories"] == "Vegetables")
        product9 = self.service.getProduct("Feliks&Sons", 9, guest0_entrance_id).getReturnValue()
        self.assertTrue(product9["name"] == "Mango_K")
        self.assertTrue(product9["quantity"] == 30)
        self.assertTrue(product9["price"] == 20)
        self.assertTrue(product9["categories"] == "Fruits")

    def test_guest_information_fetching_noSuchStore_failure(self):
        stores_info = ast.literal_eval(self.service.getStoresBasicInfo().getReturnValue())
        store_count = stores_info.__len__()
        self.assertTrue(store_count == 2)
        self.assertFalse(self.service.getStoreProductsInfo("Ari&Bears").getStatus())

    def test_guest_information_fetching_noSuchProduct_failure(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        stores_info = ast.literal_eval(self.service.getStoresBasicInfo().getReturnValue())
        store_count = stores_info.__len__()
        self.assertTrue(store_count == 2)
        feliks_products = ast.literal_eval(self.service.getStoreProductsInfo("Feliks&Sons").getReturnValue()["products"])
        self.assertTrue(feliks_products.__len__() == 12)
        self.assertFalse(self.service.getProduct("Feliks&Sons", 15, guest0_entrance_id).getStatus())

    # Use Case 2.2.2.a

    def test_guest_product_search_by_name_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        products_res = self.service.productSearchByName("Ca", guest0_entrance_id).getReturnValue()
        self.assertTrue(products_res["Feliks&Sons"].__len__() == 3)  # Cabbage, Cauliflower, Carrot
        with self.assertRaises(Exception):
            var = products_res["Robin&Daughters"]  # None in Ca
        products_res = self.service.productSearchByName("Ch", guest0_entrance_id).getReturnValue()
        self.assertTrue(products_res["Feliks&Sons"].__len__() == 1)  # Cherry
        self.assertTrue(products_res["Robin&Daughters"].__len__() == 1)  # Chilli

    # Use Case 2.2.2.b
    def test_guest_product_search_by_category_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res_product = self.service.productSearchByCategory("Sauces", guest0_entrance_id).getReturnValue()
        self.assertTrue(res_product.__len__() == 5)  # 5 Sauces

    # Use Case 2.2.2.c
    def test_guest_product_search_by_features_price_success(self):
        # TODO
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res_products_below10 = ast.literal_eval(self.service.productFilterByFeatures({"min_price": 0, "max_price": 10},guest0_entrance_id).getReturnValue())
        res_products_below5 = ast.literal_eval(self.service.productFilterByFeatures({"min_price": 0, "max_price": 5}, guest0_entrance_id).getReturnValue())
        self.assertTrue(res_products_below10["Feliks&Sons"].__len__() == 10)  # All products except cherry and mango
        self.assertTrue(res_products_below10["Robin&Daughters"].__len__() == 3)  # just seasoning
        self.assertTrue(res_products_below5["Robin&Daughters"].__len__() == 3)  # just seasoning
        with self.assertRaises(Exception):
            x = res_products_below5.getReturnValue()["Feliks&Sons"]  # None in Feliks's
        self.assertFalse(self.service.productFilterByFeatures({"Size": 0}, guest0_entrance_id).getStatus())

    # Use Case 2.2.3

    def test_guest_add_product_to_cart_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        prod = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()
        robin_product_2_quantity = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()["quantity"]
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 2, 5)
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest0_products_Robin = ast.literal_eval(guest0_cart["Robin&Daughters"]["products"])
        self.assertTrue(guest0_products_Robin["2"]["quantity"] == 5)
        self.assertTrue(guest0_products_Robin["2"]["product"]["product_id"] == 2)
        self.service.leaveAsGuest(guest0_entrance_id)
        self.assertFalse(self.service.getCart(guest0_entrance_id).getStatus())
        robin_product_2_quantity_after = self.service.getProduct("Robin&Daughters", 2, "Robin").getReturnValue()["quantity"]
        self.assertTrue(robin_product_2_quantity_after == robin_product_2_quantity)

    def test_guest_add_product_to_cart_productDoesntExists_failure(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertFalse(self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 80, 5).getStatus())
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart == {})
    def test_guest_add_product_to_cart_StoreDoesntExists_failure(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertFalse(self.service.addToBasket(guest0_entrance_id, "Robin&Sons", 1, 5).getStatus())
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart == {})

    # Use Case 2.2.4.a

    def test_guest_getBasket_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest0_products_Robin = ast.literal_eval(guest0_cart["Robin&Daughters"]["products"])
        guest0_products_Feliks = ast.literal_eval(guest0_cart["Feliks&Sons"]["products"])
        self.assertTrue(guest0_products_Feliks["1"]["quantity"] == 5)
        self.assertTrue(guest0_products_Feliks["1"]["product"]["product_id"] == 1)
        self.assertTrue(guest0_cart.keys().__contains__("Feliks&Sons"))
        self.assertTrue(guest0_products_Robin["1"]["quantity"] == 5)
        self.assertTrue(guest0_products_Robin["1"]["product"]["product_id"] == 1)
        self.assertTrue(guest0_cart.keys().__contains__("Robin&Daughters"))

    # Use Case 2.2.4.b
    def test_guest_editBasket_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "Sauces"
        self.service.editBasketQuantity(guest0_entrance_id, "Feliks&Sons", 1, 7)
        self.service.editBasketQuantity(guest0_entrance_id, "Robin&Daughters", 1, 8)
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        guest0_products_Robin = ast.literal_eval(guest0_cart["Robin&Daughters"]["products"])
        guest0_products_Feliks = ast.literal_eval(guest0_cart["Feliks&Sons"]["products"])
        self.assertTrue(guest0_products_Feliks["1"]["quantity"] == 7)
        self.assertTrue(guest0_products_Feliks["1"]["product"]["product_id"] == 1)
        self.assertTrue(guest0_cart.keys().__contains__("Feliks&Sons"))
        self.assertTrue(guest0_products_Robin["1"]["quantity"] == 8)
        self.assertTrue(guest0_products_Robin["1"]["product"]["product_id"] == 1)
        self.assertTrue(guest0_cart.keys().__contains__("Robin&Daughters"))

    def test_guest_editBasket_itemDoesntExists_fail(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "Sauces"
        self.assertFalse(self.service.editBasketQuantity(guest0_entrance_id, "Feliks&Sons", 2, 7).getStatus())

    def test_guest_editBasket_BasketDoesntExists_fail(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.assertFalse(self.service.editBasketQuantity(guest0_entrance_id, "Robin&Daughters", 1, 7).getStatus())

    # Use Case 2.2.5.a

    def test_guest_purchaseCart_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 2, 5)  # "Cabbage_K", "30", "8", "Vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "Sauces"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 2, 5)  # "Ketchup", "30", "15", "Sauces"
        guest0_cart_baskets = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart_baskets.__len__() == 2)
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        robin_notification_count = self.service.getAllNotifications("Robin").getReturnValue().__len__()
        feliks_inventory = ast.literal_eval(self.service.getProductsByStore("Feliks&Sons", "Feliks").getReturnValue())
        feliks_item1_count = feliks_inventory["1"]["quantity"]
        feliks_item2_count = feliks_inventory["2"]["quantity"]
        robin_inventory = ast.literal_eval(self.service.getProductsByStore("Robin&Daughters", "Robin").getReturnValue())
        robin_item1_count = robin_inventory["1"]["quantity"]
        robin_item2_count = robin_inventory["2"]["quantity"]
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        robin_notification_count_after = self.service.getAllNotifications("Robin").getReturnValue().__len__()
        feliks_inventory = ast.literal_eval(self.service.getProductsByStore("Feliks&Sons", "Feliks").getReturnValue())
        feliks_item1_count_after = feliks_inventory["1"]["quantity"]
        feliks_item2_count_after = feliks_inventory["2"]["quantity"]
        robin_inventory = ast.literal_eval(self.service.getProductsByStore("Robin&Daughters", "Robin").getReturnValue())
        robin_item1_count_after = robin_inventory["1"]["quantity"]
        robin_item2_count_after = robin_inventory["2"]["quantity"]
        self.assertTrue(feliks_notification_count_after == feliks_notification_count + 1)
        self.assertTrue(robin_notification_count_after == robin_notification_count + 1)
        #   check that the items were removed from the inventory
        self.assertTrue(feliks_item1_count_after == feliks_item1_count - 5)
        self.assertTrue(feliks_item2_count_after == feliks_item2_count - 5)
        self.assertTrue(robin_item1_count_after == robin_item1_count - 5)
        self.assertTrue(robin_item2_count_after == robin_item2_count - 5)
        #  check that the cart is empty
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart == {})


    def test_guest_purchaseCart_withAddedDiscount_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.logIn("Feliks", "password333")
        self.service.addDiscount("Feliks&Sons", "Feliks", "Simple", percent=25, level="Product", level_name=5)
        self.service.addDiscount("Feliks&Sons", "Feliks", "Simple", percent=25, level="Category", level_name="Fruits")
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 5, 5)  # "Tomato_K", "30", "8", "Vegetables" simple discount 25
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 5)  # "Mango_K", "30", "20", "Fruits" all Fruits 25 simple discount
        guest0_cart = ast.literal_eval(self.service.getCart(guest0_entrance_id).getReturnValue()["baskets"])
        self.assertTrue(guest0_cart.__len__() == 1)
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket("Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 * 0.75 + 5 * 20 * 0.75)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        with self.assertRaises(Exception):
            self.service.store_facade.getCart(guest0_entrance_id).get_Basket("Feliks&Sons")
        feliks_inventory = ast.literal_eval(self.service.getProductsByStore("Feliks&Sons", "Feliks").getReturnValue())
        feliks_item5_count_after = feliks_inventory["5"]["quantity"]
        feliks_item9_count_after = feliks_inventory["9"]["quantity"]
        self.assertTrue(feliks_item5_count_after == 25)
        self.assertTrue(feliks_item9_count_after == 25)

    def test_guest_purchaseCart_CardDateFail_fail(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "Sauces"
        self.assertFalse(self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/20", "Amiel Saad", "986", "123456789",
                                      "be'er sheva", "beer sheva", "israel", "1234152").getStatus())
        feliks_inventory = ast.literal_eval(self.service.getProductsByStore("Feliks&Sons", "Feliks").getReturnValue())
        feliks_item1_count_after = feliks_inventory["1"]["quantity"]
        robin_inventory = ast.literal_eval(self.service.getProductsByStore("Robin&Daughters", "Robin").getReturnValue())
        robin_item1_count_after = robin_inventory["1"]["quantity"]
        self.assertTrue(feliks_item1_count_after == 30)
        self.assertTrue(robin_item1_count_after == 30)

    # Use Case 2.2.5.b,c (guests cant participate in bids)
    def test_member_BidPurchaseRegular_success(self):
        self.service.logIn("Amiel", "password111")
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        feliks_notifications_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "Vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "Vegetables"  , 4K = 32 ins
        # ////////////
        feliks_notifications_count_afterplace = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        feliks_store_bids = self.service.store_facade.getAllBidsFromStore("Feliks&Sons")
        amiel_store_bids = self.service.store_facade.getAllBidsFromUser("Amiel")
        bid1: Bid = feliks_store_bids.get(0)
        bid2: Bid = feliks_store_bids.get(1)
        Amiel_cart = ast.literal_eval(self.service.getCart("Amiel").getReturnValue()["baskets"])
        self.assertTrue(len(feliks_store_bids.get()) == 2)
        self.assertTrue(len(amiel_store_bids) == 2)
        self.assertTrue(bid1.get_product_id() == 3)
        self.assertTrue(bid2.get_product_id() == 4)
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
        self.service.approveBid("Feliks", "Feliks&Sons", 0)
        self.service.approveBid("Son_A", "Feliks&Sons", 0)
        self.service.approveBid("Son_B", "Feliks&Sons", 0)
        self.service.approveBid("Son_C", "Feliks&Sons", 0)
        self.service.approveBid("Son_D", "Feliks&Sons", 0)
        self.service.approveBid("Feliks", "Feliks&Sons", 1)
        self.service.approveBid("Son_A", "Feliks&Sons", 1)
        feliks_notifications_count_afterapprove = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterapprove = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterapprove = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterapprove = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterapprove = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterapprove = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        self.assertTrue(feliks_notifications_count_afterapprove == feliks_notifications_count_afterplace + 1)
        self.assertTrue(sona_notifications_count_afterapprove == sona_notifications_count_afterplace + 1)
        self.assertTrue(sonb_notifications_count_afterapprove == sonb_notifications_count_afterplace + 1)
        self.assertTrue(sonc_notifications_count_afterapprove == sonc_notifications_count_afterplace + 1)
        self.assertTrue(sond_notifications_count_afterapprove == sond_notifications_count_afterplace + 1)
        self.assertTrue(amiel_notifications_count_afterapprove == amiel_notifications_count_afterplace + 1)
        feliks_store_bids = self.service.store_facade.getAllBidsFromStore("Feliks&Sons")
        bid1: Bid = feliks_store_bids.get(0)
        bid2: Bid = feliks_store_bids.get(1)
        self.assertTrue(bid1.get_status() == 1)
        self.assertTrue(bid2.get_status() == 0)
        self.service.purchaseConfirmedBid(0, "Feliks&Sons", "Amiel", "4580020345672134", "12/26", "Amiel Saad", "555",
                                          "123456789",
                                          "be'er sheva", "beer sheva", "israel", "1234152")
        feliks_notifications_count_afterpurchase = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterpurchase = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterpurchase = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterpurchase = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterpurchase = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterpurchase = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
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
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "Vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "Vegetables"  , 4K = 32 ins
        # ////////////
        basket = self.service.getBasket("Amiel", "Feliks&Sons")
        bid1: Bid = basket.get_bids().get(0)
        bid2: Bid = basket.get_bids().get(1)
        # ========= one rejects all =========
        feliks_notifications_count_afterplace = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        self.service.approveBid("Feliks", "Feliks&Sons", 3)
        self.service.approveBid("Son_A", "Feliks&Sons", 3)
        self.service.approveBid("Son_B", "Feliks&Sons", 3)
        self.service.approveBid("Son_C", "Feliks&Sons", 3)
        self.service.rejectBid("Son_D", "Feliks&Sons", 3)
        self.service.approveBid("Feliks", "Feliks&Sons", 4)
        self.service.approveBid("SonA", "Feliks&Sons", 4)
        feliks_notifications_count_afterreject = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterreject = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterreject = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterreject = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterreject = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterreject = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
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
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 3, 4)  # "Broccoli_K", "30", "8", "Vegetables", 4K = 32 ins
        self.service.placeBid("Amiel", "Feliks&Sons", 25, 4, 4)  # "Carrot_K", "30", "8", "Vegetables"  , 4K = 32 ins
        # ////////////
        basket = self.service.getBasket("Amiel", "Feliks&Sons")
        bid1: Bid = basket.get_bids().get(0)
        bid2: Bid = basket.get_bids().get(1)
        # ========= one rejects all =========
        feliks_notifications_count_afterplace = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afterplace = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afterplace = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afterplace = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afterplace = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afterplace = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
        self.service.approveBid("Feliks", "Feliks&Sons", 3)
        self.service.sendAlternativeOffer("Son_D", "Feliks&Sons", 3, 30)
        self.service.approveBid("Feliks", "Feliks&Sons", 4)
        self.service.approveBid("Son_A", "Feliks&Sons", 4)
        feliks_notifications_count_afteralternate = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        sona_notifications_count_afteralternate = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notifications_count_afteralternate = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notifications_count_afteralternate = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notifications_count_afteralternate = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        amiel_notifications_count_afteralternate = self.service.getAllNotifications("Amiel").getReturnValue().__len__()
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


""" ---------------------- (2.3) Member Functionality tests ---------------------- """
class Test_Use_Case_2_3_members(TestCase):

    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    # Use Case 2.3.1
    def test_log_out_from_the_system_success(self):
        self.service.loginAsGuest()
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.logInFromGuestToMember(1, "Amiel", "password111")
        data = self.service.logOut("Amiel")
        self.assertTrue(data.getReturnValue()["entrance_id"] == guest1_entrance_id)

    def test_member_logout_same_cart(self):
        # a meber adds stuff to his cart, the log out and log in and we need to check that the cart is the same
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
        self.service.logIn("Amiel", "password111")
        self.service.createStore("Amiel", "Amiel&sons")
        amiels_store: Store = self.service.store_facade.getStores()["Amiel&sons"]
        self.assertTrue(self.service.store_facade.getStores().__len__() == 3)
        self.assertTrue(amiels_store.getFounder().get_username() == "Amiel")
        self.assertTrue(amiels_store.getAllStaffMembers("Amiel&Sons", "Amiel").__len__() == 1)

    def test_createShop_exists_failure(self):
        # a member creates a shop but the name is already taken
        self.service.logIn("Amiel", "password111")
        with self.assertRaises(Exception):
            self.service.createStore("Amiel", "Feliks&Sons")

    # Use Case 2.3.7
    def test_getPurchaseHistory_forMember_success(self):
        # a member buys stuff, and we need to check that it is in his purchase history
        self.service.addToBasket("Amiel", "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "Vegetables"
        self.service.addToBasket("Amiel", "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "Sauces"
        self.assertTrue(self.service.getCart("Amiel").getReturnValue()["baskets"].__len__() == 2)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel Saad", "555", "123456789",
                                  "be'er sheva", "beer sheva", "israel", "1234152")
        self.assertTrue(self.service.getPurchaseHistory("Amiel").getReturnValue().__len__() == 1)
        self.assertTrue(self.service.getPurchaseHistory("Amiel").getReturnValue()[0].get_basket().getBasketSize() == 2)


""" ---------------------- (2.4 & 2.5) Owner & Manager Functionality tests ---------------------- """
class Test_Use_Case_2_4_Management(TestCase):

    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    # =================================================================================================================
    # Use Case 4.1.a
    def test_addProductToStore_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.addNewProductToStore("Son_A", "Feliks&Sons", "Cucumber_K", "30", "8", "Vegetables")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().__len__() == 13)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(12).get_quantity() == 30)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(12).get_price() == 8)
        self.assertTrue(
            self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(12).get_category() == "Vegetables")
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 13, 5)

    # Use Case 4.1.b
    def test_deleteProductFromStore_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.addNewProductToStore("Son_A", "Feliks&Sons", "Cucumber_K", "30", "8", "Vegetables")
        self.service.removeProductFromStore("Son_A", "Feliks&Sons", 12)
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        with self.assertRaises(Exception):
            self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 12, 5)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().__len__() == 12)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 13, 5)

    # Use Case 4.1.c
    def test_changeProductInStore_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_quantity() == 30)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_price() == 8)
        self.assertTrue(
            self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_category() == "Vegetables")
        self.service.editProductOfStore("Son_A", "Feliks&Sons", 10, price=10, quantity=10, categories="veggies")
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_quantity() == 10)
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_price() == 10)
        self.assertTrue(
            self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(10).get_category() == "veggies")
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 5)

    # =================================================================================================================
    # Use Case 4.2.a - Simple

    def test_newDiscountToStore_Simple_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(1).get_price() == 8)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 40)
        # add 25% discount to prod id 1
        self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Product", level_name=1)
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 30)

    def test_newDiscountToStore_Simple_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(1).get_price() == 8)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 5)  # "Mango_K", "30", "20", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 5)  # "Banana_K", "30", "8", "fruits"
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8)
        # add 25% discount to all Fruits Category in Feliks&Sons
        self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Category", level_name="Fruits")
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 * 0.75 + 5 * 8 * 0.75)

    def test_newDiscountToStore_Simple_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(1).get_price() == 8)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 5)  # "Mango_K", "30", "20", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 5)  # "Banana_K", "30", "8", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8 + 5 * 15)
        # add 25% discount to all store: Feliks&Sons
        self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Store", level_name="")
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 * 0.75 + 5 * 20 * 0.75 + 5 * 8 * 0.75 + 5 * 15)

    def test_removeDiscountFromStore_Simple_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 40)
        # add 25% discount to prod id 1, then remove it
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Product", level_name=1)
        added_discount: Discount = ast.literal_eval(res.getReturnValue())
        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 40)

    def test_removeDiscountFromStore_Simple_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(1).get_price() == 8)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 5)  # "Mango_K", "30", "20", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 5)  # "Banana_K", "30", "8", "fruits"
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8)
        # add 25% discount to all Fruits Category in Feliks&Sons, then remove it
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Category",
                                       level_name="Fruits")
        added_discount: Discount = ast.literal_eval(res.getReturnValue())
        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8)

    def test_removeDiscountFromStore_Simple_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.assertTrue(self.service.store_facade.getStores()["Feliks&Sons"].getProducts().get(1).get_price() == 8)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)  # "Cauliflower_K", "30", "8", "vegetables"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 5)  # "Mango_K", "30", "20", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 5)  # "Banana_K", "30", "8", "fruits"
        self.service.addToBasket(guest0_entrance_id, "Robin&Daughters", 1, 5)  # "BBQ_Sauce", "30", "15", "sauces"
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8 + 5 * 15)
        # add 25% discount to all store: Feliks&Sons, then remove it
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Simple", percent=25, level="Store", level_name="")
        added_discount: Discount = ast.literal_eval(res.getReturnValue())
        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())
        basket_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket_price == 5 * 8 + 5 * 20 + 5 * 8 + 5 * 15)

    # =================================================================================================================
    # Use Case 4.2.b - Conditional

    def test_newDiscountToStore_Conditional_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 120 OR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off mango
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 120,
                 "child": {"logic_type": "OR", "rule": rule2}}
        self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Product", level_name=9,
                                 rule=rule1)

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 4 mango - no discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 4)
        # guest1 will have just 5 cauliflower and 1 mango - no discount
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 9, 1)
        # guest2 will have a big basket from 7 mango - discount
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 9, 7)  # 20*6 > 120
        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 4 * 20)
        self.assertTrue(basket1_price == 5 * 8 + 20 * 1)
        self.assertTrue(basket2_price == 7 * 20 * 0.5)
        self.assertTrue(basket3_price == 5 * 8 + 5 * 8 + 20 * 1 * 0.5)

    def test_newDiscountToStore_Conditional_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 200 XOR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off all fruits
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 200,
                 "child": {"logic_type": "XOR", "rule": rule2}}
        self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Category",
                                 level_name="Fruits", rule=rule1)

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 4 mango 4 bananas - no discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 4)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 4)
        # guest1 will have just 5 cauliflower and 1 mango and 1 banana - no discount
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 9, 1)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 1)
        # guest2 will have a big basket from 10 mango AND 5 cabbages and 5 cauliflower - no discount, XOR fault
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 9, 10)  # 20*10 > 120
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 2, 5)
        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango and 1 banana - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 10, 1)

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 4 * 20 + 4 * 8)
        self.assertTrue(basket1_price == 5 * 8 + 20 * 1 + 8 * 1)
        self.assertTrue(basket2_price == 10 * 20 + 5 * 8 + 5 * 8)
        self.assertTrue(basket3_price == 5 * 8 + 5 * 8 + 20 * 1 * 0.5 + 8 * 1 * 0.5)

    def test_newDiscountToStore_Conditional_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 200 XOR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off all store
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 200,
                 "child": {"logic_type": "XOR", "rule": rule2}}
        self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Category",
                                 level_name="Fruits", rule=rule1)

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 4 mango 4 bananas - no discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 4)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 4)
        # guest1 will have just 5 cauliflower and 1 mango and 1 banana - no discount
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 9, 1)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 1)
        # guest2 will have a big basket from 10 mango AND 5 cabbages and 5 cauliflower - no discount, XOR fault
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 9, 10)  # 20*10 > 120
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 2, 5)
        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango and 1 banana - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 10, 1)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 3, 5)

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 4 * 20 + 4 * 8)
        self.assertTrue(basket1_price == 5 * 8 + 20 * 1 + 8 * 1)
        self.assertTrue(basket2_price == 10 * 20 + 5 * 8 + 5 * 8)
        self.assertTrue(basket3_price == 5 * 8 * 0.5 + 5 * 8 * 0.5 + 20 * 1 * 0.5 + 8 * 1 * 0.5)

    def test_removeDiscountFromStore_Conditional_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 120 OR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off mango
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 120,
                 "child": {"logic_type": "OR", "rule": rule2}}
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Product", level_name=9,
                                       rule=rule1)
        added_discount: Discount = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest2 will have a big basket from 7 mango - discount
        self.service.addToBasket(guest2_entrance_id, "Feliks&Sons", 9, 7)  # 20*6 > 120
        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)

        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())

        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket2_price == 7 * 20)
        self.assertTrue(basket3_price == 5 * 8 + 5 * 8 + 20 * 1)

    def test_removeDiscountFromStore_Conditional_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 200 XOR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off all fruits
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 200,
                 "child": {"logic_type": "XOR", "rule": rule2}}
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Category",
                                       level_name="Fruits", rule=rule1)
        added_discount: Discount = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango and 1 banana - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)

        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())
        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket3_price == 5 * 8 + 5 * 8 + 20 * 1 + 8 * 1)

    def test_removeDiscountFromStore_Conditional_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: if all basket price is greater than 200 XOR (cabbage(2) amount >= 5 AND cauliflower(1) amount >= 5)
        #               then: 50% off all store
        rule3 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": ">=", "quantity": 5,
                 "child": {}}
        rule2 = {"rule_type": "amount_of_product", "product": 2, "category": "", "operator": ">=", "quantity": 5,
                 "child": {"logic_type": "AND", "rule": rule3}}
        rule1 = {"rule_type": "basket_total_price", "product": -1, "category": "", "operator": ">=", "quantity": 200,
                 "child": {"logic_type": "XOR", "rule": rule2}}
        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Conditioned", percent=50, level="Category",
                                       level_name="Fruits", rule=rule1)
        added_discount: Discount = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest3_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest 3 will have 5 cabbage 5 cauliflower and 1 mango and 1 banana - discount
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 9, 1)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 10, 1)
        self.service.addToBasket(guest3_entrance_id, "Feliks&Sons", 3, 5)

        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())

        basket3_price = self.service.store_facade.getCart(guest3_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        self.assertTrue(basket3_price == 5 * 8 + 5 * 8 + 20 * 1 + 8 * 1)

    # =================================================================================================================
    # Use Case 4.2.c - Max
    def test_newDiscountToStore_Max_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Max discount: 1) 50% off cauliflower 2) 25% off all vegetables 3) 20% off all store
        discount1 = {"discount_type": "Simple", "percent": 50, "level": "Product", "level_name": 1}
        discount2 = {"discount_type": "Simple", "percent": 25, "level": "Category", "level_name": "Vegetable"}
        discount3 = {"discount_type": "Simple", "percent": 20, "level": "Store", "level_name": ""}

        self.service.addDiscount("Feliks&Sons", "Son_A", "Max",
                                 discounts={"1": discount1, "2": discount2, "3": discount3})

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 5 cauliflower - 50% discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        # guest1 will have just 5 cabbage and 5 cauliflower - 50% discount cauliflower 25% discount cabbage
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        # guest2 will have just 5 cabbage and 5 cauliflower and 5 banana - 50% discount cauliflower 25% discount cabbage 20% banana
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 5)

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 5 * 8 * 0.5)
        self.assertTrue(basket1_price == 5 * 8 * 0.5 + 5 * 8 * 0.75)
        self.assertTrue(basket2_price == 5 * 8 * 0.5 + 5 * 8 * 0.75 + 5 * 8 * 0.8)

    def test_removeDiscountFromStore_Max_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Max discount: 1) 50% off cauliflower 2) 25% off all vegetables 3) 20% off all store
        discount1 = {"discount_type": "Simple", "percent": 50, "level": "Product", "level_name": 1}
        discount2 = {"discount_type": "Simple", "percent": 25, "level": "Category", "level_name": "Vegetable"}
        discount3 = {"discount_type": "Simple", "percent": 20, "level": "Store", "level_name": ""}

        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Max",
                                       discounts={"1": discount1, "2": discount2, "3": discount3})
        added_discount: Discount = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 5 cauliflower - 50% discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        # guest1 will have just 5 cabbage and 5 cauliflower - 50% discount cauliflower 25% discount cabbage
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        # guest2 will have just 5 cabbage and 5 cauliflower and 5 banana - 50% discount cauliflower 25% discount cabbage 20% banana
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 5)

        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 5 * 8)
        self.assertTrue(basket1_price == 5 * 8 + 5 * 8)
        self.assertTrue(basket2_price == 5 * 8 + 5 * 8 + 5 * 8)

    # =================================================================================================================
    # Use Case 4.2.d - Add
    def test_newDiscountToStore_Add_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: 1) 50% off cauliflower 2) 25% off all vegetables 3) 20% off all store
        discount1 = {"discount_type": "Simple", "percent": 50, "level": "Product", "level_name": 1}
        discount2 = {"discount_type": "Simple", "percent": 25, "level": "Category", "level_name": "Vegetable"}
        discount3 = {"discount_type": "Simple", "percent": 20, "level": "Store", "level_name": ""}

        self.service.addDiscount("Feliks&Sons", "Son_A", "Add",
                                 discounts={"1": discount1, "2": discount2, "3": discount3})

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 5 cauliflower - 50%+25%+20% discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        # guest1 will have just 5 cabbage and 5 cauliflower - 50%+25%+20% discount cauliflower 25%+20% discount cabbage
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        # guest2 will have just 5 cabbage and 5 cauliflower and 5 banana - 50%+25%+20% discount cauliflower 25%+20% discount cabbage 20% banana
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 5)

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 5 * 8 * 0.05)
        self.assertTrue(basket1_price == 5 * 8 * 0.05 + 5 * 8 * 0.55)
        self.assertTrue(basket2_price == 5 * 8 * 0.05 + 5 * 8 * 0.55 + 5 * 8 * 0.8)

    def test_removeDiscountFromStore_Add_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add discount: 1) 50% off cauliflower 2) 25% off all vegetables 3) 20% off all store
        discount1 = {"discount_type": "Simple", "percent": 50, "level": "Product", "level_name": 1}
        discount2 = {"discount_type": "Simple", "percent": 25, "level": "Category", "level_name": "Vegetable"}
        discount3 = {"discount_type": "Simple", "percent": 20, "level": "Store", "level_name": ""}

        res = self.service.addDiscount("Feliks&Sons", "Son_A", "Add",
                                       discounts={"1": discount1, "2": discount2, "3": discount3})
        added_discount: Discount = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest2_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 5 cauliflower - 50% discount
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        # guest1 will have just 5 cabbage and 5 cauliflower - 50% discount cauliflower 25% discount cabbage
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        # guest2 will have just 5 cabbage and 5 cauliflower and 5 banana - 50% discount cauliflower 25% discount cabbage 20% banana
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 5)

        self.service.removeDiscount("Feliks&Sons", "Son_A", added_discount.get_discount_id())

        basket0_price = self.service.store_facade.getCart(guest0_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket1_price = self.service.store_facade.getCart(guest1_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()
        basket2_price = self.service.store_facade.getCart(guest2_entrance_id).get_Basket(
            "Feliks&Sons").calculateBasketPrice()

        self.assertTrue(basket0_price == 5 * 8)
        self.assertTrue(basket1_price == 5 * 8 + 5 * 8)
        self.assertTrue(basket2_price == 5 * 8 + 5 * 8 + 5 * 8)

    # =================================================================================================================
    # Use Case 4.2.e

    def test_newPurchasePolicyToStore_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 cauliflowers_K and then buy Melon
        rule1 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": "<=", "quantity": 5,
                 "child": {}}
        self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Product",
                                       level_name=11)

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 6 cauliflower and then try to buy melon - fail
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 6)
        with self.assertRaises(Exception):
            self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 11, 6)
        # guest1 will have buy 5 cauliflower then buy melon - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 11, 6)
        # guest1 will then add a cauliflower - fail
        with self.assertRaises(Exception):
            self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_newPurchasePolicyToStore_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 vegetables and then buy fruits
        rule1 = {"rule_type": "amount_of_category", "product": "", "category": "Vegetables", "operator": "<=",
                 "quantity": 5, "child": {}}
        self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Category",
                                       level_name="Fruits")

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest0 will just buy 3 cauliflower 3 cabbage and then will try to buy fruit - fail
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 3)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 2, 3)
        with self.assertRaises(Exception):
            self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 6)
        # guest1 will have buy 5 cauliflower and then will try to buy fruit - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 6)
        # guest1 will then add a vegetable - fail
        with self.assertRaises(Exception):
            self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_newPurchasePolicyToStore_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 cauliflowers_K
        rule1 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": "<=", "quantity": 5,
                 "child": {}}
        self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Basket",
                                       level_name="")

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        with self.assertRaises(Exception):
            # guest0 will just buy 6 cauliflower - fail
            self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 6)
        # guest1 will have buy 5 cauliflower - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        with self.assertRaises(Exception):
            # guest1 will just buy 1 more cauliflower - fail
            self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_newPurchasePolicyToStore_UserLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Ari", "password222")
        # Add policy: Ari can't buy banana
        rule1 = {"rule_type": "username_restriction", "product": -1, "category": "", "operator": "", "quantity": 0,
                 "user_field": "Ari", "child": {}}
        self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Product",
                                       level_name=10)

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        # guest can add banana
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 1)
        # guest can add mango
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 1)
        # Ari can add mango
        self.service.addToBasket("Ari", "Feliks&Sons", 9, 1)
        # Ari can't add banana
        with self.assertRaises(Exception):
            self.service.addToBasket("Ari", "Feliks&Sons", 10, 1)

    def test_removePurchasePolicyFromStore_ProductLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 cauliflowers_K and then buy Melon
        rule1 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": "<=", "quantity": 5,
                 "child": {}}
        res = self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Product",
                                             level_name=11)
        added_Policy: PurchasePolicy = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        self.service.removePurchasePolicy("Feliks&Sons", "Son_A", added_Policy.get_policy_id())

        # guest0 will just buy 6 cauliflower and then try to buy melon - no more fail
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 6)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 11, 6)
        # guest1 will have buy 5 cauliflower then buy melon - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 11, 6)
        # guest1 will then add a cauliflower - no more fail
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_removePurchasePolicyFromStore_CategoryLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 vegetables and then buy fruits
        rule1 = {"rule_type": "amount_of_category", "product": "", "category": "Vegetables", "operator": "<=",
                 "quantity": 5, "child": {}}
        res = self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Category",
                                             level_name="Fruits")
        added_Policy: PurchasePolicy = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        self.service.removePurchasePolicy("Feliks&Sons", "Son_A", added_Policy.get_policy_id())

        # guest0 will just buy 3 cauliflower 3 cabbage and then will try to buy fruit - no more fail
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 3)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 2, 3)
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 6)
        # guest1 will have buy 5 cauliflower and then will try to buy fruit - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 10, 6)
        # guest1 will then add a vegetable - no more fail
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_removePurchasePolicyFromStore_StoreLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        # Add policy: cannot have more than 5 cauliflowers_K
        rule1 = {"rule_type": "amount_of_product", "product": 1, "category": "", "operator": "<=", "quantity": 5,
                 "child": {}}
        res = self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Basket",
                                             level_name="")
        added_Policy: PurchasePolicy = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])

        self.service.removePurchasePolicy("Feliks&Sons", "Son_A", added_Policy.get_policy_id())

        # guest0 will just buy 6 cauliflower - no more fail
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 6)
        # guest1 will have buy 5 cauliflower - success
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 5)
        # guest1 will just buy 1 more cauliflower - no more fail
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 1, 1)

    def test_removePurchasePolicyFromStore_UserLevel_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Ari", "password222")
        # Add policy: Ari can't buy banana
        rule1 = {"rule_type": "username_restriction", "product": -1, "category": "", "operator": "", "quantity": 0,
                 "user_field": "Ari", "child": {}}
        res = self.service.addPurchasePolicy("Feliks&Sons", "Son_A", "PurchasePolicy", rule=rule1, level="Product",
                                             level_name=10)
        added_Policy: PurchasePolicy = ast.literal_eval(res.getReturnValue())

        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.removePurchasePolicy("Feliks&Sons", "Son_A", added_Policy.get_policy_id())

        # guest can add banana
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 9, 1)
        # guest can add mango
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 10, 1)
        # Ari can add mango
        self.service.addToBasket("Ari", "Feliks&Sons", 9, 1)
        # Ari can't add banana - now can
        self.service.addToBasket("Ari", "Feliks&Sons", 10, 1)

    # =================================================================================================================
    # Use Case 4.4.a
    def test_nominateShopOwnerByOwner_AllApprove_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.nominateStoreOwner("Son_A", "Son_E", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count)
        self.assertEqual(sond_notification_count_after, sond_notification_count)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        self.service.approveNomination("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        self.service.approveNomination("Son_B", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertTrue("Son_E" in staff_list)
        sona_notification_count_after_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after_after, sona_notification_count_after + 1)
        self.assertEqual(sonb_notification_count_after_after, sonb_notification_count_after + 1)
        self.assertEqual(sonc_notification_count_after_after, sonc_notification_count_after + 1)
        self.assertEqual(sond_notification_count_after_after, sond_notification_count_after + 1)
        self.assertEqual(sone_notification_count_after_after, sone_notification_count_after + 1)
        self.assertEqual(feliks_notification_count_after_after, feliks_notification_count_after + 1)

    def test_nominateShopOwnerByOwner_oneReject_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreOwner("SonA", "SonE", "Feliks&Sons")
        self.service.rejectNomination("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        with self.assertRaises(Exception):  # shouldn't approve now, agreement cancelled
            self.service.approveNomination("Son_B", "Son_E", "Feliks&Sons")

    def test_nominateShopOwnerByOwner_OneGotFireBeforeOtherApproved_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreOwner("Son_A", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        self.service.removeAccess("Feliks", "Son_B", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.approveNomination("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertTrue("Son_E" in staff_list)
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertTrue(FeliksSons_roles['Son_E']['role'] == 'Owner')
        sona_notification_count_after_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after_after, sona_notification_count_after + 1)
        self.assertEqual(sonb_notification_count_after_after, sonb_notification_count_after + 1)
        self.assertEqual(sonc_notification_count_after_after, sonc_notification_count_after + 1)
        self.assertEqual(sond_notification_count_after_after, sond_notification_count_after + 1)
        self.assertEqual(sone_notification_count_after_after, sone_notification_count_after + 1)
        self.assertEqual(feliks_notification_count_after_after, feliks_notification_count_after + 1)

    def test_nominateShopOwnerByOwner_LastOneToApproveFired_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreOwner("Son_A", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.approveNomination("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_E" in staff_list)
        self.service.removeAccess("Feliks", "Son_B", "Feliks&Sons")
        self.assertTrue("Son_E" in staff_list)
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertTrue(FeliksSons_roles['Son_E']['role'] == 'Owner')
        sona_notification_count_after_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after_after, sona_notification_count_after + 1)
        self.assertEqual(sonb_notification_count_after_after, sonb_notification_count_after + 1)
        self.assertEqual(sonc_notification_count_after_after, sonc_notification_count_after + 1)
        self.assertEqual(sond_notification_count_after_after, sond_notification_count_after + 1)
        self.assertEqual(sone_notification_count_after_after, sone_notification_count_after + 1)
        self.assertEqual(feliks_notification_count_after_after, feliks_notification_count_after + 1)

    # Use Case 4.4.b
    def test_nominateShopOwnerByFounder_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.nominateStoreOwner("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Son_A").getReturnValue()
        self.assertTrue("Son_E" in staff_list)
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertTrue(FeliksSons_roles['Son_E']['role'] == 'Owner')
        sona_notification_count_after_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after_after, sona_notification_count_after + 1)
        self.assertEqual(sonb_notification_count_after_after, sonb_notification_count_after + 1)
        self.assertEqual(sonc_notification_count_after_after, sonc_notification_count_after + 1)
        self.assertEqual(sond_notification_count_after_after, sond_notification_count_after + 1)
        self.assertEqual(sone_notification_count_after_after, sone_notification_count_after + 1)
        self.assertEqual(feliks_notification_count_after_after, feliks_notification_count_after + 1)

    # =================================================================================================================
    # Use Case 4.5.a
    def test_removeShopOwnerByHisNomineeOwner_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreOwner("Son_A", "Son_E", "Feliks&Sons")
        self.service.approveNomination("Feliks", "Son_E", "Feliks&Sons")
        self.service.approveNomination("Son_B", "Son_E", "Feliks&Sons")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.removeAccess("Son_A", "Son_E", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertTrue("Son_E" not in self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks"))
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count + 1)
        self.assertEqual(sond_notification_count_after, sond_notification_count + 1)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)

    # Use Case 4.5.b
    def test_removeShopOwnerByFounder_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.removeAccess("Feliks", "Son_A", "Feliks&Sons")  # should remove son_D as well
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertFalse("Son_A" in staff_list)
        self.assertFalse("Son_D" in staff_list)
        sona_notification_count_after_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after_after, sona_notification_count_after + 1)
        self.assertEqual(sonb_notification_count_after_after, sonb_notification_count_after + 1)
        self.assertEqual(sonc_notification_count_after_after, sonc_notification_count_after + 1)
        self.assertEqual(sond_notification_count_after_after, sond_notification_count_after + 1)
        self.assertEqual(sone_notification_count_after_after, sone_notification_count_after + 1)
        self.assertEqual(feliks_notification_count_after_after, feliks_notification_count_after + 1)

    # =================================================================================================================
    # Use Case 4.6.a
    def test_nominateShopManagerByOwner_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.nominateStoreManager("Son_A", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertTrue("Son_E" in staff_list)
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertTrue(FeliksSons_roles['Son_E']['role'] == 'Manager')
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count + 1)
        self.assertEqual(sond_notification_count_after, sond_notification_count + 1)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)

    # Use Case 4.6.b
    def test_nominateShopManagerByFounder_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.nominateStoreManager("Feliks", "Son_E", "Feliks&Sons")
        staff_list = self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks")
        self.assertTrue("Son_E" in staff_list)
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertTrue(FeliksSons_roles['Son_E']['role'] == 'Manager')
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count + 1)
        self.assertEqual(sond_notification_count_after, sond_notification_count + 1)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)

    # =================================================================================================================
    # Use Case 4.7.a
    def test_addPermissionToShopManager_Success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_D", "passwordDDD")
        SonD_permissions = self.service.getPermissions("Feliks&Sons", "Son_A", "Son_D")
        self.assertFalse(SonD_permissions.__contains__("ProductChange"))
        with self.assertRaises(Exception):
            self.service.editProductOfStore("Son_D", "Feliks&Sons", 10, price=10, quantity=10, categories="veggies")
        self.service.addPermission("Feliks&Sons", "Son_A", "Son_D", "ProductChange")
        SonD_permissions = self.service.getPermissions("Feliks&Sons", "Son_A", "Son_D")
        self.assertTrue(SonD_permissions.__contains__("ProductChange"))
        self.service.editProductOfStore("Son_D", "Feliks&Sons", 10, price=10, quantity=10, categories="veggies")

    # Use Case 4.7.b
    def test_removePermissionToShopManager_success(self):
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_D", "passwordDDD")
        SonD_permissions = self.service.getPermissions("Feliks&Sons", "Son_A", "Son_D")
        self.assertFalse(SonD_permissions.__contains__("ProductChange"))
        self.service.addPermission("Feliks&Sons", "Son_A", "Son_D", "ProductChange")
        SonD_permissions = self.service.getPermissions("Feliks&Sons", "Son_A", "Son_D")
        self.assertTrue(SonD_permissions.__contains__("ProductChange"))
        self.service.removePermissions("Feliks&Sons", "Son_A", "Son_D", "ProductChange")
        SonD_permissions = self.service.getPermissions("Feliks&Sons", "Son_A", "Son_D")
        self.assertFalse(SonD_permissions.__contains__("ProductChange"))
        with self.assertRaises(Exception):
            self.service.editProductOfStore("Son_D", "Feliks&Sons", 10, price=10, quantity=10, categories="veggies")

    # =================================================================================================================
    # Use Case 4.8.a
    def test_removeShopManagerByHisNomineeOwner_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreManager("Son_A", "Son_E", "Feliks&Sons")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.removeAccess("Son_A", "Son_E", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertTrue("Son_E" not in self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks"))
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertFalse(FeliksSons_roles.__contains__('Son_E'))
        self.assertEqual(sona_notification_count_after, sona_notification_count)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count)
        self.assertEqual(sond_notification_count_after, sond_notification_count)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count)

    # Use Case 4.8.b
    def test_removeShopManagerByFounder_Success(self):
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.logIn("Son_E", "passwordEEE")
        self.service.nominateStoreManager("Son_A", "Son_E", "Feliks&Sons")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.service.removeAccess("Feliks", "Son_E", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        sone_notification_count_after = self.service.getAllNotifications("Son_E").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertTrue("Son_E" not in self.service.getAllStaffMembersNames("Feliks&Sons", "Feliks"))
        FeliksSons_roles = ast.literal_eval(self.service.getStoreAllInfo("Feliks&Sons").getReturnValue()["accesses"])
        self.assertFalse(FeliksSons_roles.__contains__('Son_E'))
        self.assertEqual(sona_notification_count_after, sona_notification_count)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count)
        self.assertEqual(sond_notification_count_after, sond_notification_count)
        self.assertEqual(sone_notification_count_after, sone_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count)

    # =================================================================================================================
    # Use Case 4.9
    def test_closeStore_success(self):
        # also to check users can't see items from there after close
        # and that notifications were sent to all staff
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res_product = self.service.productSearchByName("Ca", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Feliks&Sons"].__len__() == 3)  # Cabbage, Cauliflower, Carrot
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        with self.assertRaises(Exception):
            self.service.closeStore("Son_A", "Feliks&Sons")
        self.service.closeStore("Feliks", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count + 1)
        self.assertEqual(sond_notification_count_after, sond_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)
        with self.assertRaises(Exception):
            self.service.getProductsByStore("Feliks&Sons", guest0_entrance_id)
        products_with_ca = ast.literal_eval(self.service.productSearchByName("Ca", guest0_entrance_id)["baskets"])
        self.assertTrue(products_with_ca == {})

    # Use Case 4.10
    def test_reopenStore_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res_product = self.service.productSearchByName("Ca", guest0_entrance_id)
        self.assertTrue(res_product.getReturnValue()["Feliks&Sons"].__len__() == 3)  # Cabbage, Cauliflower, Carrot
        self.service.logIn("Feliks", "password333")
        self.service.logIn("Son_A", "passwordAAA")
        self.service.logIn("Son_B", "passwordBBB")
        self.service.logIn("Son_C", "passwordCCC")
        self.service.logIn("Son_D", "passwordDDD")
        self.service.closeStore("Feliks", "Feliks&Sons")
        sona_notification_count = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        feliks_notification_count = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        with self.assertRaises(Exception):
            self.service.openStore("Son_A", "Feliks&Sons")
        self.service.openStore("Feliks", "Feliks&Sons")
        sona_notification_count_after = self.service.getAllNotifications("Son_A").getReturnValue().__len__()
        sonb_notification_count_after = self.service.getAllNotifications("Son_B").getReturnValue().__len__()
        sonc_notification_count_after = self.service.getAllNotifications("Son_C").getReturnValue().__len__()
        sond_notification_count_after = self.service.getAllNotifications("Son_D").getReturnValue().__len__()
        feliks_notification_count_after = self.service.getAllNotifications("Feliks").getReturnValue().__len__()
        self.assertEqual(sona_notification_count_after, sona_notification_count + 1)
        self.assertEqual(sonb_notification_count_after, sonb_notification_count + 1)
        self.assertEqual(sonc_notification_count_after, sonc_notification_count + 1)
        self.assertEqual(sond_notification_count_after, sond_notification_count + 1)
        self.assertEqual(feliks_notification_count_after, feliks_notification_count + 1)
        self.service.getProductsByStore("Feliks&Sons", guest0_entrance_id)
        products_with_ca = ast.literal_eval(self.service.productSearchByName("Ca", guest0_entrance_id)["baskets"])
        self.assertTrue(products_with_ca.__len__() == 3)

    # Use Case 4.11
    def test_requestStoreStaffInfo_success(self):
        self.service.logIn("Feliks", "password333")
        accesses_list = ast.literal_eval(self.service.getStaffInfo("Feliks", "Feliks&Sons").getReturnValue())
        self.assertTrue(accesses_list.__len__() == 5)
        access_SonD_names = self.service.getPermissions("Feliks&Sons", "Feliks", "Son_D").getReturnValue().keys()
        self.assertTrue(access_SonD_names.__len__() == 2)

    # Use Case 4.13
    def test_OwnerRequestStorePurchaseHistory_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 3, 5)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        self.service.purchaseCart(guest1_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        PurchaseHistory_FeliksSons = ast.literal_eval(
            self.service.getStorePurchaseHistory("Feliks", "Feliks&Sons").getReturnValue())
        self.assertTrue(PurchaseHistory_FeliksSons.__len__() == 2)
        guest0_transaction = PurchaseHistory_FeliksSons[0]
        self.assertTrue(guest0_transaction['username'] == guest0_entrance_id)
        self.assertTrue(guest0_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest0_transaction['products'][0][1] == 'Cauliflower_K')
        self.assertTrue(guest0_transaction['products'][0][2] == 5)
        self.assertTrue(guest0_transaction['overall_price'] == 8 * 5)
        guest1_transaction = PurchaseHistory_FeliksSons[1]
        self.assertTrue(guest1_transaction['username'] == guest1_entrance_id)
        self.assertTrue(guest1_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest1_transaction['products'][0][1] == 'Cabbage_K')
        self.assertTrue(guest1_transaction['products'][0][2] == 5)
        self.assertTrue(guest1_transaction['products'][1][1] == 'Broccoli_K')
        self.assertTrue(guest1_transaction['products'][1][2] == 5)
        self.assertTrue(guest1_transaction['overall_price'] == 8 * 5 + 8 * 5)

    # =================================================================================================================
    # Use Case 5.13
    def test_MemberRequestStorePurchaseHistory_success(self):
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 3, 5)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        self.service.purchaseCart(guest1_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        PurchaseHistory_FeliksSons = ast.literal_eval(
            self.service.getStorePurchaseHistory("Son_A", "Feliks&Sons").getReturnValue())
        self.assertTrue(PurchaseHistory_FeliksSons.__len__() == 2)
        guest0_transaction = PurchaseHistory_FeliksSons[0]
        self.assertTrue(guest0_transaction['username'] == guest0_entrance_id)
        self.assertTrue(guest0_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest0_transaction['products'][0][1] == 'Cauliflower_K')
        self.assertTrue(guest0_transaction['products'][0][2] == 5)
        self.assertTrue(guest0_transaction['overall_price'] == 8 * 5)
        guest1_transaction = PurchaseHistory_FeliksSons[1]
        self.assertTrue(guest1_transaction['username'] == guest1_entrance_id)
        self.assertTrue(guest1_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest1_transaction['products'][0][1] == 'Cabbage_K')
        self.assertTrue(guest1_transaction['products'][0][2] == 5)
        self.assertTrue(guest1_transaction['products'][1][1] == 'Broccoli_K')
        self.assertTrue(guest1_transaction['products'][1][2] == 5)
        self.assertTrue(guest1_transaction['overall_price'] == 8 * 5 + 8 * 5)


""" ---------------------- (2.6) Admin Functionality tests ---------------------- """
class Test_Use_Case_2_6_transactions(TestCase):
    def setUp(self):
        self.service = Service(config_file=default_config, load_file=stores_load, send_notification_call=true_lambda)

    def tearDown(self):
        # Reset the singleton instance of Service
        Service._instance = None

    # Use Case 2.6.2
    def test_AdminBanMember_success(self):
        self.service.logIn("admin", "12341234")
        self.service.logIn("Amiel", "password111")
        self.service.removePermissionFreeMember("admin", "Amiel")
        online_member_dict = ast.literal_eval(self.service.getAllOnlineMembers("admin").getReturnValue())
        self.assertFalse(self.service.getAllOnlineMembers("admin").getReturnValue().__contains__("Amiel"))
        self.assertFalse(self.service.logIn("Amiel", "password111").getStatus())
        self.service.returnPermissionFreeMember("admin", "Amiel")
        self.service.logIn("Amiel", "password111")
        self.assertTrue(self.service.getAllOnlineMembers("admin").getReturnValue().__contains__("Amiel"))

    # Use Case 2.6.4
    def test_StorePurchaseHistoryAdmin_success(self):
        self.service.logIn("admin", "12341234")
        res = self.service.loginAsGuest()
        guest0_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        res = self.service.loginAsGuest()
        self.assertTrue(res.getStatus())
        guest1_entrance_id = int(ast.literal_eval(res.getReturnValue())["entrance_id"])
        self.service.addToBasket(guest0_entrance_id, "Feliks&Sons", 1, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 2, 5)
        self.service.addToBasket(guest1_entrance_id, "Feliks&Sons", 3, 5)
        self.service.purchaseCart(guest0_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        self.service.purchaseCart(guest1_entrance_id, "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        PurchaseHistory_FeliksSons = ast.literal_eval(
            self.service.getStorePurchaseHistory("admin", "Feliks&Sons").getReturnValue())
        self.assertTrue(PurchaseHistory_FeliksSons.__len__() == 2)
        guest0_transaction = PurchaseHistory_FeliksSons[0]
        guest1_transaction = PurchaseHistory_FeliksSons[1]
        if guest0_transaction['username'] != str(guest0_entrance_id):
            guest0_transaction = PurchaseHistory_FeliksSons[1]
            guest1_transaction = PurchaseHistory_FeliksSons[0]
        guest0_products = ast.literal_eval(guest0_transaction['products'])
        guest1_products = ast.literal_eval(guest1_transaction['products'])

        self.assertTrue(guest0_transaction['username'] == str(guest0_entrance_id))
        self.assertTrue(guest0_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest0_products[0][1] == 'Cauliflower_K')
        self.assertTrue(guest0_products[0][2] == 5)
        self.assertTrue(guest0_transaction['overall_price'] == 40)
        self.assertTrue(guest1_transaction['username'] == str(guest1_entrance_id))
        self.assertTrue(guest1_transaction['storename'] == "Feliks&Sons")
        self.assertTrue(guest1_products[0][1] == 'Cabbage_K')
        self.assertTrue(guest1_products[0][2] == 5)
        self.assertTrue(guest1_products[1][1] == 'Broccoli_K')
        self.assertTrue(guest1_products[1][2] == 5)
        self.assertTrue(guest1_transaction['overall_price'] == 80)

    def test_UserPurchaseHistoryAdmin_success(self):
        self.service.logIn("admin", "12341234")
        self.service.logIn("Amiel", "password111")
        self.service.addToBasket("Amiel", "Feliks&Sons", 1, 5)
        self.service.addToBasket("Amiel", "Robin&Daughters", 2, 5)
        self.service.addToBasket("Amiel", "Robin&Daughters", 3, 5)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        PurchaseHistory_Amiel = ast.literal_eval(
            self.service.getMemberPurchaseHistory("admin", "Amiel").getReturnValue())
        self.assertTrue(PurchaseHistory_Amiel.__len__() == 1)
        transaction = next(iter(PurchaseHistory_Amiel.values()))
        FStore_transaction = transaction['products']["Feliks&Sons"]
        RStore_transaction = transaction['products']["Robin&Daughters"]
        self.assertTrue(FStore_transaction[0][1] == 'Cauliflower_K')
        self.assertTrue(FStore_transaction[0][2] == 5)
        self.assertTrue(RStore_transaction[0][1] == 'Ketchup')
        self.assertTrue(RStore_transaction[0][2] == 5)
        self.assertTrue(RStore_transaction[1][1] == 'Mustard')
        self.assertTrue(RStore_transaction[1][2] == 5)

    # Use Case 2.6.6
    def test_AdminGetInfoMembersOnOff_success(self):
        self.service.logIn("admin", "12341234")
        self.service.logIn("Amiel", "password111")
        online_members_dict = ast.literal_eval(self.service.getAllOnlineMembers("admin").getReturnValue())
        self.assertTrue(online_members_dict.__len__() == 3) # Feliks Robin Amiel
        self.assertTrue(online_members_dict.keys().__contains__("Amiel"))
        self.assertTrue(online_members_dict.keys().__contains__("Robin"))
        self.assertTrue(online_members_dict.keys().__contains__("Feliks"))
        offline_members_dict = ast.literal_eval(self.service.getAllOfflineMembers("admin").getReturnValue())
        self.assertTrue(offline_members_dict.__len__() == 7)  # Ari and SonA-SonF = 7
        self.assertTrue(offline_members_dict.keys().__contains__("Ari"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_A"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_B"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_C"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_D"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_E"))
        self.assertTrue(offline_members_dict.keys().__contains__("Son_F"))

    def test_AdminGetInfoMember_success(self):
        self.service.logIn("admin", "12341234")
        self.service.logIn("Amiel", "password111")
        self.service.addToBasket("Amiel", "Feliks&Sons", 1, 5)
        self.service.addToBasket("Amiel", "Robin&Daughters", 2, 5)
        self.service.addToBasket("Amiel", "Robin&Daughters", 3, 5)
        self.service.purchaseCart("Amiel", "4580020345672134", "12/26", "Amiel saad", "555", "123456789",
                                  "some_address", "be'er sheva", "Israel", "1234567")
        amiel_info = ast.literal_eval(ast.literal_eval(self.service.getMemberInfo("admin", "Amiel").getReturnValue())['member'])
        self.assertTrue(amiel_info['username'] == "Amiel")
        self.assertTrue(amiel_info['email'] == "amiel@gmail.com")
        self.assertTrue(amiel_info['accesses'] == '{}')
        Feliks_info = ast.literal_eval(ast.literal_eval(self.service.getMemberInfo("admin", "Feliks").getReturnValue())['member'])
        self.assertTrue(Feliks_info['username'] == "Feliks")
        self.assertTrue(Feliks_info['email'] == "feliks@gmail.com")
        Feliks_accesses = ast.literal_eval(Feliks_info['accesses'])
        self.assertTrue(Feliks_accesses["Feliks&Sons"]["store"]["store_name"] == "Feliks&Sons")
        self.assertTrue(Feliks_accesses["Feliks&Sons"]["role"] == "Founder")
        SonA_info = ast.literal_eval(ast.literal_eval(self.service.getMemberInfo("admin", "Son_A").getReturnValue())['member'])
        self.assertTrue(SonA_info['username'] == "Son_A")
        self.assertTrue(SonA_info['email'] == "sona@gmail.com")
        SonA_accesses = ast.literal_eval(SonA_info['accesses'])
        self.assertTrue(SonA_accesses["Feliks&Sons"]["store"]["store_name"] == "Feliks&Sons")
        self.assertTrue(SonA_accesses["Feliks&Sons"]["role"] == "Owner")


if __name__ == '__main__':
    unittest.main()
