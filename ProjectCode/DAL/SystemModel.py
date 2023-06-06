from peewee import *


class SystemModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'system'

    entrance_id = IntegerField(primary_key=True)
