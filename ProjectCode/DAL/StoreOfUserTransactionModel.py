from datetime import datetime
from peewee import *

from ProjectCode.DAL.UserTransactionModel import UserTransactionModel


class StoreOfUserTransactionModel(Model):
    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'store_of_user_transaction'

    store_name = CharField(max_length=100, primary_key=True)
    transaction = ForeignKeyField(UserTransactionModel, backref='store_of_user_transaction')
