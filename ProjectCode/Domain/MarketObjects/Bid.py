class Bid:
    def __init__(self,bid_id, username, storename, offer, product_id, quantity):
        self.bid_id = bid_id
        self._username = username
        self._storename = storename
        self._offer = offer
        self._product_ID = product_id
        self._quantity = quantity
        self._status = 0 # 0-PENDING 1-APPROVED 2-REJECTED 3-ALTERNATE_OFFER
        self._left_to_approval = 0 #number of owners that needs to approve this bid


    def approve_by_one(self):
        self._left_to_approval -= 1

    def increment_left_to_approve(self):
        self._left_to_approval += 1

    def get_left_to_approval(self):
        return self._left_to_approval
        
    # Getter and setter for username
    def get_id(self):
        return self.bid_id

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
    def get_product_id(self):
        return self._product_ID

    def set_product(self, product):
        self._product = product

    # Getter and setter for approved
    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status
        
    def get_quantity(self):
        return self._quantity

    # =======================JSON=======================#
    def toJson(self):
        return{
            'bid_id': self.bid_id,
            'username': self._username,
            'storename': self._storename,
            'offer': self._offer.toJson(),
            'product': self._product.toJson(),
            'quantity': self._quantity,
            'status': self._status,
            'left_to_approval': self._left_to_approval
        }