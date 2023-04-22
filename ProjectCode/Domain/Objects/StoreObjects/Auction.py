from ProjectCode.Domain.Objects.UserObjects.Member import Member
from ProjectCode.Domain.Helpers.TypedDict import TypedDict
class Auction:
    def __init__(self, auction_id, product_id, starting_offer, current_offer, start_date, expiration_date, highest_offer_username):
        self.__auction_id = auction_id
        self.__product_id = product_id
        self.__starting_offer = starting_offer
        self.__current_offer = current_offer
        self.__start_date = start_date
        self.__expiration_date = expiration_date
        self.__highest_offer_username = highest_offer_username
        #self.__participants = TypedDict(str, Member)

    def add_participant(self, member):
        if self.__participants.get(member.get_username()) is None:
            self.__participants[member.get_username()] = member

    def get_participants(self):
        return self.__participants

    def get_auction_id(self):
        return self.__auction_id

    def set_auction_id(self, auction_id):
        self.__auction_id = auction_id

    def get_product_id(self):
        return self.__product_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def get_starting_offer(self):
        return self.__starting_offer

    def set_starting_offer(self, starting_offer):
        self.__starting_offer = starting_offer

    def get_current_offer(self):
        return self.__current_offer

    def set_current_offer(self, current_offer):
        self.__current_offer = current_offer

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_expiration_date(self):
        return self.__expiration_date

    def set_expiration_date(self, expiration_date):
        self.__expiration_date = expiration_date

    def get_highest_offer_username(self):
        return self.__highest_offer_username

    def set_highest_offer_username(self, highest_offer_username):
        self.__expiration_date = highest_offer_username
