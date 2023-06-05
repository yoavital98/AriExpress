from peewee import *

from ProjectCode.DAL.CartModel import CartModel
from ProjectCode.DAL.MemberModel import MemberModel
from ProjectCode.Domain.MarketObjects.UserObjects.Member import Member
from ProjectCode.Domain.Repository.Repository import Repository


class MemberRepository(Repository):

    def __init__(self):
        self.model = MemberModel

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("MemberRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("MemberRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("MemberRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
         pass

    def get(self, pk=None):
        if not pk:
            member_list = []
            for entry in self.model.select():
                member_list.append(Member(-1, entry.user_name, entry.password, entry.email))
            return member_list
        else:
            entry = self.model.get(self.model.user_name == pk)
            member_obj = Member(-1, entry.user_name, entry.password, entry.email)
            return member_obj

    def add(self, member: Member):
        cart = CartModel.create(user_name=member.get_username())
        member_entry = self.model.create(user_name=member.get_username(), password=member.get_password() ,email=member.get_email(), cart=cart)
        return member

    def remove(self, pk):
        user_entry = MemberModel.get(MemberModel.user_name == pk)
        user_entry.cart.delete_instance()
        user_entry.delete_instance()

    def keys(self):
        return [member.user_name for member in MemberModel.select()]

    def values(self):
        return self.get()
