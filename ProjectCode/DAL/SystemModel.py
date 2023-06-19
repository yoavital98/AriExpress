from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class SystemModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'system'

    entrance_id = IntegerField()
    bid_id_counter = IntegerField()