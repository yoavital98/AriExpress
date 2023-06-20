from peewee import *
# from playhouse.mysql_ext import *
from playhouse.postgres_ext import *
from ProjectCode.DAL.StoreModel import StoreModel
from ProjectCode.DAL.database_conf import DatabaseConf


class PurchasePolicyModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'purchase_policy'

    policy_id = AutoField()
    store = ForeignKeyField(StoreModel, backref='policies')
    policy_type = CharField(max_length=100)
    level = CharField(max_length=100)
    level_name = CharField(max_length=100)
    rule = JSONField(null=True)

