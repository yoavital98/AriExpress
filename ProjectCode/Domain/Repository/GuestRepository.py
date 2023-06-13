from peewee import *

from ProjectCode.DAL.GuestModel import GuestModel
from ProjectCode.Domain.MarketObjects.UserObjects.Guest import Guest
from ProjectCode.Domain.Repository.Repository import Repository


class GuestRepository(Repository):

    def __init__(self):
        self.model = GuestModel

    def __getitem__(self, entrance_id):
        return self.get(entrance_id)


    def __setitem__(self, key, value): #key is meaningless
        try:
            return self.add(value)
        except Exception as e:
            raise Exception("GuestRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("GuestRepository: __delitem__ failed: " + str(e))

    def __contains__(self, key):
        try:
            return self.contains(key)
        except Exception as e:
            raise Exception("GuestRepository: __delitem__ failed: " + str(e))

    def get(self, pk=None):
        try:
            if not pk:
                guest_list = []
                for entry in self.model.select():
                    guest_list.append(Guest(entry.entrance_id))
                return guest_list
            else:
                entry = self.model.get(self.model.entrance_id == pk)
                admin_obj = Guest(entry.entrance_id)
                return admin_obj
        except Exception as e:
            return None

    def add(self, guest: Guest):
        admin_entry = self.model.create(entrance_id=guest.entrance_id)
        return guest

    def remove(self, pk):
        user_entry = GuestModel.get(GuestModel.entrance_id == pk)
        user_entry.delete_instance()

    def keys(self):
        return [guest.entrance_id for guest in GuestModel.select()]

    def values(self):
        return self.get()

    def contains(self, entrance_id):
        query = self.model.select().where(self.model.entrance_id == entrance_id)
        return query.exists()

    def getCart(self, entrance_id):
        pass

    def clear(self):
        for entry in self.model.select():
            entry.delete_instance()
