from peewee import *

class BasketModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'basket'

    user_name = CharField(max_length=100, primary_key=True)
