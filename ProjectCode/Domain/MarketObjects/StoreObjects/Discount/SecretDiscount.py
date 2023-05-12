from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class SecretDiscount(Policy):
    def __init__(self):
        pass

    def calculate(self, product, basket, total_price):
        pass

    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            #"rule": self.rule,
            "discount_type": "Secret"
        }