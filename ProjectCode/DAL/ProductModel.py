from peewee import *



class ProductModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'product'

    product_id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    quantity = IntegerField()
    price = IntegerField()
    categories = CharField(max_length=100)

