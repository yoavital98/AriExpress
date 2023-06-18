import json



class Product:

    def __init__(self, product_id, name, quantity, price, categories):
        self.product_id = product_id
        self.name = name
        self.quantity = int(quantity)
        self.price = float(price)
        self.categories = categories

    def __str__(self):
        return f'{self.name} - {self.quantity} - {self.price} - {self.categories}'

    def __eq__(self, other):
        return self.product_id == other.product_id and self.name == other.name and self.quantity == other.quantity and self.price == other.price and self.categories == other.categories

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.price

    def get_categories(self):
        return self.categories

    def checkFeatures(self, features):
        for k, v in features.items():
            if k == "min_price":
                if self.price < v:
                    return False
            elif k == "max_price":
                if self.price > v:
                    return False
            else:
                raise Exception("invalid feature")
        return True

    # =======================JSON=======================#

    def toJson(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'categories': self.categories
            # 'categories': json.dumps(self.categories)
        }
