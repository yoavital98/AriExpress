import json
import unittest

from peewee import SqliteDatabase


from ProjectCode.DAL.AccessModel import AccessModel
from ProjectCode.DAL.AccessStateModel import AccessStateModel
from ProjectCode.DAL.AdminModel import AdminModel
from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.BidModel import BidModel
from ProjectCode.DAL.GuestModel import GuestModel
from ProjectCode.DAL.DiscountModel import DiscountModel
#from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.DAL.ProductBasketModel import ProductBasketModel
from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.DAL.ProductStoreTransactionModel import ProductStoreTransactionModel
from ProjectCode.DAL.ProductUserTransactionModel import ProductUserTransactionModel
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.StoreOfUserTransactionModel import StoreOfUserTransactionModel
from ProjectCode.DAL.StoreTransactionModel import StoreTransactionModel
from ProjectCode.DAL.SystemModel import SystemModel
from ProjectCode.DAL.UserTransactionModel import UserTransactionModel
from ProjectCode.Domain.ExternalServices.TransactionObjects.StoreTransaction import StoreTransaction
from ProjectCode.Domain.ExternalServices.TransactionObjects.UserTransaction import UserTransaction
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Domain.Repository.BidsRepository import BidsRepository
from ProjectCode.Domain.StoreFacade import StoreFacade


