from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.ProductModel import ProductModel

class ProductBasketModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'productBasket'

    quantity = IntegerField()
    product = ForeignKeyField(ProductModel)
    basket = ForeignKeyField(BasketModel, backref='products')
