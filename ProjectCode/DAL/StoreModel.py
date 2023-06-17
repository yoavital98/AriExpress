from peewee import *

#from ProjectCode.DAL.ProductModel import ProductModel


class StoreModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'store'


    store_name = CharField(max_length=100, primary_key=True)
    active = BooleanField(default=True)
    closed_by_admin = BooleanField(default=False)
    product_id_counter = IntegerField()
    auction_id_counter = IntegerField(default=0)
    lottery_id_counter = IntegerField(default=0)
    #products = ManyToManyField(ProductModel, backref='store')
    #accesses = ManyToManyField(AccessModel, backref='store')