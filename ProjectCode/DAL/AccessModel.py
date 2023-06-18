from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf
from ProjectCode.DAL.AccessStateModel import AccessStateModel



class AccessModel(Model):

    class Meta:
        database = DatabaseConf.database
        # database = PostgresqlDatabase('gebvljnj', user='gebvljnj', password='WoCu2HIY7yeExx9B2l_ea0Qhpl5hJT3I',
        #                         host='rogue.db.elephantsql.com', port=5432)
        db_table = 'accesses'
        primary_key = CompositeKey('store', 'user')

    from ProjectCode.DAL.MemberModel import MemberModel
    from ProjectCode.DAL.StoreModel import StoreModel

    store = ForeignKeyField(StoreModel, backref='accesses')
    user = ForeignKeyField(MemberModel, backref='accesses')
    nominated_by_username = CharField(max_length=100)
    role = CharField(max_length=100)
    access_state = ForeignKeyField(AccessStateModel, backref='accesses')
    nominations = CharField(max_length=1000)
    # access_state = ForeignKeyField
