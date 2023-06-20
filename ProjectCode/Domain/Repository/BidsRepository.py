from peewee import fn

from ProjectCode.DAL.BidModel import BidModel
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.Repository.Repository import Repository


class BidsRepository(Repository):
    def __init__(self):
        self.model = BidModel

    def __getitem__(self, bid_id):
        try:
            return self.get(bid_id)
        except Exception as e:
            raise Exception("BidsRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value):  # key is meaningless
        try:
            return self.add(key, value)
        except Exception as e:
            raise Exception("BidsRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("BidsRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            return False

    def get(self, pk=None):
        if pk is not None:
            bid_model = self.model.get_or_none(self.model.bid_id == pk)
            if bid_model:
                return self._map_bid_model_to_bid(bid_model)
        else:
            bid_models = self.model.select()
            return [self._map_bid_model_to_bid(bid_model) for bid_model in bid_models]

    def get_by_storename(self, store_name):
        bid_models = self.model.select().where(self.model.store_name == store_name)
        if bid_models:
            return [self._map_bid_model_to_bid(bid_model) for bid_model in bid_models]
        else:
            return []

    def get_by_username(self, username):
        bid_models = self.model.select().where(self.model.user_name == username)
        if bid_models:
            return [self._map_bid_model_to_bid(bid_model) for bid_model in bid_models]
        else:
            return []

    def add(self, key, bid: Bid):
        self.model.create(
            bid_id=bid.bid_id,
            user_name=bid._username,
            store_name=bid._storename,
            offer=bid._offer,
            product_id=bid._product_ID,
            quantity=bid._quantity,
            status=bid._status,
            left_to_approval=bid._left_to_approval
        )


    def remove(self, pk):
        bid_model = self.model.get_or_none(self.model.bid_id == pk)
        if bid_model:
            bid_model.delete_instance()

    def keys(self):
        bid_models = self.model.select()
        return [bid_model.bid_id for bid_model in bid_models]

    def keys_for_user(self, user_name):
        bid_models = self.model.select().where(self.model.user_name == user_name)
        return [bid_model.bid_id for bid_model in bid_models]

    def values(self):
        return self.get()

    def items(self):
        return [(bid.bid_id, bid) for bid in self.get()]

    def contains(self, bid_id):
        return bid_id in self.keys()

    def increment_left_to_approve(self, bid_id):
        bid_model = self.model.get_by_id(bid_id)
        bid_model.left_to_approval += 1
        bid_model.save()

    def decrement_left_to_approve(self, bid_id):
        bid_model = self.model.get_by_id(bid_id)
        bid_model.left_to_approval -= 1
        bid_model.save()

    def set_left_to_approve(self, bid_id, number):
        bid_model = self.model.get_by_id(bid_id)
        bid_model.left_to_approval = number
        bid_model.save()

    def set_status(self, bid_id, number):
        bid_model = self.model.get_by_id(bid_id)
        bid_model.status = number
        bid_model.save()

    def _map_bid_model_to_bid(self, bid_request_model):
        bid = bid_request_model
        my_bid = Bid(
            bid.bid_id,
            bid.user_name,
            bid.store_name,
            bid.offer,
            bid.product_id,
            bid.quantity
        )
        my_bid.set_users_to_approval(bid.left_to_approval)
        my_bid.set_status(bid.status)
        return my_bid

    def set_offer(self, bid_id, alternate_offer):
        bid_model = self.model.get_by_id(bid_id)
        bid_model.offer = alternate_offer
        bid_model.save()

    def get_highest_id(self):
        highest_id = self.model.select(fn.Max(self.model.bid_id)).scalar()
        if highest_id is None:
            return 0
        return highest_id
