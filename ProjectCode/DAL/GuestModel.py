from peewee import *



class GuestModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'guest'

    entrance_id = CharField(max_length=100, primary_key=True)
