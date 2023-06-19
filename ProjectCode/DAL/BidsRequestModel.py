from peewee import *
from ProjectCode.DAL.BidModel import BidModel
from ProjectCode.DAL.database_conf import DatabaseConf


class BidsRequestModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'bids_request'

    wait_for_approve_user_name = CharField(max_length=100)
    bid_id = ForeignKeyField(BidModel, backref='bids_request')
