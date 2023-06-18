from datetime import datetime
from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class UserTransactionModel(Model):
    class Meta:
        database = DatabaseConf.database
        db_table = 'user_transaction'

    transaction_id = IntegerField(primary_key=True)
    supply_id = IntegerField()
    username = CharField(max_length=100)
    overall_price = DoubleField()
    date = DateTimeField()
