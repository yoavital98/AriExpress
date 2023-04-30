from ProjectCode.Domain.Objects.StoreObjects import Product


class DataProduct:
    def __init__(self, product: Product):
        self.product_id = product.get_product_id()
        self.name = product.get_name()
        self.quantity = product.get_quantity()
        self.price = product.get_price()
        self.categories = product.get_categories()
