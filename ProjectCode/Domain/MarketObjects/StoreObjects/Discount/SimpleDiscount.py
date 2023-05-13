from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class SimpleDiscount(Policy):

    def __init__(self, percent, level, level_name):
        super().__init__(level, level_name)
        self.percent = percent

    def calculate(self, product, basket, total_price):
        if super()._checkIfRelevant(product):
            return self.percent
        else:
            return 0

    def parse(self):
        pass

    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            # "rule": self.rule,
            "discount_type": "Simple"
        }

