from ProjectCode.Domain.DataObjects.DataAccess import DataAccess
from ProjectCode.Domain.DataObjects.DataAuction import DataAuction
from ProjectCode.Domain.DataObjects.DataBid import DataBid
from ProjectCode.Domain.DataObjects.DataLottery import DataLottery
from ProjectCode.Domain.DataObjects.DataProduct import DataProduct
from ProjectCode.Domain.MarketObjects import Store


class DataStore:
    def __init__(self, store: Store):
        self.store_name = store.get_store_name()
        self.products = self.getProducts(store.get_products())
        self.active = store.active
        self.accesses = self.getAcceses(store.get_accesses())
        self.bids = self.getBids(store.get_bids())
        self.bids_requests = self.getBidsRequests(store.get_bids_requests())
        self.auctions = self.getAuctions(store.get_auctions())
        self.lotteries = self.getLotteries(store.get_lottery())

    def getProducts(self, product_dict):
        products = dict()
        for key, value in product_dict.items():
            products[key] = DataProduct(value)
        return products

    def getAcceses(self, accesses_dict):
        accesses = dict()
        for key, value in accesses_dict.items():
            accesses[key] = DataAccess(value)
        return accesses

    def getBids(self, bids_dict):
        bids = dict()
        for key, value in bids_dict.items():
            bids[key] = DataBid(value)
        return bids

    def getBidsRequests(self, bids_request_dict):
        bids_requests = dict()
        for key, value in bids_request_dict.items():
            bids_requests[key] = DataBid(value)
        return bids_requests

    def getAuctions(self, auctions_dict):
        auctions = dict()
        for key, value in auctions_dict.items():
            auctions[key] = DataAuction(value)
        return auctions

    def getLotteries(self, lotteries_dict):
        lotteries = dict()
        for key, value in lotteries_dict.items():
            lotteries[key] = DataLottery(value)
        return lotteries
