from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.ProductModel import ProductModel

class ProductBasketModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'product_basket'


    product_id = IntegerField(primary_key=True)
    quantity = IntegerField()
    product_model = ForeignKeyField(ProductModel, backref='product_basket')
    basket = ForeignKeyField(BasketModel, backref='products')
    price = DoubleField()
