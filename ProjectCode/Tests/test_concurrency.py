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


def test_func_ten(func, *args, **kwargs):
    # Create a shared variable to track the success/failure of foo()
    result = {'success_count': 0, 'failure_count': 0}

    def run_func():
        try:
            func(*args, **kwargs)  # Call foo()
            result['success_count'] += 1
            print(f"success: {result.get('success_count')}")
        except Exception:
            result['failure_count'] += 1
            print(f"success: {result.get('failure_count')}")

    threads = []
    for _ in range(10):
        thread = threading.Thread(target=run_func)
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Check the result
    assert result['success_count'] == 10, "All function calls should succeed"
    assert result['failure_count'] == 10, "All function calls should fail"

def test_func_one(func, *args, **kwargs):
    # Create a shared variable to track the success/failure of foo()
    result = {'success_count': 0, 'failure_count': 0}

    def run_func():
        try:
            func(*args, **kwargs)  # Call foo()
            result['success_count'] += 1
            print(f"success: {result.get('success_count')}")
        except Exception:
            result['failure_count'] += 1
            print(f"success: {result.get('failure_count')}")

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
    def setUp(self):
        self.store_facade = StoreFacade()
        self.store_facade.register("username", "password", "email")
        self.store_facade.logInAsMember("username", "password")
        self.store_facade.createStore("username", "storename")
        self.store_facade.addNewProductToStore("username", "storename", "product1", 100, 10, "category")
        # self.store_facade.addNewProductToStore("username", "storename", "product2", 100, 10, "category")

    def test_addToBasket_success(self):
        # test_func(self.store_facade.purchaseCart("username", 1234, "feliks", 123456789, 1, 111, "okokok"))
        # test_func_one(self.store_facade.purchaseCart, "username", 1234, "feliks", 123456789, 1, 111, "okokok")
        for i in range(0, 10):
            self.store_facade.addToBasket("username", "storename", 1, 5)
            test_func_one(self.store_facade.purchaseCart, "username", 1234, "feliks", 123456789, 1, 111, "okokok")
        


if __name__ == '__main__':
    unittest.main()
