from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel


class ProductModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'product'

    product_id = IntegerField()
    store = ForeignKeyField(StoreModel, backref='products')
    name = CharField(max_length=100)
    quantity = IntegerField()
    price = IntegerField()
    categories = CharField(max_length=100)

