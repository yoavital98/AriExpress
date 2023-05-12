from datetime import datetime


class StoreTransaction:
    def __init__(self, username, storename, products, overall_price):
        self._username = username
        self._store_name = storename
        self._products = products  # set of tuples (product_id, product_name, quantity)
        self._overall_price = overall_price
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_username(self):
        return self._username

    def get_storename(self):
        return self._store_name

    def get_products(self):
        return self._products

    def get_overall_price(self):
        return self._overall_price

    def get_date(self):
        return self._date

    def __str__(self):
        product_list = "\n".join([f"{k}: {v[0]} x {v[1]}" for k, v in self._products.items()])
        return f"Transaction on {self._date}:\nStore: {self._store_name}\nUser: {self._username}\nProducts:\n{product_list}\nOverall Price: {self._overall_price}"
