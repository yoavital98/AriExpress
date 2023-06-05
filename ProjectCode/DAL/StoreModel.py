from peewee import *

from ProjectCode.DAL.AccessModel import AccessModel
from ProjectCode.DAL.ProductModel import ProductModel


class StoreModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'store'


    store_name = CharField(max_length=100, primary_key=True)
    products = ManyToManyField(ProductModel, backref='store')
    #accesses = ManyToManyField(AccessModel, backref='store')