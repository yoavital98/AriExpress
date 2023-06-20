from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


class NotificationModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'notification'

    notification_id = AutoField()
    sender_id = CharField(max_length=1000)
    receiver_id = CharField(max_length=1000)
    subject = CharField(max_length=1000)
    content = CharField(max_length=1000)
    date = DateTimeField()
    read = BooleanField(default=False)