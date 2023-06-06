from peewee import *
#from playhouse.sqlite_ext import *
from playhouse.mysql_ext import *

from ProjectCode.DAL.StoreModel import StoreModel


class DiscountModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'discount'

    discount_id = AutoField()
    store = ForeignKeyField(StoreModel, backref='discounts')
    discount_type = CharField(max_length=100)
    percent = IntegerField()
    level = CharField(max_length=100)
    level_name = BareField()
    rule = JSONField(null=True) #ConditionedDiscount
    discount_dict = JSONField(null=True) #AddComp or MaxComp
    #parent_discount = ForeignKeyField('self', null=True, backref='discounts')

