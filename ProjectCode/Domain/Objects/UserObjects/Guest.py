from ProjectCode.Domain.Objects.User import User


class Guest(User):
    def __init__(self, username):
        super().__init__(username)

    def get_cart(self):
        return super().get_cart()

    def add_to_cart(self, storename, productID, product, quantity):
        super().add_to_cart(storename, productID, product, quantity)

    def get_Basket(self, storename):
        return super().get_Basket(storename)

    def removeFromBasket(self, storename, productID):
        super().removeFromBasket(storename, productID)

    def get_username(self):
        return super().get_username()


