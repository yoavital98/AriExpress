from datetime import datetime

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class UserTransaction:
    def __init__(self, transaction_id, supply_id, username, stores_products_dict, overall_price):
        self._transaction_id = transaction_id
        self._supply_id = supply_id
        self._username = username
        self._products_dict = stores_products_dict  # TypedDict(str, set): store_name -> set of tuples (product_id, product_name, quantity, price)
        self._overall_price = overall_price
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_username(self):
        return self._username

    def get_products(self):
        return self._products_dict

    def get_overall_price(self):
        return self._overall_price

    def get_date(self):
        return self._date

    def get_transaction_id(self):
        return self._transaction_id

    def get_supply_id(self):
        return self._supply_id

    def __str__(self):
        return f"Purchase made by {self._username} at {self._storename} on {self._date}\nProducts: {self._products_dict}\nOverall price: {self._overall_price}"

    # =======================JSON=======================#

    def toJson(self):
        return {
            "transaction_id": self._transaction_id,
            "supply_id": self._supply_id,
            "username": self._username,
            "products": JsonSerialize.toJsonAttributes(self._products_dict),
            "overall_price": self._overall_price,
            "date": self._date
        }