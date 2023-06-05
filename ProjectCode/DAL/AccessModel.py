from peewee import *

from ProjectCode.DAL.AccessStateModel import AccessStateModel


class AccessModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'accesses'
        primary_key = CompositeKey('store', 'user')

    store = DeferredForeignKey('StoreModel', null=True, backref='accesses')
    user = DeferredForeignKey('MemberModel', null=True, backref='accesses')
    nominated_by_username = CharField(max_length=100)
    role = CharField(max_length=100)
    access_state = ForeignKeyField(AccessStateModel, backref='accesses', on_delete='CASCADE')
    #nominations = ManyToManyField('self', backref='children')
    # access_state = ForeignKeyField
