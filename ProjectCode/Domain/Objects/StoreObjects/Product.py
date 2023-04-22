
class Product:
    def __init__(self, product_id, name, quantity, price, categories):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.categories = categories


    def get_product_id(self):
        return self.product_id


