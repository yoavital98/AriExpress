from peewee import *

from ProjectCode.DAL.AccessStateModel import AccessStateModel



class AccessModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
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
