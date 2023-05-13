from abc import ABC, abstractmethod

from ProjectCode.Domain.Helpers.JsonSerialize import JsonSerialize


class Policy(ABC):
    """
            percent := percent of the discount
            level := "Store" | "Category" | "Product"
            level_name := name of a category | product id | "" blank for store
    """
    def __init__(self, level, level_name):
        #self.percent = percent
        self.level = level
        self.level_name = level_name

    @abstractmethod
    def calculate(self, product, basket, total_price):
        pass

    @abstractmethod
    def parse(self):
        pass

    def _checkIfRelevant(self, product):
        if self.level == "Store":
            return True
        elif self.level == "Category":
            return self.level_name in product.get_categories()
        elif self.level == "Product":
            return self.level_name == product.get_product_id()
        return False


