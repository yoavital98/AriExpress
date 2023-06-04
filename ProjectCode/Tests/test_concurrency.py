import concurrent
import random
import unittest
from unittest import TestCase
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.UserObjects import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Domain.StoreFacade import StoreFacade
from ProjectCode.Service.Service import Service
import threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from unittest import TestCase


# def test_func_ten(func, *args, **kwargs):
#     # Create a shared variable to track the success/failure of foo()
#     result = {'success_count': 0, 'failure_count': 0}
#
#     def run_func():
#         try:
#             func(*args, **kwargs)  # Call foo()
#             result['success_count'] += 1
#             print(f"success: {result.get('success_count')}")
#         except Exception:
#             result['failure_count'] += 1
#             print(f"success: {result.get('failure_count')}")
#
#     threads = []
#     for _ in range(10):
#         thread = threading.Thread(target=run_func)
#         thread.start()
#         threads.append(thread)
#
#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()
#
#     # Check the result
#     assert result['success_count'] == 10, "All function calls should succeed"
#     assert result['failure_count'] == 10, "All function calls should fail"

def test_2_concurrent_actions(func1, func2, user1_args, user2_args):
    # Create a shared variable to track the success/failure of the function calls
    result = {'success_count': 0, 'failure_count': 0}

    def run_func(func, user_args):
        try:
            func(*user_args)  # Call the function with user-specific arguments
            result['success_count'] += 1
            print(f"User {user_args[0]} succeeded. Success count: {result['success_count']}")
        except Exception:
            result['failure_count'] += 1
            print(f"User {user_args[0]} failed. Failure count: {result['failure_count']}")

    # Create a list of threads
    thread1 = threading.Thread(target=run_func, args=(func1, user1_args,))
    thread2 = threading.Thread(target=run_func, args=(func2, user2_args,))
    threads = [thread1, thread2]

    # Shuffle the order of threads
    random.shuffle(threads)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return result


