import unittest
from unittest import TestCase
from unittest.mock import MagicMock, Mock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade, Cart
from ProjectCode.Domain.Objects.Store import Store
from ProjectCode.Domain.Objects.UserObjects.Member import Member


class TestStoreFacade(TestCase):

    def setUp(self):
        # TODO: check info for duplicates
        # TODO: check implementations of tests
        self.store_facade = StoreFacade()
        self.member1 = Member("John", "password123", "john.doe@example.com")
        self.store_facade.members["John"] = self.member1
        self.member2 = Member("Jane", "password456", "jane.doe@example.com")
        self.store_facade.members["Jane"] = self.member2
        # self.store = Store("Store1")
        # self.store_facade.stores["Store1"] = self.store

    


if __name__ == '__main__':
    unittest.main()
