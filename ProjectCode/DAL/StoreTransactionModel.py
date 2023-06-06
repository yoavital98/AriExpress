from peewee import *

from ProjectCode.DAL.StoreModel import StoreModel


class StoreTransactionModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'store_transaction'


    transaction_id = IntegerField(primary_key=True)
    supply_id = IntegerField()
    store_name = CharField()
    user_name = CharField(max_length=100)
    overall_price = DoubleField()
    date = DateTimeField()


    # self._transaction_id = transaction_id
    # self._supply_id = supply_id
    # self._username = username
    # self._store_name = storename
    # self._products = products  # set of tuples (product_id, product_name, quantity, price))
    # self._overall_price = overall_price
    # self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")