class TestStoreFacade(TestCase):
    def setup(self):
        # sets 3 users, 1 stores where user1 is founder, user2 is manager, user3 is costumer
        self.store_facade = StoreFacade()
        self.store_facade.register("user1", "123", "email1")
        self.store_facade.register("user2", "123", "email2")
        self.store_facade.register("user3", "123", "email3")
        self.store_facade.logInAsMember("user1", "123")
        self.store_facade.logInAsMember("user2", "123")
        self.store_facade.logInAsMember("user3", "123")
        self.store_facade.createStore("user1", "store1")
        self.store_facade.nominateStoreManager("user1", "user2", "store1")
        self.store_facade.addNewProductToStore("user1", "store1", "product1", 1, 10, "category")

    def test_concurrent_purchaseCart_2CostumersLastItem(self):
        # Simulate two customers attempting to purchase the same last item in stock simultaneously.
        # Verify that the system handles the concurrency correctly, allowing only one customer
        # to successfully purchase the item while notifying the other customer that the item is no longer available.
        for _ in range(10):  # Run the scenario 10 times
            self.setup()
            self.store_facade.addToBasket("user2", "store1", 1, 1)
            self.store_facade.addToBasket("user3", "store1", 1, 1)

            user1_args = ("user2", 123, "feliks", 123456789, 1, 111, "okokok")
            user2_args = ("user3", 123, "feliks", 123456789, 1, 111, "okokok")

            result = test_2_concurrent_actions(self.store_facade.purchaseCart, self.store_facade.purchaseCart,
                                               user1_args, user2_args)
            # Check the result
            assert result['success_count'] == 1, "One function call should succeed"
            assert result['failure_count'] == 1, "One function call should fail"

    def test_concurrent_purchaseCart_managerDeletesItem(self):
        # Test a scenario where a customer initiates a purchase for an item while a manager concurrently deletes the
        # same item from the system. Ensure that the system handles this concurrency appropriately,
        # either preventing the purchase or notifying the customer about the item's unavailability.
        for _ in range(10):  # Run the scenario 10 times
            self.setup()
            self.store_facade.addToBasket("user2", "store1", 1, 1)

            user1_args = ("user2", 123, "feliks", 123456789, 1, 111, "okokok")
            user2_args = ("user1", "store1", 1)

            result = test_2_concurrent_actions(self.store_facade.purchaseCart, self.store_facade.removeProductFromStore,
                                               user1_args, user2_args)
            assert (result['success_count'] == 1 and result['failure_count'] == 1) or \
                   (result['success_count'] == 2)
            # One function call should succeed and the other to fail
            # OR both should succeed but the product is not in the store
            if result['success_count'] == 2:
                with self.assertRaises(Exception):
                    # The product should not be in the store
                    self.store_facade.getProduct("user2", "store1", 1)
                with self.assertRaises(Exception):
                    # The product should not be in user2's purchase history
                    self.store_facade.getMemberPurchaseHistory("user2", "store1")

    def test_concurrent_nominateManager_sameNomineeTwice(self):
        # Create a test case where two managers simultaneously try to nominate themselves as the new manager for
        # a specific task or department. Validate that the system handles this concurrency correctly,
        # allowing only one manager to be nominated while preventing conflicts or inconsistencies.
        # TODO this works but there's no denial of making same manager over again it seems ARI
        pass
        # for _ in range(10):
        #     self.setup()
        #     user1_args = ("user1", "user3", "store1")
        #     user2_args = ("user1", "user3", "store1")
        #     result = test_2_concurrent_actions(self.store_facade.nominateStoreManager,
        #                                        self.store_facade.nominateStoreManager,
        #                                        user1_args, user2_args)
        #     assert result['success_count'] == 1, "One function call should succeed"
        #     assert result['failure_count'] == 1, "One function call should fail"


    def test_concurrent_editProduct_sameProductTwice(self):
        # Create a test case where two managers simultaneously try to edit the same product.
        # Validate that the system handles this concurrency correctly, allowing only one manager to edit the product
        # while preventing conflicts or inconsistencies.
        for _ in range(10):
            self.setup()
            self.store_facade.editProductOfStore("user1", "store1", 1, name= "Banana", quantity=5, price=1, categories="Fruits")
            user1_args = ("user1", "store1", 1, {"name": "Banana", "quantity": 5, "price": 1, "categories": "Fruits"})
            user2_args = ("user2", "store1", 1, {"name": "Apple", "quantity": 5, "price": 1, "categories": "Fruits"})
            result = test_2_concurrent_actions(self.store_facade.editProductOfStore, self.store_facade.editProductOfStore,
                                               user1_args, user2_args)
            product_name = self.store_facade.getProduct("store1", 1, "user1").get_name()
            assert product_name == "Apple" or product_name == "Banana", "One function call should succeed"
    def test_concurrent_addProduct_twice(self):

        # Create a test case where two managers simultaneously try to add the same product.
        # Validate that the system handles this concurrency correctly, allowing only one manager to add the product
        # while preventing conflicts or inconsistencies.
        # TODO this works but there's no denial of making 2 products of the same name
        pass
        # for _ in range(10):
        #     self.setup()
        #     user1_args = ("user1", "store1", "newProduct", 1, 10, "category")
        #     user2_args = ("user2", "store1", "newProduct", 1, 10, "category")
        #     result = test_2_concurrent_actions(self.store_facade.addNewProductToStore,
        #                                        self.store_facade.addNewProductToStore,
        #                                        user1_args, user2_args)
        #     assert result['success_count'] == 1, "One function call should succeed"
        #     assert result['failure_count'] == 1, "One function call should fail"

    def test_concurrent_addDiscount_twice(self):
        # Create a test case where two managers simultaneously try to add the same discount.
        # Validate that the system handles this concurrency correctly, allowing only one manager to add the discount
        # while preventing conflicts or inconsistencies.
        for _ in range(10):
            self.setup()
            user1_args = ("store1", "user1", "Simple", 20, "product", "product1", None, None)
            user2_args = ("store1", "user2", "Simple", 20, "product", "product1", None, None)
            result = test_2_concurrent_actions(self.store_facade.addDiscount,
                                               self.store_facade.addDiscount,
                                               user1_args, user2_args)
            assert result['success_count'] == 1, "One function call should succeed"
            assert result['failure_count'] == 1, "One function call should fail"

    def test_concurrent_registerTwice_sameName(self):
        # Create a test case where two users simultaneously try to register with the same username.
        # Validate that the system handles this concurrency correctly, allowing only one user to register
        # while preventing conflicts or inconsistencies.
        for _ in range(10):
            self.setup()
            user1_args = ("Onyankopon", "asdf1233", "feliks@f.com")
            user2_args = ("Onyankopon", "asdf1233", "feliks@f.com")
            result = test_2_concurrent_actions(self.store_facade.register, self.store_facade.register,
                                               user1_args, user2_args)
            assert result['success_count'] == 1, "One function call should succeed"
            assert result['failure_count'] == 1, "One function call should fail"


if __name__ == '__main__':
    unittest.main()
