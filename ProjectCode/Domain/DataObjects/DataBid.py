from ProjectCode.Domain.Objects import Bid

class DataBid:
    def __init__(self, bid: Bid):
        self.bid_id = bid.bid_id
        self.username = bid.get_username()
        self.storename = bid.get_storename()
        self.offer = bid.get_offer()
        self.product_ID = bid.get_product()
        self.quantity = bid.get_quantity()
        self.status = bid.get_status()  # 0-PENDING 1-APPROVED 2-REJECTED 3-ALTERNATE_OFFER
