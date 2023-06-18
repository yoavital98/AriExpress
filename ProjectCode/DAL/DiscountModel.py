from peewee import *
from playhouse.sqlite_ext import *
# from playhouse.postgres_ext import *

from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class DiscountModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'discount'

    discount_id = AutoField()
    store = ForeignKeyField(StoreModel, backref='discounts')
    discount_type = CharField(max_length=100)
    percent = IntegerField()
    level = CharField(max_length=100)
    level_name = CharField(max_length=100)
    rule = JSONField(null=True) #ConditionedDiscount
    discount_dict = JSONField(null=True) #AddComp or MaxComp
    #parent_discount = ForeignKeyField('self', null=True, backref='discounts')

