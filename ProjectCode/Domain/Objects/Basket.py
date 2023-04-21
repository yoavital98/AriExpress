from ProjectCode.Domain.Objects.Store import Store


class Basket:
    def __init__(self, cart_id, store):
        self.cart_id = cart_id
        self.store: Store = store
        self.products = []

    def add_Product(self, product):
        self.products.add(product)

    def remove_Product(self, product):
        self.products.remove(product)

    def get_Cart_Id(self):
        return self.cart_id

    def set_Cart_Id(self, cart_id):
        self.cart_id = cart_id

    def get_Store(self):
        return self.store

    def set_Store(self, store):
        self.store = store

    def get_Products(self):
        return self.products