from peewee import *



class AccessStateModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'access_states'

    permissions = CharField(max_length=1000)
    state = CharField(max_length=100)



