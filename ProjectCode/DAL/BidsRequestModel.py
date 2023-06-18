from peewee import *
from ProjectCode.DAL.BidModel import BidModel


class BidsRequestModel(Model):

    class Meta:
        database = SqliteDatabase('database.db')
        db_table = 'bids_request'

    wait_for_approve_user_name = CharField(max_length=100)
    bid_id = ForeignKeyField(BidModel, backref='bids_request')
