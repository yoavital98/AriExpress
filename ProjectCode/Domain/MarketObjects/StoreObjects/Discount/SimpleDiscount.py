from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class SimpleDiscount(Policy):

    def __init__(self, percent, level, level_name, discount_id=-1):
        super().__init__(level, level_name)
        self.discount_id = discount_id
        self.percent = percent

    def calculate(self, product, basket, total_price):
        if super()._checkIfRelevant(product):
            return self.percent
        else:
            return 0

    def parse(self):
        pass

    def get_discount_id(self):
        return self.discount_id

    def get_discount_type(self):
        return "Simple"

    def get_percent(self):
        return self.percent

    def get_level(self):
        return self.level

    def get_level_name(self):
        return self.level_name

    def get_rule(self):
        return {}

    def get_discount_dict(self):
        return {}


    def __eq__(self, other):
        return self.percent == other.percent and self.level == other.level and self.level_name == other.level_name
    # =======================JSON=======================#

    def toJson(self):
        return{
            "percent": self.percent,
            "level": self.level,
            "level_name": self.level_name,
            # "rule": self.rule,
            "discount_type": "Simple"
        }
    # =======================FOR TESTS=======================#

    def calculateForTest(self):
        return self.percent
