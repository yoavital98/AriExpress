from datetime import datetime
from peewee import *

class UserTransactionModel(Model):
    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'user_transaction'

    transaction_id = IntegerField(primary_key=True)
    supply_id = IntegerField()
    username = CharField(max_length=100)
    overall_price = DoubleField()
    date = DateTimeField()
