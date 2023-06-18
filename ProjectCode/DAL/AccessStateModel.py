from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class AccessStateModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'access_states'

    permissions = CharField(max_length=1000)
    state = CharField(max_length=100)



