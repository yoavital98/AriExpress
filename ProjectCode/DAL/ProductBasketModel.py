from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.ProductModel import ProductModel

class ProductBasketModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'product_basket'

    product_id = IntegerField()
    quantity = IntegerField()
    product = ForeignKeyField(ProductModel)
    basket = ForeignKeyField(BasketModel, backref='products')
    price = DoubleField()
