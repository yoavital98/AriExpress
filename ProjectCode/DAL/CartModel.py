# from peewee import *
#
# from ProjectCode.DAL.BasketModel import BasketModel
#
#
# class CartModel(Model):
#
#     class Meta:
#         database = SqliteDatabase('database.db')
#         db_table = 'cart'
#         primary_key = CompositeKey('user_name', 'store_name')
#
#     user_name = CharField(max_length=100)
#     store_name = CharField(max_length=100)
#
