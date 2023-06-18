from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class GuestModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'guest'

    entrance_id = CharField(max_length=100, primary_key=True)
