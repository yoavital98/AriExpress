from ProjectCode.Domain.DataObjects.DataBid import *
from ProjectCode.Domain.Objects import Basket


class DataBasket:
    def __init__(self, basket: Basket):
        self.products = basket.get_Products() #returns Dict(int, tuple), int = product_id, tuple = (product_name,quantity)
        self.bids = self.getBids(basket.get_bids()) #returns Dict(int, DataBid) int= bid_id

    def getBids(self, bids_dict):
        bids = dict()
        for key, value in bids_dict.items():
            bids[key] = DataBid(value)
        return bids
