from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class MessageModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'message'

    message_id = AutoField()
    sender_id = CharField(max_length=100)
    receiver_id = CharField(max_length=100)
    subject = CharField(max_length=100)
    content = CharField(max_length=100)
    date = DateTimeField()
    read = BooleanField(default=False)

