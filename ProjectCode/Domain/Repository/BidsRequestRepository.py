from ProjectCode.DAL.BidModel import BidModel
from ProjectCode.DAL.BidsRequestModel import BidsRequestModel
from ProjectCode.Domain.MarketObjects.Bid import Bid
from ProjectCode.Domain.Repository.Repository import Repository


class BidsRequestRepository(Repository):
    def __init__(self):
        self.model = BidsRequestModel

    def __getitem__(self, user_name):
        try:
            return self.get(user_name)
        except Exception as e:
            raise Exception("BidsRequestRepository: __getitem__ failed: " + str(e))

    def __setitem__(self, key, value):  # key is meaningless
        try:
            return self.add(key, value)
        except Exception as e:
            raise Exception("BidsRequestRepository: __setitem__ failed: " + str(e))

    def __delitem__(self, key):
        try:
            return self.remove(key)
        except Exception as e:
            raise Exception("BidsRequestRepository: __delitem__ failed: " + str(e))

    def __contains__(self, item):
        try:
            return self.contains(item)
        except Exception as e:
            return False

    def get(self, pk=None):
        if pk is not None:
            bid_request_models = self.model.select().where(self.model.wait_for_approve_user_name == pk)
            if bid_request_models:
                return [self._map_bid_request_model_to_bid(bid_request_model) for bid_request_model in
                        bid_request_models]
        else:
            bid_request_models = self.model.select()
            return [self._map_bid_request_model_to_bid(bid_request_model) for bid_request_model in bid_request_models]

    def add(self, key, bid: Bid):
        bid_model = BidModel.get_or_none(BidModel.bid_id == bid.bid_id)
        if bid_model:
            self.model.create(
                wait_for_approve_user_name=key,
                bid_id=bid_model
            )


    def remove(self, pk):
        pass

    def delete_bid_from_user(self, user_name, bid_id):
        bid_request_model = self.model.get_or_none(
            (self.model.wait_for_approve_user_name == user_name) &
            (self.model.bid_id.bid_id == bid_id)
        )
        if bid_request_model:
            bid_request_model.delete_instance()


    def keys(self):
        bid_request_models = self.model.select()
        return [bid_request_model.id for bid_request_model in bid_request_models]

    def values(self):
        return self.get()

    def contains(self, bid_id):
        return any(bid_id == bid_request.bid_id for bid_request in self.get())


    def _map_bid_request_model_to_bid(self, bid_request_model):
        bid = bid_request_model.bid_id
        return Bid(
            bid.bid_id,
            bid.user_name,
            bid.store_name,
            bid.offer,
            bid.product_id,
            bid.left_to_approval
        )
