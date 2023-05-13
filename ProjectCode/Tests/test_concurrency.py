import unittest
from unittest import TestCase
from ProjectCode.Domain.MarketObjects.Store import Store
from ProjectCode.Domain.MarketObjects.UserObjects import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.MarketObjects.UserObjects.Admin import Admin
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Service.Service import Service
import threading

class TestStoreFacade(TestCase):

    def setUp(self):
        self.Service = Service()
        # self.Service.register("username", "password", "email")
        # self.Service.logIn("username", "password")
        # self.Service.openStore("username", "storename")
        # self.Service.addNewProductToStore("username", "storename", "product1", "category", 10, 10)
        # self.Service.addNewProductToStore("username", "storename", "product2", "category", 10, 10)


    def test_foo(func):
        # Create a shared variable to track the success/failure of foo()
        result = {'success_count': 0, 'failure_count': 0}

        def run_func():
            try:
                func()  # Call foo()
                result['success_count'] += 1
            except Exception:
                result['failure_count'] += 1

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




if __name__ == '__main__':
    unittest.main()
