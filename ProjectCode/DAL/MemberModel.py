from peewee import *

from ProjectCode.DAL.database_conf import DatabaseConf


#from ProjectCode.DAL.CartModel import CartModel
# from ProjectCode.DAL.AccessModel import AccessModel
# from ProjectCode.DAL.AuctionModel import AuctionModel
# from ProjectCode.DAL.LotteryModel import LotteryModel


class MemberModel(Model):

    class Meta:
        database = DatabaseConf.database
        db_table = 'member'

    user_name = CharField(max_length=100, primary_key=True)
    password = CharField(max_length=100)
    email = CharField(max_length=100)
    entrance_id = IntegerField()
    logged_in = BooleanField(default=False)
    banned = BooleanField(default=False)

    #cart = ForeignKeyField(CartModel, backref='member')
    #accesses = ManyToManyField(AccessModel, backref='member')
    # auctions = ManyToManyField(AuctionModel, backref='member')
    # lotteries = ManyToManyField(LotteryModel, backref='member')