class MyTestCase(unittest.TestCase):

    def setUp(self):
        # db = SqliteDatabase('database.db')
        # db.connect()
        # db.drop_tables([SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel, BasketModel,
        #                 ProductBasketModel, DiscountModel, AdminModel, GuestModel])
        # db.create_tables(
        #     [SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel, BasketModel,
        #      ProductBasketModel, DiscountModel, AdminModel, GuestModel])
        send_notification_lambda = lambda self, receiver_id, notification_id, type, subject: True
        config = "../../default_config.json"
        with open(config, 'r') as f:
            config_data: dict = json.load(f)
        self.store_facade = StoreFacade(config_data, send_notification_call=send_notification_lambda)
        self.store_facade.register("Ari", "password123", "ari@gmail.com")
        self.store_facade.register("Jane", "password456", "jane.doe@example.com")
        self.store_facade.register("Feliks", "password456", "fe.doe@example.com")
        self.member1: Member = self.store_facade.members.get("Ari")
        self.member2: Member = self.store_facade.members.get("Jane")
        self.member3: Member = self.store_facade.members.get("Feliks")
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore("Ari", "Store1")
        self.store_facade.createStore("Ari", "Store2")
        self.store1: Store = self.store_facade.stores.get("Store1")
        self.store2: Store = self.store_facade.stores.get("Store2")
        self.store_facade.addNewProductToStore("Ari", "Store1", "paper", 10, 500, "paper")
        self.store_facade.addNewProductToStore("Ari", "Store1", "oreo", 10, 10, "food")
        self.item_paper: Product = self.store1.getProductById(1, "Ari")
        self.oreo: Product = self.store1.getProductById(2, "Ari")


        self.sub_rule = {"rule_type": "amount_of_product", "product_id": self.item_paper.get_product_id(),
                         "operator": ">=", "quantity": 1, "category": "", "child": {}}
        self.rule = {"rule_type": "amount_of_product", "product_id": self.oreo.get_product_id(),
                     "operator": ">=", "quantity": 1, "category": "",
                     "child": {"logic_type": "OR", "rule": self.sub_rule}}
        self.discount = ConditionedDiscount(10, "Product", self.oreo.get_product_id(), self.rule)
        self.discount2 = SimpleDiscount(10, "Basket", "")
        db = SqliteDatabase('database.db')
        db.connect()
        #StoreProduct = StoreModel.products.get_through_model()
        db.drop_tables([SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel,
                        BasketModel, ProductBasketModel, DiscountModel, AdminModel, GuestModel, UserTransactionModel,
                        StoreOfUserTransactionModel, ProductUserTransactionModel, StoreTransactionModel,
                        ProductStoreTransactionModel, BidModel])
        db.create_tables([SystemModel, ProductModel, StoreModel, AccessModel, AccessStateModel, MemberModel,
                          BasketModel, ProductBasketModel, DiscountModel, AdminModel, GuestModel, UserTransactionModel,
                        StoreOfUserTransactionModel, ProductUserTransactionModel, StoreTransactionModel,
                          ProductStoreTransactionModel, BidModel])

    # ------ AccessRepository Tests ------

    def test_Orm_access_nominations(self):
        #MemberModel.create(user_name=self.member1.user_name, password=self.member1.password, email=self.member1.email)
        #StoreModel.create(store_name="Store1")
        self.store_facade.nominateStoreOwner("Ari",  "Jane", "Store1")
        self.store_facade.nominateStoreOwner("Ari", "Feliks", "Store1")
        print(self.store1.get_accesses()["Ari"].get_nominations())

    def test_Orm_access_del(self):
        MemberModel.create(user_name=self.member1.user_name, password=self.member1.password, email=self.member1.email)
        StoreModel.create(store_name="Store1")
        access = Access(self.store1, self.member1, "Ari")
        access.setAccess("Founder")
        self.store1.accesses_test["Ari"] = access
        del self.store1.accesses_test["Ari"]




    def test_Orm_user_access(self):
        MemberModel.create(user_name=self.member1.user_name, password=self.member1.password, email=self.member1.email)
        StoreModel.create(store_name="Store1")
        access = Access(self.store1, self.member1, "Ari")
        access.setAccess("Founder")
        self.store1.accesses_test["Store1"] = access
        self.assertEqual(self.member1.accesses_test[None][0].__str__(),"Ari Store1 Founder Ari")

    def test_Orm_user_keys(self):
        MemberModel.create(user_name=self.member1.user_name, password=self.member1.password, email=self.member1.email)
        StoreModel.create(store_name="Store1")
        access = Access(self.store1, self.member1, "Ari")
        access.setAccess("Founder")
        self.store1.accesses_test["Store1"] = access
        print(self.member1.accesses_test.keys())

    def test_Orm_store_access_keys(self):
        StoreModel.create(store_name=self.store1.get_store_name())
        MemberModel.create(user_name=self.member1.get_username(), password=self.member1.get_password(),
                                       email=self.member1.get_email())
        MemberModel.create(user_name=self.member2.get_username(), password=self.member2.get_password(), email=self.member2.get_email())

        new_access = Access(self.store1, self.member1, "Ari")
        new_access.setAccess("Founder")
        self.store1.accesses_test[self.member1.get_username()] = new_access
        print(self.store1.accesses_test.keys())

    def test_Orm_store_access_values(self):
        StoreModel.create(store_name=self.store1.get_store_name())
        MemberModel.create(user_name=self.member1.get_username(), password=self.member1.get_password(),
                           email=self.member1.get_email())
        MemberModel.create(user_name=self.member2.get_username(), password=self.member2.get_password(),
                           email=self.member2.get_email())

        new_access = Access(self.store1, self.member1, "Ari")
        new_access.setAccess("Founder")
        self.store1.accesses_test[self.member1.get_username()] = new_access
        print(self.store1.accesses_test.values())


    # def test_Orm_store_items(self):
    #     self.store_facade.stores["Hi"] = Store("Hi")
    #     self.store_facade.stores["Bye"] = Store("Bye")
    #     for key, value in self.store_facade.stores.items():
    #         print(key, value.get_store_name())

    # ------ MemberRepository Tests ------

    def test_Orm_member_get(self):
        self.store_facade.members_test[self.member1.get_username()] = self.member1
        self.store_facade.members_test[self.member2.get_username()] = self.member2
        print(self.store_facade.members_test.get("Ari").get_username())
        print(self.store_facade.members_test.get("Jane").get_username())
        print([user.get_username() for user in self.store_facade.members_test.get()])
        print(self.store_facade.members_test.keys())
        print([user.get_username() for user in self.store_facade.members_test.values()])

    # ------ ProductRepository Tests ------

    def test_Orm_product_keys_values(self):
        StoreModel.create(store_name=self.store1.get_store_name())
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        print(self.store1.prods[self.item_paper.get_product_id()].get_quantity())
        self.item_paper.quantity = 123
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        print(self.store1.prods[self.item_paper.get_product_id()].get_quantity())

        print(self.store1.prods.keys())
        print(self.store1.prods.values())

    # ------ ProductRepository Tests ------

    def test_Orm_store(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        print(self.store_facade.stores_test["Store1"].get_store_name())
        print(self.store_facade.stores_test[None][0].get_store_name())
        print(self.store_facade.stores_test["Store1"].prods[self.item_paper.get_product_id()].get_name())
        #del self.store_facade.stores_test["Store1"]

    def test_Orm_store_del(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        self.store1.prods[self.oreo.get_product_id()] = self.oreo
        del self.store_facade.stores_test["Store1"]

    def test_Orm_store_keys_values(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.store_facade.stores_test["Store2"] = self.store2
        print(self.store_facade.stores_test.keys())
        print(self.store_facade.stores_test.values())


    # ------ BasketRepository Tests ------

    def test_Orm_create_basket(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.member1.cart.basket_test["Store1"] = Basket(self.member1.get_username(), self.store1)
        basket = self.member1.cart.basket_test["Store1"]
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        basket.products_test[self.item_paper.get_product_id()] = (self.item_paper, 5, self.item_paper.get_price())
        print(basket.products_test[self.item_paper.get_product_id()])
        print(basket.products_test[None])
        print(self.member1.cart.basket_test["Store1"])
        print(self.member1.cart.basket_test[None])

        del [self.member1.cart.basket_test["Store1"]]

    # ------ AdminRepository Tests ------
    def test_Orm_create_and_get_admin(self):
        admin: Admin = Admin("Ari", "password", "a@a")
        admin2: Admin = Admin("Rubs", "password", "rubbbs@gmail.com")# create and get
        self.store_facade.admins_test[admin.get_username()] = admin
        print(self.store_facade.admins_test.get(admin.get_username()).get_username())
        print(self.store_facade.admins_test.get(admin.get_username()).get_password())
        print(self.store_facade.admins_test.get(admin.get_username()).get_email())
        self.store_facade.admins_test[admin2.get_username()] = admin2
        print(self.store_facade.admins_test.get(admin2.get_username()).get_username())
        print(self.store_facade.admins_test.get(admin2.get_username()).get_password())
        print(self.store_facade.admins_test.get(admin2.get_username()).get_email())

    def test_Orm_del_and_contains_admin(self):
        admin: Admin = Admin("Ari", "password", "a@a")
        admin2: Admin = Admin("Rubs", "password", "rubbbs@gmail.com")  # create and get
        self.store_facade.admins_test[admin.get_username()] = admin
        self.store_facade.admins_test[admin2.get_username()] = admin2
        self.store_facade.admins_test.__delitem__("Ari")
        print(self.store_facade.admins_test.__contains__("Ari"))
        print(self.store_facade.admins_test.__contains__("Rubs"))

    def test_Orm_keys_admin(self):
        admin: Admin = Admin("Ari", "password", "a@a")
        admin2: Admin = Admin("Rubs", "password", "rubbbs@gmail.com")  # create and get
        self.store_facade.admins_test[admin.get_username()] = admin
        self.store_facade.admins_test[admin2.get_username()] = admin2
        print(self.store_facade.admins_test.keys())

    # ------ GuestRepository Tests ------
    def test_Orm_createAndGet_guest(self):
        guest: Guest = Guest("0")
        guest2: Guest = Guest("1")
        self.store_facade.onlineGuests_test[guest.get_entrance_id()] = guest
        self.store_facade.onlineGuests_test[guest2.get_entrance_id()] = guest2
        print(self.store_facade.onlineGuests_test.get("0").get_entrance_id())
        print(self.store_facade.onlineGuests_test.get("1").get_entrance_id())

    def test_Orm_del_and_contains_guest(self):
        guest: Guest = Guest("0")
        guest2: Guest = Guest("1")
        self.store_facade.onlineGuests_test[guest.get_entrance_id()] = guest
        self.store_facade.onlineGuests_test[guest2.get_entrance_id()] = guest2
        self.store_facade.onlineGuests_test.__delitem__("0")
        print(self.store_facade.onlineGuests_test.__contains__("0"))
        print(self.store_facade.onlineGuests_test.__contains__("1"))
    def test_Orm_keys_guest(self):
        guest: Guest = Guest("0")
        guest2: Guest = Guest("1")
        self.store_facade.onlineGuests_test[guest.get_entrance_id()] = guest
        self.store_facade.onlineGuests_test[guest2.get_entrance_id()] = guest2
        print(self.store_facade.onlineGuests_test.keys())

    # ------ DiscountRepository Tests ------

    def test_Orm_create_discount(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        self.store1.prods[self.oreo.get_product_id()] = self.oreo
        self.store1.get_discount_policy().discounts_test[1] = self.discount
        print(self.store1.get_discount_policy().discounts_test[1].rule["rule_type"])

        del self.store1.get_discount_policy().discounts_test[1]

    def test_Orm_multiple_discounts(self):
        self.store_facade.stores_test["Store1"] = self.store1
        self.store1.prods[self.item_paper.get_product_id()] = self.item_paper
        self.store1.prods[self.oreo.get_product_id()] = self.oreo
        self.store1.get_discount_policy().discounts_test[1] = self.discount
        self.store1.get_discount_policy().discounts_test[2] = self.discount2
        print(self.store1.get_discount_policy().discounts_test[None])

        # ------ StoreTransactionRepository Tests ------

    def test_Orm_create_and_get_storeTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        store_transaction = StoreTransaction(1, 1, "Ari", "AriExpress", products, 500)
        self.store_facade.store_transactions_test.add(store_transaction)
        store_transactions_after_get: list = self.store_facade.store_transactions_test.__getitem__("AriExpress")
        for x in store_transactions_after_get:
            print(x.get_transaction_id())
            print(x.get_products())
            print(x.get_storename())


    def test_Orm_del_and_contains_storeTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        user_transaction = StoreTransaction(1, 1, "Ari", "AriExpress", products, 500)
        self.store_facade.store_transactions_test.add(user_transaction)
        products = list()
        products.append((7, "zero", 50, 500))
        user_transaction2 = StoreTransaction(2, 1, "Ari", "AmielExpress", products, 500)
        self.store_facade.store_transactions_test.add(user_transaction2)
        self.store_facade.store_transactions_test.__delitem__(1)
        print(self.store_facade.store_transactions_test.__contains__(1))
        print(self.store_facade.store_transactions_test.__contains__(2))
    def test_Orm_keys_storeTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        user_transaction = StoreTransaction(1, 1, "Ari", "AriExpress", products, 500)
        self.store_facade.store_transactions_test.add(user_transaction)
        products = list()
        products.append((7, "zero", 50, 500))
        user_transaction2 = StoreTransaction(2, 1, "Ari", "AmielExpress", products, 500)
        self.store_facade.store_transactions_test.add(user_transaction2)
        print(self.store_facade.user_transactions_test.keys())

        # ------ UserTransactionRepository Tests ------

    def test_Orm_create_and_get_userTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        dict_for_products: dict = {"AriExpress": products}
        user_transaction = UserTransaction(1, 1, "Ari", dict_for_products, 500)
        self.store_facade.user_transactions_test.add(user_transaction)
        user_transactions_after_get: list = self.store_facade.user_transactions_test.__getitem__("Ari")
        for x in user_transactions_after_get:
            print(x.get_transaction_id())
            print(x.get_products())
            print(x.get_overall_price())

    def test_Orm_del_and_contains_userTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        dict_for_products: dict = {"AriExpress": products}
        user_transaction = UserTransaction(1, 1, "Ari", dict_for_products, 500)
        self.store_facade.user_transactions_test.add(user_transaction)
        products = list()
        products.append((1, "cariot", 50, 500))
        dict_for_products: dict = {"AmielExpress": products}
        user_transaction = UserTransaction(5, 1, "Amiel", dict_for_products, 500)
        self.store_facade.user_transactions_test.add(user_transaction)
        self.store_facade.user_transactions_test.__delitem__(1)
        print(self.store_facade.user_transactions_test.__contains__(1))
        print(self.store_facade.user_transactions_test.__contains__(5))

    def test_Orm_keys_storeTransaction(self):
        products = list()
        products.append((5, "cola", 50, 500))
        dict_for_products: dict = {"AriExpress": products}
        user_transaction = UserTransaction(1, 1, "Ari", dict_for_products, 500)
        self.store_facade.user_transactions_test.add(user_transaction)
        products = list()
        products.append((1, "cariot", 50, 500))
        dict_for_products: dict = {"AmielExpress": products}
        user_transaction = UserTransaction(5, 1, "Amiel", dict_for_products, 500)
        self.store_facade.user_transactions_test.add(user_transaction)
        print(self.store_facade.user_transactions_test.keys())

    #------------------- BidRepo -------------------------------
    def test_Orm_create_and_get_Bid(self):
        bid: Bid = Bid(0,"Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[0] = bid
        bid: Bid = bid_repository.get(0)
        print(bid.bid_id), print(bid.get_offer()), print(bid.get_username())
        bid: Bid = Bid(1, "Feliks", "some_Store", 500, 1, 5)
        bid_repository[1] = bid
        bid: Bid = bid_repository.get(1)
        print(bid.bid_id), print(bid.get_offer()), print(bid.get_username())

    def test_Orm_del_and_contains_BidsTransaction(self):
        bid: Bid = Bid(0, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[0] = bid
        print(bid_repository.contains(0))
        bid: Bid = Bid(1, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[1] = bid
        print(bid_repository.contains(1))
        bid_repository.__delitem__(0)
        print(bid_repository.contains(0))
        bid_repository.__delitem__(1)
        print(bid_repository.contains(1))
    def test_Orm_keys_BidsTransaction(self):
        bid: Bid = Bid(0, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[0] = bid
        print(bid_repository.keys())
        bid: Bid = Bid(1, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[1] = bid
        print(bid_repository.keys())

    def test_Orm_get_by_storename_BidsTransaction(self):
        bid: Bid = Bid(0, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[0] = bid
        bid: Bid = Bid(1, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[1] = bid
        bid: Bid = Bid(2, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[2] = bid
        bid: Bid = Bid(3, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[3] = bid
        list_Store: list = bid_repository.get_by_storename("Store")
        print(list_Store)
        list_Store: list = bid_repository.get_by_storename("some_Store")
        print(list_Store)

    def test_Orm_get_by_username_BidsTransaction(self):
        bid: Bid = Bid(0, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[0] = bid
        bid: Bid = Bid(1, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[1] = bid
        bid: Bid = Bid(2, "Ari", "Store", 500, 1, 5)
        bid_repository = BidsRepository()
        bid_repository[2] = bid
        bid: Bid = Bid(3, "Feliks", "some_Store", 300, 2, 8)
        bid_repository[3] = bid
        list_Store: list = bid_repository.get_by_username("Ari")
        print(list_Store)
        list_Store: list = bid_repository.get_by_username("Feliks")
        print(list_Store)

if __name__ == '__main__':
    unittest.main()
