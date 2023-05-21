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

def test_func_one(func, *args, **kwargs):
    # Create a shared variable to track the success/failure of foo()
    result = {'success_count': 0, 'failure_count': 0}

    def run_func():
        try:
            func(*args, **kwargs)  # Call foo()
            result['success_count'] += 1
            print(f"success_success: {result.get('success_count')}")
        except Exception:
            result['failure_count'] += 1
            print(f"failure_success: {result.get('failure_count')}")

    # Create two threads to run foo() concurrently
    thread1 = threading.Thread(target=run_func)
    thread2 = threading.Thread(target=run_func)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Check the result
    assert result['success_count'] == 1, "One function call should succeed"
    assert result['failure_count'] == 1, "One function call should fail"

class TestStoreFacade(TestCase):
    def baseSetUp(self):
        # sets 3 users, 1 stores where user1 is founder, user2 is manager, user3 is costumer
        self.store_facade = StoreFacade()
        self.store_facade.register("user1", "123", "email1")
        self.store_facade.register("user2", "123", "email2")
        self.store_facade.register("user3", "123", "email3")
        self.store_facade.logInAsMember("user1", "123")
        self.store_facade.logInAsMember("user2", "123")
        self.store_facade.createStore("user1", "store1")
        self.store_facade.nominateStoreManager("user1", "user2", "store1")
        self.store_facade.addNewProductToStore("user1", "store1", "product1", 100, 10, "category")

    def setUpForPurchaseCartTwice(self):
        self.store_facade = StoreFacade()
        self.store_facade.register("username", "password", "email")
        self.store_facade.logInAsMember("username", "password")
        self.store_facade.createStore("username", "storename")
        self.store_facade.addNewProductToStore("username", "storename", "product1", 100, 10, "category")

    def setUpForPurchaseCartUsers(self):
        pass

    def setUpForPurchaseCartManagerDeletes(self):
        pass

    def setUpForNominateManagerTwice(self):
        pass



    def test_concurrent_purchaseCart_purchaseTwice(self):
        # test_func(self.store_facade.purchaseCart("username", 1234, "feliks", 123456789, 1, 111, "okokok"))
        # test_func_one(self.store_facade.purchaseCart, "username", 1234, "feliks", 123456789, 1, 111, "okokok")
        self.setUpForPurchaseCartTwice()
        for i in range(0, 10):
            self.store_facade.addToBasket("username", "storename", 1, 5)
            test_func_one(self.store_facade.purchaseCart, "username", 1234, "feliks", 123456789, 1, 111, "okokok")

    def test_concurrent_purchaseCart_2CostumersLastItem(self):
        # Simulate two customers attempting to purchase the same last item in stock simultaneously.
        # Verify that the system handles the concurrency correctly, allowing only one customer
        # to successfully purchase the item while notifying the other customer that the item is no longer available.
        self.setUpForPurchaseCartTwice()
        self.store_facade.addToBasket("username", "storename", 1, 10)
        self.store_facade.addToBasket("username", "storename", 1, 10)
        self.store_facade.purchaseCart("username", 1234, "feliks", 123456789, 1, 111, "okokok")
        self.store_facade.purchaseCart("username", 1234, "feliks", 123456789, 1, 111, "okokok")

    def test_concurrent_purchaseCart_managerDeletesItem(self):
        # Test a scenario where a customer initiates a purchase for an item while a manager concurrently deletes the
        # same item from the system. Ensure that the system handles this concurrency appropriately,
        # either preventing the purchase or notifying the customer about the item's unavailability.
        self.setUpForPurchaseCartManagerDeletes()
        self.store_facade.addToBasket("username", "storename", 1, 10)
        self.store_facade.addToBasket("username", "storename", 1, 10)

    def test_concurrent_nominateManager_sameNomineeTwice(self):
        # Create a test case where two managers simultaneously try to nominate themselves as the new manager for
        # a specific task or department. Validate that the system handles this concurrency correctly,
        # allowing only one manager to be nominated while preventing conflicts or inconsistencies.
        pass

    def test_concurrent_editProduct_sameProductTwice(self):
        # Create a test case where two managers simultaneously try to edit the same product.
        # Validate that the system handles this concurrency correctly, allowing only one manager to edit the product
        # while preventing conflicts or inconsistencies.
        pass

    def test_concurrent_addProduct_twice(self):
        # Create a test case where two managers simultaneously try to add the same product.
        # Validate that the system handles this concurrency correctly, allowing only one manager to add the product
        # while preventing conflicts or inconsistencies.
        pass

    def test_concurrent_addDiscount_twice(self):
        # Create a test case where two managers simultaneously try to add the same discount.
        # Validate that the system handles this concurrency correctly, allowing only one manager to add the discount
        # while preventing conflicts or inconsistencies.
        pass

    def test_concurrent_registerTwice_sameName(self):
        # Create a test case where two users simultaneously try to register with the same username.
        # Validate that the system handles this concurrency correctly, allowing only one user to register
        # while preventing conflicts or inconsistencies.
        pass

if __name__ == '__main__':
    unittest.main()
