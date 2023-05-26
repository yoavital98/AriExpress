import json
from peewee import *

class Product(Model):

    product_id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    quantity = IntegerField()
    price = IntegerField()
    categories = CharField(max_length=100)

    class Meta:
        database = SqliteDatabase('database.db')

    # def __init__(self, product_id, name, quantity, price, categories):
    #     self.product_id = product_id
    #     self.name = name
    #     self.quantity = quantity
    #     self.price = price
    #     self.categories = categories

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.price

    def get_categories(self):
        return self.categories

    # =======================JSON=======================#

    def toJson(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'categories': json.dumps(self.categories)
        }
