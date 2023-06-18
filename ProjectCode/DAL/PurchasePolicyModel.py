from peewee import *
from playhouse.mysql_ext import *

from ProjectCode.DAL.StoreModel import StoreModel


class PurchasePolicyModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'purchase_policy'

    policy_id = AutoField()
    store = ForeignKeyField(StoreModel, backref='policies')
    policy_type = CharField(max_length=100)
    level = CharField(max_length=100)
    level_name = BareField()
    rule = JSONField(null=True) #ConditionedDiscount
    #parent_discount = ForeignKeyField('self', null=True, backref='discounts')

