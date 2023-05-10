from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.ConditionedDiscount import ConditionedDiscount
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.DiscountType import DiscountType
from ProjectCode.Domain.MarketObjects.StoreObjects.Discount.SimpleDiscount import SimpleDiscount


class AddComp(DiscountType):
    def __init__(self, discount_dict):
        super().__init__(0, "", "")
        self.discount_dict = discount_dict
        self.childs = list()

    # child: DiscountType
    def addChild(self, child):
        self.childs.append(child)

    def calculate(self, product, basket, total_price):
        added_percent = 0
        for child in self.childs:
            if child._checkIfRelevant(product):
                added_percent += child.calculate(product, basket, total_price)
        return added_percent

    def parse(self):
        for discount in self.discount_dict.values():
            new_discount = None
            discount_type, percent, level = discount["discount_type"], discount["percent"], discount["level"]
            level_name, rule = discount["level_name"], discount["rule"]
            if discount_type == "Conditioned":
                new_discount = ConditionedDiscount(percent, level, level_name, rule)
            elif discount_type == "Add":
                new_discount = AddComp(discount["discounts"])
            elif discount_type == "Max": #TODO: impl max discount
                pass
            elif discount_type == "Simple":
                new_discount = SimpleDiscount(percent, level, level_name)
            elif discount_type == "Coupon":  # TODO: impl coupon discount
                pass
            else:
                raise Exception("No such discount type exists")
            new_discount.parse()
            self.addChild(new_discount)

