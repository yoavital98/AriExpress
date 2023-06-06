from peewee import *



class AdminModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'admin'

    user_name = CharField(max_length=100, primary_key=True)
    password = CharField(max_length=100)
    email = CharField(max_length=100)
    logged_in = BooleanField()


