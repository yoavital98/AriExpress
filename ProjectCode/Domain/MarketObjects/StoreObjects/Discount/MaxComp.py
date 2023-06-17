from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.AddComp import AddComp
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Policy import Policy


class MaxComp(Policy):
    def __init__(self, discount_dict, discount_id=-1):
        super().__init__("", "")
        self.discount_id = discount_id
        self.discount_dict = discount_dict
        self.childs = list()
        self.parse()

    # child: Policy
    def addChild(self, child: Policy):
        self.childs.append(child)

    def calculate(self, product, basket, total_price):
        max_percent = -1
        for child in self.childs:
            cur_percent = child.calculate(product, basket, total_price)
            if cur_percent > max_percent:
                max_percent = cur_percent
        return max_percent

    def parse(self):
        for discount in self.discount_dict.values():
            new_discount = None
            discount_type, percent, level = discount["discount_type"], discount["percent"], discount["level"]
            level_name = discount["level_name"]
            if discount_type == "Conditioned":
                new_discount = ConditionedDiscount(percent, level, level_name, discount["rule"])
            elif discount_type == "Add":
                new_discount = AddComp(discount["discounts"])
            elif discount_type == "Max":
                new_discount = MaxComp(discount["discounts"])
            elif discount_type == "Simple":
                new_discount = SimpleDiscount(percent, level, level_name)
            elif discount_type == "Coupon":  # TODO: impl coupon discount
                pass
            else:
                raise Exception("No such discount type exists")
            self.addChild(new_discount)

    def get_discount_id(self):
        return self.discount_id

    def get_discount_type(self):
        return "Max"

    def get_percent(self):
        return 0

    def get_level(self):
        return self.level

    def get_level_name(self):
        return self.level_name

    def get_rule(self):
        return {}

    def get_discount_dict(self):
        return self.discount_dict