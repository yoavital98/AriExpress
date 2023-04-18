import unittest
from unittest import TestCase
from unittest.mock import MagicMock
from ProjectCode.Domain.Controllers.StoreFacade import StoreFacade




class TestStoreFacade(TestCase):

    def setUp(self):
        self.store_facade = StoreFacade()

    def test_load_data(self):
        self.fail()

    def test_exit_the_system(self):
        self.fail()

    def test_register_new_member(self):
        username = "test_user"
        password = "test_password"
        email = "test_email@example.com"
        self.store_facade.passwordValidator.ValidatePassword = MagicMock(return_value=True)
        member = self.store_facade.register(username, password, email)
        self.assertEqual(self.store_facade.members[username], member)

    def test_log_in_as_guest(self):
        self.fail()

    def test_log_in_as_member(self):
        self.fail()

    def test_log_out(self):
        self.fail()

    def test_get_member_purchase_history(self):
        self.fail()

    def test_get_stores(self):
        self.fail()

    def test_get_products_by_store(self):
        self.fail()

    def test_get_product(self):
        self.fail()

    def test_product_search_by_name(self):
        self.fail()

    def test_product_search_by_category(self):
        self.fail()

    def test_product_filter_by_features(self):
        self.fail()

    def test_get_basket(self):
        self.fail()

    def test_get_cart(self):
        self.fail()

    def test_add_to_basket(self):
        self.fail()

    def test_remove_from_basket(self):
        self.fail()

    def test_edit_basket_quantity(self):
        self.fail()

    def test_purchase_cart(self):
        self.fail()

    def test_place_bid(self):
        self.fail()

    def test_get_store_purchase_history(self):
        self.fail()

    def test_open_store(self):
        self.fail()

    def test_add_new_product_to_store(self):
        self.fail()

    def test_remove_product_from_store(self):
        self.fail()

    def test_edit_product_of_store(self):
        self.fail()

    def test_nominate_store_owner(self):
        self.fail()

    def test_nominate_store_manager(self):
        self.fail()

    def test_add_permissions_for_manager(self):
        self.fail()

    def test_edit_permissions_for_manager(self):
        self.fail()

    def test_close_store(self):
        self.fail()

    def test_get_staff_info(self):
        self.fail()

    def test_get_store_manager_permissions(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()