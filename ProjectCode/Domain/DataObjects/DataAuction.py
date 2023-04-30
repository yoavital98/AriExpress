from ProjectCode.Domain.Objects.StoreObjects import Auction


class DataAuction:
    def __init__(self, auction: Auction):
        self.auction_id = auction.get_auction_id()
        self.product_id = auction.product_id()
        self.starting_offer = auction.starting_offer()
        self.current_offer = auction.current_offer()
        self.start_date = auction.start_date()
        self.expiration_date = auction.expiration_date()
        self.highest_offer_username = auction.highest_offer_username()
        self.participants = auction.get_participants() #(username,last_offer)