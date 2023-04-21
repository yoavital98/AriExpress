class Bid:
    def __init__(self,bid_id, username, storename, offer, product, quantity, approved=False):
        self.bid_id = bid_id
        self._username = username
        self._storename = storename
        self._offer = offer
        self._product_ID = product
        self._quantity = quantity
        self._approved = approved

    def get_bid_id(self):
        return self.bid_id

    # Getter and setter for username
    def get_username(self):
        return self._username

    def set_username(self, username):
        self._username = username

    # Getter and setter for storename
    def get_storename(self):
        return self._storename

    def set_storename(self, storename):
        self._storename = storename

    # Getter and setter for offer
    def get_offer(self):
        return self._offer

    def set_offer(self, offer):
        self._offer = offer

    # Getter and setter for product
    def get_product(self):
        return self._product

    def set_product(self, product):
        self._product = product

    # Getter and setter for approved
    def get_approved(self):
        return self._approved

    def set_approved(self, approved):
        self._approved = approved
