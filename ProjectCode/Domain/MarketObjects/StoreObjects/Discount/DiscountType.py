from abc import ABC, abstractmethod


class DiscountType(ABC):
    """
            percent := percent of the discount
            level := "Store" | "Category" | "Product"
            level_name := name of a category | product id | "" blank for store
    """
    def __init__(self, percent, level, level_name):
        self.percent = percent
        self.level = level
        self.level_name = level_name

    @abstractmethod
    def calculate(self, product, basket, total_price, category_or_product_id):
        pass

    def _checkIfRelevant(self, arg):
        if self.level == "Store":
            return True
        elif self.level == "Category":
            return self.level_name == arg
        elif self.level == "Product":
            return self.level_name == arg
        return False

