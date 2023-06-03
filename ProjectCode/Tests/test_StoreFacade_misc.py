import unittest
from unittest import TestCase

from ProjectCode.Domain.ExternalServices.TransactionHistory import TransactionHistory
from ProjectCode.Domain.MarketObjects.Basket import Basket
from ProjectCode.Domain.MarketObjects.Cart import Cart

from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.StoreObjects.LogicComponents.LogicComp import LogicComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Product import Product
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.StoreFacade import StoreFacade
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
from ProjectCode.Domain.MarketObjects.Access import Access
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member



class TestStoreFacade(TestCase):

    def setUp(self):
        self.store_facade = StoreFacade()
        self.store_facade.admins["Ari"] = Admin("Ari", "password123", "ari@gmail.com")
        self.store_facade.admins["Rubin"] = Admin("Rubin", "password123", "rubin@gmail.com")
        self.store_facade.register("Feliks", "password456", "feliks@gmail.com")
        self.store_facade.register("Amiel", "password789", "amiel@gmail.com")
        self.store_facade.register("YuvalMelamed", "PussyDestroyer69", "fuck@gmail.com")
        self.store_facade.loginAsGuest()
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.createStore("Feliks", "AriExpress")
        self.my_store: Store = self.store_facade.stores.get("AriExpress")
        self.store_facade.addNewProductToStore("Feliks", "AriExpress", "paper", 10, 500, "paper")
        self.item_paper: Product = self.my_store.getProductById(1, "Feliks")
        self.store_facade.logOut("Feliks")


    # __getAdmin
    def test_getAdmin_success(self):
        admin: Admin = self.store_facade.getAdmin("Ari")
        self.assertTrue(admin.user_name == "Ari" and admin.email == "ari@gmail.com")
        admin2: Admin = self.store_facade.getAdmin("Rubin")
        self.assertTrue(admin2.user_name == "Rubin" and admin2.email == "rubin@gmail.com")

    def test_getAdmin_fail(self):
        with self.assertRaises(Exception):
            admin: Admin = self.store_facade.getAdmin("Felix")
            self.assertTrue(admin.user_name == "Felix" and admin.email == "felix@gmail.com")
    # __getOnlineMemberOnly
    def test_getOnlineMemberOnly_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        member: Member = self.store_facade.getOnlineMemberOnly("Feliks")
        self.assertTrue(member.user_name == "Feliks" and member.email == "feliks@gmail.com")

    def test_getOnlineMemberOnly_fail(self):
        with self.assertRaises(Exception):
            member: Member = self.store_facade.getOnlineMemberOnly("Feliks")
            self.assertTrue(member.user_name == "Feliks" and member.email == "feliks@gmail.com")

    # __getUserOrMember
    def test_getUserOrMember_getUser_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        member: Member = self.store_facade.getUserOrMember("Feliks")
        self.assertTrue(member.user_name == "Feliks" and member.email == "feliks@gmail.com")

    def test_getUserOrMember_getGuest_success(self):
        guest: Guest = self.store_facade.getUserOrMember(0)
        self.assertTrue(guest.get_entrance_id() == "0")

    def test_getUserOrMember_getGuest_fail(self):
        with self.assertRaises(Exception):
            guest: Guest = self.store_facade.getUserOrMember(5)

    def test_getUserOrMember_getMember_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.logInAsMember("Feliks", "password456")
            member: Member = self.store_facade.getUserOrMember("someone")
    # addAdmin
    def test_addAdmin_success(self):
        self.store_facade.addAdmin("Ari", "yoav", "password789", "yoav@gmail.com")
        self.assertTrue(self.store_facade.admins.keys().__contains__("yoav"))


    def test_addAdmin_userNotAdmin_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.addAdmin("Felix", "yoav", "password789", "yoav@gmail.com")
        self.assertTrue(not self.store_facade.admins.keys().__contains__("yoav"))

    def test_addAdmin_newAdminAlreadyAdmin_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.addAdmin("Ari", "Rubin", "password789", "yoav@gmail.com")


    def test_addAdmin_weakPassword_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.addAdmin("Ari", "Rubin", "pass", "yoav@gmail.com")


    def test_addAdmin_selfAddToAdmin_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.addAdmin("Ari", "Ari", "pass", "yoav@gmail.com")
    
    # addAuction
    def test_addAuction_success(self):
        pass

    def test_addAuction_userNotLoggedIn_fail(self):
        pass

    def test_addAuction_storeNotExists_fail(self):
        pass

    def test_addAuction_userWithoutPermission_fail(self):
        pass

    def test_addAuction_productNotExists_fail(self):
        pass

    def test_addAuction_startingPriceLessEqualZero_fail(self):
        pass

    def test_addAuction_durationLessEqualZero_fail(self):
        pass

    def test_addAuction_productAlreadyInAuction_fail(self):
        pass

    # addDiscount
    def test_addDiscount_success(self):
        pass

    def test_addDiscount_userNotLoggedIn_fail(self):
        pass

    def test_addDiscount_storeNotExists_fail(self):
        pass

    def test_addDiscount_userWithoutPermission_fail(self):
        pass

    def test_addDiscount_productNotExists_fail(self):
        pass

    def test_addDiscount_productAlreadyInDiscount_fail(self):
        #TODO: check if this is legal - should it fail or success?
        pass

    def test_addDiscount_invalidDiscountType_fail(self):
        pass

    def test_addDiscount_invalidDiscountPercentage_fail(self):
        pass

    # addLottery
    def test_addLottery_success(self):
        pass

    def test_addLottery_userNotLoggedIn_fail(self):
        pass

    def test_addLottery_storeNotExists_fail(self):
        pass

    def test_addLottery_userWithoutPermission_fail(self):
        pass

    def test_addLottery_productNotExists_fail(self):
        pass

    def test_addLottery_productAlreadyInLottery_fail(self):
        pass

    # addNewProductToStore
    def test_addNewProductToStore_success(self):
        #before
        self.store_facade.logInAsMember("Feliks", "password456")
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        #after
        self.store_facade.addNewProductToStore("Feliks", "AriExpress", "shoes", 10, 500, "shoes")
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 2)
        new_product: Product = self.my_store.getProductById(2, "Feliks")
        self.assertTrue(new_product.get_name() == "shoes")
        

    def test_addNewProductToStore_userNotLoggedIn_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        with self.assertRaises(Exception):
            self.store_facade.addNewProductToStore("Feliks", "AriExpress", "shoes", 10, 500, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    def test_addNewProductToStore_storeNotExists_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        with self.assertRaises(Exception):
            self.store_facade.addNewProductToStore("Feliks", "Some_Store", "shoes", 10, 500, "shoes")


    def test_addNewProductToStore_userWithoutPermission_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            # Amiel is trying to add a product to a store he doesn't own or manage
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", 10, 500, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    def test_addNewProductToStore_invalidPrice_0_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # Amiel is trying to add a product to a store he doesn't own or manage
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", 10, 0, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    def test_addNewProductToStore_invalidPrice_negativePrice_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # Amiel is trying to add a product to a store he doesn't own or manage
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", 10, -1, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
    def test_addNewProductToStore_invalidQuantity_0_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # zero price
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", 0, 500, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    def test_addNewProductToStore_invalidQuantity_negativeQuantity_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # negative price
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", -1, 500, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)


    def test_addNewProductToStore_invalidCategory_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # empty category
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "shoes", -1, 500, "")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    def test_addNewProductToStore_invalidName_fail(self):
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            # empty name
            self.store_facade.addNewProductToStore("Amiel", "AriExpress", "", -1, 500, "shoes")
        # checks if the store products list hasn't changed
        self.assertTrue(len(self.my_store.getProducts("Feliks").values()) == 1)

    # addPermissions
    def test_nominateOwner_success(self):
        member_to_nominate: Member = self.store_facade.members.get("Amiel")
        # before
        self.assertTrue(not member_to_nominate.accesses.keys().__contains__("AriExpress"))
        # after
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.nominateStoreOwner("Feliks", "Amiel", "AriExpress")
        self.assertTrue(member_to_nominate.accesses.keys().__contains__("AriExpress"))
        access: Access = member_to_nominate.get_accesses().get("AriExpress")
        self.assertTrue(access.get_nominated_by_username() == "Feliks")
        self.assertTrue(self.my_store.get_accesses().keys().__contains__("Amiel"))
        self.assertTrue(access.hasRole("Owner"))

    def test_nominateManager_success(self):
        member_to_nominate: Member = self.store_facade.members.get("Amiel")
        # before
        self.assertTrue(not member_to_nominate.accesses.keys().__contains__("AriExpress"))
        # after
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.nominateStoreManager("Feliks", "Amiel", "AriExpress")
        self.assertTrue(member_to_nominate.accesses.keys().__contains__("AriExpress"))
        access: Access = member_to_nominate.get_accesses().get("AriExpress")
        self.assertTrue(access.get_nominated_by_username() == "Feliks")
        self.assertTrue(self.my_store.get_accesses().keys().__contains__("Amiel"))
        self.assertTrue(access.hasRole("Manager"))

    def test_nominate_nomineeNotExists_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            self.store_facade.nominateStoreOwner("Feliks", "some_random_guy", "AriExpress")
        self.assertFalse(len(self.my_store.get_accesses().values()) == 2)
        self.assertTrue(len(self.my_store.get_accesses().values()) == 1)



    def test_nominate_storeNotExists_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            self.store_facade.nominateStoreOwner("Feliks", "Amiel", "some_store")
        self.assertFalse(self.store_facade.stores.keys().__contains__("some_store"))

    def test_nominate_userWithoutPermission_Ownertry_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.nominateStoreOwner("Amiel","YuvalMelamed","AriExpress")
        self.assertFalse(len(self.my_store.get_accesses().values()) == 2)
        self.assertTrue(len(self.my_store.get_accesses().values()) == 1)
        yuval: Member = self.store_facade.members.get("YuvalMelamed")
        self.assertFalse(yuval.get_accesses().keys().__contains__("AriExpress"))

    def test_nominate_userWithoutPermission_Managertry_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.nominateStoreManager("Amiel","YuvalMelamed","AriExpress")
        self.assertFalse(len(self.my_store.get_accesses().values()) == 2)
        self.assertTrue(len(self.my_store.get_accesses().values()) == 1)
        yuval: Member = self.store_facade.members.get("YuvalMelamed")
        self.assertFalse(yuval.get_accesses().keys().__contains__("AriExpress"))

    def test_nominate_nomineeAlreadyHasBeenNominated_fail(self):
        member_to_nominate: Member = self.store_facade.members.get("Amiel")
        # before
        self.assertTrue(not member_to_nominate.accesses.keys().__contains__("AriExpress"))
        # after
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.nominateStoreOwner("Feliks", "Amiel", "AriExpress")
        with self.assertRaises(Exception):
            self.store_facade.nominateStoreOwner("Feliks", "Amiel", "AriExpress")
        self.assertTrue(member_to_nominate.accesses.keys().__contains__("AriExpress"))
        access: Access = member_to_nominate.get_accesses().get("AriExpress")
        self.assertTrue(access.get_nominated_by_username() == "Feliks")
        self.assertTrue(self.my_store.get_accesses().keys().__contains__("Amiel"))
        self.assertTrue(access.hasRole("Owner"))

    # addPurchasePolicy
    def test_addPurchasePolicy_success(self):
        pass

    def test_addPurchasePolicy_userNotLoggedIn_fail(self):
        pass

    def test_addPurchasePolicy_storeNotExists_fail(self):
        pass

    def test_addPurchasePolicy_userWithoutPermission_fail(self):
        pass

    def test_addPurchasePolicy_invalidPolicy_fail(self):
        pass

    # addToBasket
    def test_addToBasket_success(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertTrue(amiel.cart.baskets.keys().__contains__("AriExpress"))
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        self.assertTrue(len(basket.products.values()) == 1)
        self.assertTrue(basket.products.keys().__contains__(1))
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[0] == self.item_paper)
        self.assertTrue(product_tuple[1] == 5)
        self.assertTrue(product_tuple[2] == 500)

    def test_addToBasket_fromMultipleStores_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.createStore("Feliks", "FeliksExpress")
        my_store2: Store = self.store_facade.stores.get("FeliksExpress")
        self.store_facade.addNewProductToStore("Feliks", "FeliksExpress", "shoes", 10, 500, "shoes")
        item_shoes: Product = my_store2.getProductById(1, "Feliks")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        self.store_facade.addToBasket("Amiel", "FeliksExpress", 1, 5)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertTrue(amiel.cart.baskets.keys().__contains__("AriExpress"))
        self.assertTrue(amiel.cart.baskets.keys().__contains__("FeliksExpress"))
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        basket2: Basket = amiel.cart.baskets.get("FeliksExpress")
        self.assertTrue(basket.products.keys().__contains__(1))
        self.assertTrue(basket2.products.keys().__contains__(1))
        product_tuple: tuple = basket.products.get(1)
        product_tuple2: tuple = basket2.products.get(1)
        self.assertTrue(product_tuple[0] == self.item_paper)
        self.assertTrue(product_tuple[1] == 5)
        self.assertTrue(product_tuple[2] == 500)
        self.assertTrue(product_tuple2[0] == item_shoes)
        self.assertTrue(product_tuple2[1] == 5)
        self.assertTrue(product_tuple2[2] == 500)
    def test_addToBasket_userNotLoggedIn_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertFalse(amiel.cart.baskets.keys().__contains__("AriExpress"))


    def test_addToBasket_storeNotExists_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("Amiel", "some_store", 1, 5)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertFalse(amiel.cart.baskets.keys().__contains__("some_store"))

    def test_addToBasket_productNotExists_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("Amiel", "AriExpress", 2, 5)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertFalse(amiel.cart.baskets.keys().__contains__("AriExpress"))

    def test_addToBasket_invalidQuantity_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("Amiel", "AriExpress", 1, -1)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertFalse(amiel.cart.baskets.keys().__contains__("AriExpress"))


    def test_addToBasket_productNotInStock_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.addToBasket("Amiel", "AriExpress", 1, 11)
        amiel: Member = self.store_facade.members.get("Amiel")
        self.assertFalse(amiel.cart.baskets.keys().__contains__("AriExpress"))

    # approveBid
    #TODO: BIDS
    def test_approveBid_success(self):
        pass

    def test_approveBid_userNotLoggedIn_fail(self):
        pass

    def test_approveBid_storeNotExists_fail(self):
        pass

    def test_approveBid_userWithoutPermission_fail(self):
        pass

    def test_approveBid_bidNotExists_fail(self):
        pass


    # ClaimAuctionPurchase
    def test_ClaimAuctionPurchase_success(self):
        pass

    def test_ClaimAuctionPurchase_userNotLoggedIn_fail(self):
        pass

    def test_ClaimAuctionPurchase_storeNotExists_fail(self):
        pass

    def test_ClaimAuctionPurchase_userWithoutPermission_fail(self):
        #TODO: should there be permissions? - should it fail or success?
        pass

    def test_ClaimAuctionPurchase_auctionNotExists_fail(self):
        pass

    def test_ClaimAuctionPurchase_auctionNotEnded_fail(self):
        pass

    def test_ClaimAuctionPurchase_auctionAlreadyClaimed_fail(self):
        pass

    # closeStore
    def test_closeStore_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.closeStore("Feliks", "AriExpress")
        self.assertFalse(self.my_store.active)


    def test_closeStore_userNotLoggedIn_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Feliks", "AriExpress")
            #check if store is still active
        self.assertTrue(self.my_store.active)

    def test_closeStore_storeNotExists_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Feliks", "some_store")
            # check if store is still active
        self.assertTrue(self.my_store.active)

    def test_closeStore_userWithoutAccessToStore_fail(self):
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Amiel", "some_store")
            # check if store is still active
        self.assertTrue(self.my_store.active)

    def test_closeStore_userWithAccessToStoreAsOwner_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.nominateStoreOwner("Feliks", "Amiel", "AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Amiel", "some_store")
            # check if store is still active
        self.assertTrue(self.my_store.active)
    def test_closeStore_userWithAccessToStoreAsManager_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.nominateStoreManager("Feliks", "Amiel", "AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Amiel", "some_store")
            # check if store is still active
        self.assertTrue(self.my_store.active)


    def test_closeStore_storeAlreadyClosed_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.closeStore("Feliks", "AriExpress")
        with self.assertRaises(Exception):
            self.store_facade.closeStore("Feliks", "AriExpress")
            # check if store is still active
        self.assertFalse(self.my_store.active)

    # closeStoreAsAdmin
    def test_closeStoreAsAdmin_success(self):
        self.store_facade.logInAsAdmin("Ari", "password123")
        self.store_facade.closeStoreAsAdmin("Ari", "AriExpress")
        self.assertTrue(self.my_store.closed_by_admin)
        self.assertFalse(self.my_store.active)


    def test_closeStoreAsAdmin_userNotLoggedIn_fail(self):
        with self.assertRaises(Exception):
            self.store_facade.closeStoreAsAdmin("Ari", "AriExpress")
        self.assertFalse(self.my_store.closed_by_admin)
        self.assertTrue(self.my_store.active)

    def test_closeStoreAsAdmin_storeNotExists_fail(self):
        self.store_facade.logInAsAdmin("Ari", "password123")
        with self.assertRaises(Exception):
            self.store_facade.closeStoreAsAdmin("Ari", "some_store")
        self.assertFalse(self.my_store.closed_by_admin)
        self.assertTrue(self.my_store.active)

    def test_closeStoreAsAdmin_userNotAdmin_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            self.store_facade.closeStoreAsAdmin("Feliks", "AriExpress")
        self.assertFalse(self.my_store.closed_by_admin)
        self.assertTrue(self.my_store.active)

    def test_closeStoreAsAdmin_storeAlreadyClosed_fail(self):
        self.store_facade.logInAsAdmin("Ari", "password123")
        self.store_facade.closeStoreAsAdmin("Ari", "AriExpress")
        with self.assertRaises(Exception):
            self.store_facade.closeStoreAsAdmin("Ari", "AriExpress")
        self.assertTrue(self.my_store.closed_by_admin)
        self.assertFalse(self.my_store.active)

    # editBasketQuantity
    def test_editBasketQuantity_member_success(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        self.store_facade.editBasketQuantity("Amiel", "AriExpress", 1, 8)
        product_tuple2: tuple = basket.products.get(1)
        self.assertTrue(product_tuple2[1] == 8)



    def test_editBasketQuantity_guest_success(self):
        guest: Guest = self.store_facade.onlineGuests.get("0")
        self.store_facade.addToBasket("0", "AriExpress", 1, 5)
        basket: Basket = guest.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        self.store_facade.editBasketQuantity("0", "AriExpress", 1, 8)
        product_tuple2: tuple = basket.products.get(1)
        self.assertTrue(product_tuple2[1] == 8)

    def test_editBasketQuantity_userNotLoggedIn_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        self.store_facade.logOut("Amiel")
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("Amiel", "AriExpress", 1, 8)
        product_tuple2: tuple = basket.products.get(1)
        self.assertFalse(product_tuple2[1] == 8)
        self.assertTrue(product_tuple2[1] == 5)

    def test_editBasketQuantity_storeNotExists_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("Amiel", "some_store", 1, 8)
        product_tuple2: tuple = basket.products.get(1)
        self.assertFalse(product_tuple2[1] == 8)
        self.assertTrue(product_tuple2[1] == 5)

    def test_editBasketQuantity_productNotExists_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("Amiel", "AriExpress", 2, 8)
        product_tuple2: tuple = basket.products.get(1)
        self.assertFalse(product_tuple2[1] == 8)
        self.assertTrue(product_tuple2[1] == 5)

    def test_editBasketQuantity_invalidQuantity_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_tuple: tuple = basket.products.get(1)
        self.assertTrue(product_tuple[1] == 5)
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("Amiel", "AriExpress", 1, -5)
        product_tuple2: tuple = basket.products.get(1)
        self.assertFalse(product_tuple2[1] == 8)
        self.assertTrue(product_tuple2[1] == 5)

    def test_editBasketQuantity_productNotInBasket_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.editBasketQuantity("Amiel", "AriExpress", 1, 8)
        self.assertTrue(not amiel.cart.baskets.keys().__contains__("AriExpress"))

    # editProductOfStore
    def test_editProductOfStore_changeQuantityAndPrice_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        # before
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)
        self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, quantity = 4 , price = 25)
        # after
        self.assertTrue(product.quantity == 4)
        self.assertTrue(product.price == 25)

    def test_editProductOfStore_userNotLoggedIn_fail(self):
        product: Product = self.my_store.getProductById(1, "Feliks")
        # before
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, quantity=4, price=25)
        # after
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)

    def test_editProductOfStore_storeNotExists_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "some_store", 1, quantity=4, price=25)
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)

    def test_editProductOfStore_userWithoutPermission_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.logInAsMember("Amiel", "password789")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Amiel", "AriExpress", 1, quantity=4, price=25)
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)

    def test_editProductOfStore_productNotExists_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 2, quantity=4, price=25)
        self.assertTrue(product.quantity == 10)
        self.assertTrue(product.price == 500)

    def test_editProductOfStore_invalidQuantity_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.quantity == 10)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, quantity=-4)
        self.assertTrue(product.quantity == 10)



    def test_editProductOfStore_invalidPrice_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.price == 500)
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, price=-5)
        self.assertTrue(product.price == 500)

    def test_editProductOfStore_invalidCategory_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.name == "paper")
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, category="")
        self.assertTrue(product.name == "paper")

    def test_editProductOfStore_invalidName_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.name == "paper")
        with self.assertRaises(Exception):
            self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, name="")
        self.assertTrue(product.name == "paper")

    def test_editProductOfStore_productInSomeBasket_success(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Feliks", "password456")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        basket: Basket = amiel.cart.baskets.get("AriExpress")
        product_in_basket: Product = basket.products.get(1)[0]
        product: Product = self.my_store.getProductById(1, "Feliks")
        self.assertTrue(product.price == 500)
        self.store_facade.editProductOfStore("Feliks", "AriExpress", 1, price=1000)
        self.assertTrue(product.price == 1000)
        self.assertTrue(product_in_basket.price == 1000)

    # getAllBidsFromUser TODO:BIDS
    def test_getAllBidsFromUser_success(self):
        pass

    def test_getAllBidsFromUser_userNotLoggedIn_fail(self):
        pass

    # getAllOfflineMembers
    def test_getAllOfflineMembers_success(self):
        self.store_facade.logInAsAdmin("Ari", "password123")
        offline_members = self.store_facade.getAllOfflineMembers("Ari")
        self.assertTrue(len(offline_members) == 3)
        self.store_facade.logInAsMember("Feliks", "password456")
        offline_members = self.store_facade.getAllOfflineMembers("Ari")
        self.assertTrue(len(offline_members) == 2)
        self.store_facade.logInAsMember("Amiel", "password789")
        offline_members = self.store_facade.getAllOfflineMembers("Ari")
        self.assertTrue(len(offline_members) == 1)
        self.store_facade.logInAsMember("YuvalMelamed", "PussyDestroyer69")
        offline_members = self.store_facade.getAllOfflineMembers("Ari")
        self.assertTrue(len(offline_members) == 0)
        self.store_facade.logOut("Amiel")
        offline_members = self.store_facade.getAllOfflineMembers("Ari")
        self.assertTrue(len(offline_members) == 1)


    def test_getAllOfflineMembers_userNotLoggedIn_fail(self):
        with self.assertRaises(Exception):
            offline_members = self.store_facade.getAllOfflineMembers("Ari")


    def test_getAllOfflineMembers_userNotAdmin_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            offline_members = self.store_facade.getAllOfflineMembers("Feliks")


    # getAllOnlineMembers
    def test_getAllOnlineMembers_success(self):
        self.store_facade.logInAsAdmin("Ari", "password123")
        online_members = self.store_facade.getAllOnlineMembers("Ari")
        self.assertTrue(len(online_members) == 0)
        self.store_facade.logInAsMember("Feliks", "password456")
        online_members = self.store_facade.getAllOnlineMembers("Ari")
        self.assertTrue(len(online_members) == 1)
        self.store_facade.logInAsMember("Amiel", "password789")
        online_members = self.store_facade.getAllOnlineMembers("Ari")
        self.assertTrue(len(online_members) == 2)
        self.store_facade.logInAsMember("YuvalMelamed", "PussyDestroyer69")
        online_members = self.store_facade.getAllOnlineMembers("Ari")
        self.assertTrue(len(online_members) == 3)
        self.store_facade.logOut("YuvalMelamed")
        online_members = self.store_facade.getAllOnlineMembers("Ari")
        self.assertTrue(len(online_members) == 2)

    def test_getAllOnlineMembers_userNotLoggedIn_fail(self):
        with self.assertRaises(Exception):
            online_members = self.store_facade.getAllOnlineMembers("Ari")

    def test_getAllOnlineMembers_userNotAdmin_fail(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        with self.assertRaises(Exception):
            online_members = self.store_facade.getAllOnlineMembers("Feliks")

    # getBasket
    def test_getBasket_member_success(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        self.assertTrue(amiel.cart.baskets.keys().__contains__(self.my_store.get_store_name()))
        basket: Basket = self.store_facade.getBasket("Amiel", self.my_store.get_store_name())
        self.assertTrue(basket.username == amiel.get_username())
        self.assertTrue(basket.store == self.my_store)

    def test_getBasket_guest_success(self):
        guest: Guest = self.store_facade.getUserOrMember(0)
        self.store_facade.addToBasket("0", "AriExpress", 1, 5)
        self.assertTrue(guest.cart.baskets.keys().__contains__(self.my_store.get_store_name()))
        basket: Basket = self.store_facade.getBasket("0", self.my_store.get_store_name())
        self.assertTrue(basket.username == "0")
        self.assertTrue(basket.store == self.my_store)

    def test_getBasket_userNotLoggedIn_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        self.store_facade.logOut("Amiel")
        self.assertTrue(amiel.cart.baskets.keys().__contains__(self.my_store.get_store_name()))
        with self.assertRaises(Exception):
            basket: Basket = self.store_facade.getBasket("Amiel", self.my_store.get_store_name())

    def test_getBasket_storeNotExists_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress", 1, 5)
        self.assertTrue(amiel.cart.baskets.keys().__contains__(self.my_store.get_store_name()))
        with self.assertRaises(Exception):
            basket: Basket = self.store_facade.getBasket("Amiel", "some_store")

    def test_getBasket_basketNotExists_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.assertFalse(amiel.cart.baskets.keys().__contains__(self.my_store.get_store_name()))
        with self.assertRaises(Exception):
            basket: Basket = self.store_facade.getBasket("Amiel", "some_store")

    # getCart
    def test_getCart_member_success(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        cart: Cart = self.store_facade.getCart("Amiel")
        self.assertTrue(cart.username == "Amiel")
    def test_getCart_guest_success(self):
        guest: Guest = self.store_facade.getUserOrMember(0)
        cart: Cart = self.store_facade.getCart(0)
        self.assertTrue(cart.username == "0")
        self.assertTrue(len(cart.baskets.keys()) == 0)

    def test_getCart_userNotLoggedIn_fail(self):
        amiel: Member = self.store_facade.members.get("Amiel")
        with self.assertRaises(Exception):
            cart: Cart = self.store_facade.getCart("Amiel")

    # getDiscount
    #TODO: Discounts

    def test_addDiscount_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        feliks :Member = self.store_facade.members.get("Feliks")
        access: Access = feliks.accesses.get("AriExpress")
        oreo: Product = self.my_store.addProduct(access, "Oreo", 10, 10, "Milk")
        discount = self.my_store.addDiscount("Feliks", "Simple", percent=10, level="Product", level_name=oreo.get_product_id())
        added_discount = self.my_store.getDiscount(1)
        self.assertEqual(discount, added_discount)


    def test_calculateSimpleDiscount_success(self):
        self.store_facade.logInAsMember("Ari", "password123")
        self.store_facade.createStore(self.member1.get_username(), "Store1")
        self.store = self.store_facade.stores["Store1"]
        self.access = self.store.get_accesses()[self.member1.get_username()]
        self.product = self.store.addProduct(self.access, "Oreo", 10, 10, "Milk")
        self.discount = self.store.addDiscount("Simple", percent=10, level="Product",
                                               level_name=self.product.get_product_id())
        self.product_dict = {self.product.get_product_id(): 1}
        self.price_after_discount = self.store.getProductPriceAfterDiscount(self.product, self.product_dict, 0)
        self.assertEqual(self.price_after_discount, 9)

    def test_calculateConditionedDiscount_byCategory_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")
        feliks: Member = self.store_facade.members.get("Feliks")
        access: Access = feliks.accesses.get("AriExpress")
        oreo: Product = self.my_store.addProduct(access, "Oreo", 10, 10, "Milk")
        cariot: Product = self.my_store.addProduct(access, "Cariot", 10, 10, "Milk")
        sub_rule = {"rule_type": "amount_of_product", "product_id": oreo.get_product_id(),
                        "operator":">=", "quantity": 1,"category": "", "child": {}}
        rule = {"rule_type": "amount_of_product", "product_id": cariot.get_product_id(),
                     "operator": ">=", "quantity": 1,"category": "", "child": {"logic_type": "OR", "rule": sub_rule}}
        discount = self.my_store.addDiscount("Feliks", "Conditioned", percent=10, level="Product",
                                               level_name=self.item_paper.get_product_id(), rule=rule)
        product_dict = {cariot.get_product_id(): 2, oreo.get_product_id(): 2}
        price_after_discount_1 = self.my_store.getProductPriceAfterDiscount(self.item_paper, product_dict, 0)
        self.assertEqual(450, price_after_discount_1)

    def test_getDiscount_storeNotExists_fail(self):
            pass

    def test_getDiscount_discountNotExists_fail(self):
            pass

    # purchaseCart

    def test_purchaseCart_oneSuccessOneFail_notEnoughSupply(self):
        transaction_history = TransactionHistory()
        # before
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToUser("YuvalMelamed")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.assertTrue(len(transaction_history.user_transactions.get("Amiel")) == 0)
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.logInAsMember("YuvalMelamed", "PussyDestroyer69")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 9)
        self.store_facade.addToBasket("YuvalMelamed", "AriExpress",
                                      1, 9)
        self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                       "some_address")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("YuvalMelamed", "4580202046783956", "YuvalMelamed", "008234235", "12/11",
                                           "554H",
                                           "some_address")
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        yuval_transaction_list: list = transaction_history.get_User_Transactions("YuvalMelamed")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 1)
        self.assertTrue(len(ariExpress_transaction_list) == 1)
        # integrity that the transaction failed for Yuval
        self.assertTrue(len(yuval_transaction_list) == 0)
        transaction_history.clearAllHistory()

    def test_purchaseCart_userNotLoggedIn_fail(self):
        transaction_history = TransactionHistory()
        self.store_facade.logInAsMember("Amiel", "password789")
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 3)

        self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                       "some_address")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 3)
        self.store_facade.logOut("Amiel")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                           "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 1)
        self.assertTrue(len(ariExpress_transaction_list) == 1)
        transaction_history.clearAllHistory()

    def test_purchaseCart_cartWithoutBaskets_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                           "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 0)
        self.assertTrue(len(ariExpress_transaction_list) == 0)
        transaction_history.clearAllHistory()
    def test_purchaseCart_cardNumberInvalid_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 3)
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "020345672", "Amiel saad", "123456789", "12/26", "555",
                                           "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 0)
        self.assertTrue(len(ariExpress_transaction_list) == 0)
        transaction_history.clearAllHistory()

    def test_purchaseCart_cardDateInvalid_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 3)
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "/26", "555",
                                           "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 0)
        self.assertTrue(len(ariExpress_transaction_list) == 0)
        transaction_history.clearAllHistory()



    def test_purchaseCart_cardCcvInvalid_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 3)
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "55",
                                           "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 0)
        self.assertTrue(len(ariExpress_transaction_list) == 0)
        transaction_history.clearAllHistory()



    def test_purchaseCart_productInBasketOutOfStock_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        transaction_history.insertEmptyListToStore("AriExpress")
        self.store_facade.logInAsMember("Amiel", "password789")
        #guest adding to his cart and purchasing
        self.store_facade.addToBasket(0, "AriExpress",
                                      1, 10)
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 2)
        self.store_facade.purchaseCart(0, "4580020345672134", "some guy", "123456789", "12/26", "555",
                                           "some_address")
        # there isn't enough in stock
        with self.assertRaises(Exception):
            self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                       "some_address")
            # integrity that the transaction failed for Amiel
        amiel_transaction_list: list = transaction_history.get_User_Transactions("Amiel")
        ariExpress_transaction_list: list = transaction_history.get_Store_Transactions("AriExpress")
        # transaction did not go through!
        self.assertTrue(len(amiel_transaction_list) == 0)
        # the guest bought so there is a transaction in the store
        self.assertTrue(len(ariExpress_transaction_list) == 1)
        transaction_history.clearAllHistory()

    # getMemberPurchaseHistory
    def test_getMemberPurchaseHistory_member_success(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        amiel_list: list = self.store_facade.getMemberPurchaseHistory("Amiel","Amiel")
        # no transactions yet!
        self.assertTrue(len(amiel_list) == 0)
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 2)
        self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                       "some_address")
        # the list should be updated to 1 there is a transaction!
        self.assertTrue(len(amiel_list) == 1)
    def test_getMemberPurchaseHistory_calledByAdmin_success(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        self.store_facade.logInAsMember("Amiel", "password789")
        self.store_facade.logInAsAdmin("Ari", "password123")
        amiel_list: list = self.store_facade.getMemberPurchaseHistory("Ari", "Amiel")
        # no transactions yet!
        self.assertTrue(len(amiel_list) == 0)
        self.store_facade.addToBasket("Amiel", "AriExpress",
                                      1, 2)
        self.store_facade.purchaseCart("Amiel", "4580020345672134", "Amiel saad", "123456789", "12/26", "555",
                                       "some_address")
        # the list should be updated to 1 there is a transaction!
        self.assertTrue(len(amiel_list) == 1)


    def test_getMemberPurchaseHistory_userNotLoggedIn_fail(self):
        transaction_history = TransactionHistory()
        transaction_history.insertEmptyListToUser("Amiel")
        with self.assertRaises(Exception):
            amiel_list: list = self.store_facade.getMemberPurchaseHistory("Amiel", "Amiel")




    def test_getMemberPurchaseHistory_userNotMember_fail(self):
        transaction_history = TransactionHistory()
        with self.assertRaises(Exception):
            amiel_list: list = self.store_facade.getMemberPurchaseHistory("some_guy", "some_guy")

    # getPermissions
    def test_getPermissions_success(self):
        self.store_facade.logInAsMember("Feliks", "password456")

        self.store_facade.getPermissions()

    def test_getPermissions_userNotLoggedIn_fail(self):
        pass

    def test_getPermissions_storeNotExists_fail(self):
        pass

    def test_getPermissions_storeIsClosed_fail(self):
        pass

    def test_getPermissions_userNotOwner_fail(self):
        pass

    def test_getPermissions_nominatedNotExists_fail(self):
        pass

    def test_getPermissions_nominatedHasNoPermissions_fail(self):
        # TODO: change to success?
        pass

    # getProduct
    def test_getProduct_success(self):
        pass

    def test_getProduct_userNotLoggedIn_fail(self):
        pass

    def test_getProduct_storeNotExists_fail(self):
        pass

    def test_getProduct_productNotExists_fail(self):
        pass

    def test_getProduct_storeIsClosed_fail(self):
        pass

    def test_getProduct_productNotInStore_fail(self):
        pass

    # getProductsByStore
    def test_getProductsByStore_success(self):
        pass

    def test_getProductsByStore_userNotLoggedIn_fail(self):
        pass

    def test_getProductsByStore_storeNotExists_fail(self):
        pass

    def test_getProductsByStore_storeIsClosed_fail(self):
        pass

    # getPurchasePolicy
    def test_getPurchasePolicy_success(self):
        pass

    def test_getPurchasePolicy_userNotLoggedIn_fail(self):
        # TODO: should it be success?
        pass

    def test_getPurchasePolicy_storeNotExists_fail(self):
        pass

    def test_getPurchasePolicy_policyNotExists_fail(self):
        pass

    def test_getPurchasePolicy_storeIsClosed_fail(self):
        pass

    # getStaffInfo
    def test_getStaffInfo_success(self):
        pass

    def test_getStaffInfo_userNotLoggedIn_fail(self):
        pass

    def test_getStaffInfo_storeNotExists_fail(self):
        pass  

    def test_getStaffInfo_storeIsClosed_fail(self):
        pass  

    # getStoreManagerPermissions
    def test_getStoreManagerPermissions_success(self):
        pass

    # getStorePurchaseHistory
    def test_getStorePurchaseHistory_success(self):
        pass

    def test_getStorePurchaseHistory_userNotLoggedIn_fail(self):
        pass

    def test_getStorePurchaseHistory_storeNotExists_fail(self):
        pass

    def test_getStorePurchaseHistory_storeIsClosed_fail(self):
        pass

    # getStores
    def test_getStores_success(self):
        pass

    # getStoresJson
    def test_getStoresJson_success(self):
        pass

    # leaveAsGuest
    def test_leaveAsGuest_guest_success(self):
        pass

    def test_leaveAsGuest_member_fail(self):
        pass

    def test_leaveAsGuest_guestNotLoggedIn_fail(self):
        pass

    # loadData

    # logInAsAdmin
    def test_logInAsAdmin_success(self):
        pass

    def test_logInAsAdmin_userNotExists_fail(self):
        pass

    def test_logInAsAdmin_userNotAdmin_fail(self):
        pass

    def test_logInAsAdmin_wrongPassword_fail(self):
        pass

    def test_logInAsAdmin_adminAlreadyLoggedIn_fail(self):
        pass

    # loginAsGuest
    def test_loginAsGuest_success(self):
        pass

    def test_loginAsGuest_userAlreadyLoggedIn_fail(self):
        pass

    # logInAsMember
    def test_logInAsMember_success(self):
        pass

    def test_logInAsMember_userNotExists_fail(self):
        pass

    def test_logInAsMember_wrongPassword_fail(self):
        pass

    def test_logInAsMember_memberAlreadyLoggedIn_fail(self):
        pass

    # logInFromGuestToMember
    def test_logInFromGuestToMember_success(self):
        self.store_facade.logInFromGuestToMember(0 , "Feliks", "password456")

    def test_logInFromGuestToMember_userNotExists_fail(self):
        pass

    def test_logInFromGuestToMember_wrongPassword_fail(self):
        pass

    def test_logInFromGuestToMember_memberAlreadyLoggedIn_fail(self):
        pass

    def test_logInFromGuestToMember_notLoggedAsGuest_fail(self):
        pass

    def test_logInFromGuestToMember_checkIfCartIsSaved_success(self):
        pass

    # logOut
    def test_logOut_success(self):
        pass

    def test_logOut_userNotLoggedIn_fail(self):
        pass

    def test_logOut_guestIsLoggedIn_fail(self):
        # TODO: should it be success?
        pass

    # logOutAsAdmin
    def test_logOutAsAdmin_success(self):
        pass

    def test_logOutAsAdmin_userLoggedInNotAdmin_fail(self):
        pass

    def test_logOutAsAdmin_userNotLoggedIn_fail(self):
        pass

    # messageAsAdmin
    def test_messageAsAdmin_success(self):
        pass

    def test_messageAsAdmin_userNotLoggedIn_fail(self):
        pass

    def test_messageAsAdmin_userNotAdmin_fail(self):
        pass

    def test_messageAsAdmin_receiverNotExist_fail(self):
        pass

    def test_messageAsAdmin_messageIsInvalid_fail(self):
        pass

    # nominateStoreManager
    def test_nominateStoreManager_success(self):
        pass

    def test_nominateStoreManager_userNotLoggedIn_fail(self):
        pass

    def test_nominateStoreManager_storeNotExists_fail(self):
        pass

    def test_nominateStoreManager_userNotExists_fail(self):
        pass

    def test_nominateStoreManager_nominatedAlreadyManager_fail(self):
        pass

    def test_nominateStoreManager_nominatedAlreadyOwner_fail(self):
        pass

    def test_nominateStoreManager_userHasNoPermissions_fail(self):
        pass

    # nominateStoreOwner
    def test_nominateStoreOwner_success(self):
        pass

    def test_nominateStoreOwner_userNotLoggedIn_fail(self):
        pass

    def test_nominateStoreOwner_storeNotExists_fail(self):
        pass

    def test_nominateStoreOwner_userNotExists_fail(self):
        pass

    def test_nominateStoreOwner_nominatedAlreadyManager_fail(self):
        # TODO: should it be success?
        pass

    def test_nominateStoreOwner_nominatedAlreadyOwner_fail(self):
        pass

    def test_nominateStoreOwner_userHasNoPermissions_fail(self):
        pass

    # openStore
    def test_openStore_success(self):
        pass

    def test_openStore_userNotLoggedIn_fail(self):
        pass

    def test_openStore_storeAlreadyExists_fail(self):
        pass

    def test_openStore_storeNameIsEmpty_fail(self):
        pass

    # participateInLottery
    def test_participateInLottery_success(self):
        pass

    def test_participateInLottery_userNotLoggedIn_fail(self):
        pass

    def test_participateInLottery_storeNotExists_fail(self):
        pass

    def test_participateInLottery_storeIsClosed_fail(self):
        pass

    def test_participateInLottery_userAlreadyParticipated_fail(self):
        pass

    def test_participateInLottery_lotteryNotExists_fail(self):
        pass

    def test_participateInLottery_lotteryIsClosed_fail(self):
        pass

    # placeBid
    def test_placeBid_success(self):
        pass

    def test_placeBid_guestLoggedIn_fail(self):
        pass

    def test_placeBid_userNotLoggedIn_fail(self):
        pass

    def test_placeBid_storeNotExists_fail(self):
        pass

    def test_placeBid_storeIsClosed_fail(self):
        pass

    def test_placeBid_productNotExists_fail(self):
        pass

    def test_placeBid_productIsNotOnSale_fail(self):
        pass

    def test_placeBid_offerTooLow_fail(self):
        pass

    def test_placeBid_quantityInvalid_fail(self):
        pass

    def test_placeBid_userAlreadyPlacedBid_fail(self):
        pass

    # placeOfferInAuction
    def test_placeOfferInAuction_success(self):
        pass

    def test_placeOfferInAuction_guestLoggedIn_fail(self):
        # TODO: should it be success? can guest do it?
        pass

    def test_placeOfferInAuction_userNotLoggedIn_fail(self):
        pass

    def test_placeOfferInAuction_storeNotExists_fail(self):
        pass

    def test_placeOfferInAuction_storeIsClosed_fail(self):
        pass

    def test_placeOfferInAuction_auctionNotExists_fail(self):
        pass

    def test_placeOfferInAuction_auctionIsClosed_fail(self):
        pass

    def test_placeOfferInAuction_offerTooLow_fail(self):
        pass

    # productFilterByFeatures
    def test_productFilterByFeatures_success(self):
        pass

    def test_productFilterByFeatures_userNotLoggedIn_fail(self):
        # TODO: should it be success?
        pass

    def test_productFilterByFeatures_featureNotExists_fail(self):
        pass

    def test_productFilterByFeatures_featureIsEmpty_fail(self):
        pass

    # productSearchByCategory
    def test_productSearchByCategory_success(self):
        pass

    def test_productSearchByCategory_userNotLoggedIn_fail(self):
        # TODO: should it be success?
        pass

    def test_productSearchByCategory_categoryNotExists_fail(self):
        pass

    def test_productSearchByCategory_categoryIsEmpty_fail(self):
        pass

    # productSearchByName
    def test_productSearchByName_success(self):
        pass

    def test_productSearchByName_userNotLoggedIn_fail(self):
        # TODO: should it be success?
        pass

    def test_productSearchByName_categoryNotExists_fail(self):
        pass

    def test_productSearchByName_categoryIsEmpty_fail(self):
        pass

    # purchaseCart
    # Tests with 'invalid' means bad info/empty info/missing info
    # so each test can hold several smaller tests


    # purchaseConfirmedBid
    def test_purchaseConfirmedBid_success(self):
        pass

    def test_purchaseConfirmedBid_userNotLoggedIn_fail(self):
        pass

    def test_purchaseConfirmedBid_cardNumberInvalid_fail(self):
        pass

    def test_purchaseConfirmedBid_cardDateInvalid_fail(self):
        pass

    def test_purchaseConfirmedBid_cardNameInvalid_fail(self):
        pass

    def test_purchaseConfirmedBid_cardCcvInvalid_fail(self):
        pass

    def test_purchaseConfirmedBid_addressInvalid_fail(self):
        pass

    def test_purchaseConfirmedBid_productInBasketOutOfStock_fail(self):
        pass

    def test_purchaseConfirmedBid_productInBasketNotExists_fail(self):
        pass

    def test_purchaseConfirmedBid_bidNotConfirmed_fail(self):
        pass

    def test_purchaseConfirmedBid_bidNotExists_fail(self):
        pass

    # register
    def test_register_success(self):
        pass

    def test_register_usernameAlreadyExists_fail(self):
        pass

    def test_register_usernameIsEmpty_fail(self):
        pass

    def test_register_passwordIsEmpty_fail(self):
        pass

    def test_register_emailIsEmpty_fail(self):
        pass

    def test_register_userAlreadyLoggedIn_fail(self):
        pass

    # rejectBid
    def test_rejectBid_success(self):
        pass

    def test_rejectBid_userNotLoggedIn_fail(self):
        pass

    def test_rejectBid_storeNotExists_fail(self):
        pass

    def test_rejectBid_storeIsClosed_fail(self):
        pass

    def test_rejectBid_bidNotExists_fail(self):
        pass

    def test_rejectBid_bidNotBelongToUser_fail(self):
        pass

    def test_rejectBid_bigAlreadyAccepted_fail(self):
        pass

    def test_rejectBid_bidAlreadyRejected_fail(self):
        pass

    # removeAccess
    def test_removeAccess_success(self):
        pass

    def test_removeAccess_userNotLoggedIn_fail(self):
        pass

    def test_removeAccess_storeNotExists_fail(self):
        pass

    def test_removeAccess_storeIsClosed_fail(self):
        pass

    def test_removeAccess_requesterIsRequstee_fail(self):
        # yaani user ose removeAccess al atsmo inaal dinak
        pass

    def test_removeAccess_requesterHasNoPermissions_fail(self):
        pass

    def test_removeAccess_requesteeHasNoAccess_fail(self):
        pass

    # removeFromBasket
    def test_removeFromBasket_success(self):
        pass

    def test_removeFromBasket_userNotLoggedIn_fail(self):
        pass

    def test_removeFromBasket_basketNotExists_fail(self):
        pass

    def test_removeFromBasket_productNotExists_fail(self):
        pass

    def test_removeFromBasket_storeNotExists_fail(self):
        pass

    def test_removeFromBasket_storeIsClosed_fail(self):
        #TODO: should it be success?
        pass

    def test_removeFromBasket_productNotInBasket_fail(self):
        pass

    # removeMember
    def test_removeMember_success(self):
        pass

    def test_removeMember_userNotLoggedIn_fail(self):
        pass

    def test_removeMember_userNotAdmin_fail(self):
        pass

    def test_removeMember_memberNotExists_fail(self):
        pass

    def test_removeMember_memberIsOwner_success(self):
        # TODO: need to check that it removes all accesses that member has appointed
        pass

    def test_removeMember_memberIsAdmin_fail(self):
        # TODO: should it be success? can we use removeMember on admin?
        pass

    # removePermissions
    def test_removePermissions_success(self):
        pass

    def test_removePermissions_userNotLoggedIn_fail(self):
        pass

    def test_removePermissions_storeNotExists_fail(self):
        pass

    def test_removePermissions_storeIsClosed_fail(self):
        pass

    def test_removePermissions_requesterHasNoPermissions_fail(self):
        pass

    def test_removePermissions_requesteeHasNoAccess_fail(self):
        pass

    def test_removePermissions_permissionsInvalid_fail(self):
        pass

    # removeProductFromStore
    def test_removeProductFromStore_success(self):
        pass

    def test_removeProductFromStore_userNotLoggedIn_fail(self):
        pass

    def test_removeProductFromStore_storeNotExists_fail(self):
        pass

    def test_removeProductFromStore_storeIsClosed_fail(self):
        pass

    def test_removeProductFromStore_productNotExists_fail(self):
        pass

    def test_removeProductFromStore_productInBasket_success(self):
        # TODO: check that product is deleted from baskets
        pass

    def test_removeProductFromStore_productWithSpecialPolicies_success(self):
        # TODO: check that product is deleted properly
        pass

    # returnToGuest
    def test_returnToGuest_success(self):
        pass

    def test_returnToGuest_userNotLoggedIn_fail(self):
        pass

    def test_returnToGuest_userIsGuest_fail(self):
        pass

    def test_returnToGuest_userIsAdmin_fail(self):
        pass

    def test_returnToGuest_cartNotEmpty_success(self):
        # TODO: check that the cart is transferred to the guest user
        pass

    # sendAlternativeBid
    def test_sendAlternativeBid_success(self):
        pass

    def test_sendAlternativeBid_userNotLoggedIn_fail(self):
        pass

    def test_sendAlternativeBid_storeNotExists_fail(self):
        pass

    def test_sendAlternativeBid_storeIsClosed_fail(self):
        pass

    def test_sendAlternativeBid_bidNotExists_fail(self):
        pass

    def test_sendAlternativeBid_bidAlreadyAccepted_fail(self):
        pass

    def test_sendAlternativeBid_bidAlreadyRejected_fail(self):
        pass

    def test_sendAlternativeBid_alternateBidIsLower_fail(self):
        pass

    # django_getAllStaffMembersNames(self, storename)
    def test_django_getAllStaffMembersNames_success(self):
        pass

    def test_django_getAllStaffMembersNames_storeNotExists_fail(self):
        pass

    def test_django_getAllStaffMembersNames_storeIsClosed_fail(self):
        pass

    # messageAsAdminToUser(admin_name, receiverID, message)
    def test_messageAsAdminToUser_receiverIsAdmin_success(self):
        pass

    def test_messageAsAdminToUser_receiverIsGuest_success(self):
        pass

    def test_messageAsAdminToUser_receiverIsMember_success(self):
        pass

    def test_messageAsAdminToUser_adminNotExists_fail(self):
        pass

    def test_messageAsAdminToUser_adminNotLoggedIn_fail(self):
        pass

    def test_messageAsAdminToUser_receiverNotExists_fail(self):
        pass

    def test_messageAsAdminToUser_receiverIsStore_fail(self):
        pass

    # messageAsAdminToStore(admin_name, store_Name, message)
    def test_messageAsAdminToStore_receiverIsStore_success(self):
        pass

    def test_messageAsAdminToStore_receiverIsAdmin_fail(self):
        pass

    def test_messageAsAdminToStore_receiverIsGuest_fail(self):
        pass

    def test_messageAsAdminToStore_receiverIsMember_fail(self):
        pass

    def test_messageAsAdminToStore_adminNotExists_fail(self):
        pass

    def test_messageAsAdminToStore_adminNotLoggedIn_fail(self):
        pass

    def test_messageAsAdminToStore_storeNotExists_fail(self):
        pass

    # ----------------------------------------------------------------------------------

    # MORE TESTS IDEAS:
    # 1. check if guest can add to cart, login as member and still have the cart
    # 2. check if guest can add to cart, turn off browser, login as guest back and still have the cart


































if __name__ == '__main__':
    unittest.main()
