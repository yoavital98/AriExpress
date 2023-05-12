from datetime import datetime

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize
from ProjectCode.Domain.Helpers.TypedDict import TypedDict


class UserTransaction:
    def __init__(self, username, products, overall_price):
        self._username = username
        self._products = products  # TypedDict(str, set): store_name -> set of tuples (product_name, quantity, price)
        self._overall_price = overall_price
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_username(self):
        return self._username

    def get_products(self):
        return self._products

    def get_overall_price(self):
        return self._overall_price

    def get_date(self):
        return self._date

    def __str__(self):
        def __str__(self):
            return f"Purchase made by {self._username} at {self._storename} on {self._date}\nProducts: {self._products}\nOverall price: {self._overall_price}"

    # =======================JSON=======================#

    def toJson(self):
        return {
            "username": self._username,
            "products": JsonSerialize.toJsonAttributes(self._products),
            "overall_price": self._overall_price,
            "date": self._date
        }