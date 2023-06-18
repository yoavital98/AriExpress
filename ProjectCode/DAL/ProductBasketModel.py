from peewee import *

from ProjectCode.DAL.BasketModel import BasketModel
from ProjectCode.DAL.ProductModel import ProductModel
from ProjectCode.DAL.database_conf import DatabaseConf


class ProductBasketModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'product_basket'


    product_id = IntegerField()
    quantity = IntegerField()
    product_model = ForeignKeyField(ProductModel, backref='product_basket')
    basket = ForeignKeyField(BasketModel, backref='products')
    price = DoubleField()
